// Small extras, all optional: every page works without this file (both sessions
// simply show one after the other, and the cards scroll sideways on their own).
// Workout pages: session tabs (today's preselected), Prev/Next + numbered pips per deck,
// "Mark done" per exercise (kept for today), and the deck reopens on your last card.
// Home: highlights today's session.
(() => {
  const today = new Date().getDay();
  // Push/Pull/Legs alternate weekly: odd ISO weeks are week A (session 1), even weeks are week B (session 2)
  const isoWeek = (date) => {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    return Math.ceil(((d - Date.UTC(d.getUTCFullYear(), 0, 1)) / 864e5 + 1) / 7);
  };
  const weekAB = isoWeek(new Date()) % 2 ? "A" : "B";
  const dateKey = new Date().toISOString().slice(0, 10);
  const page = location.pathname;
  const store = {
    get(key) { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} },
  };

  // ── Session tabs ──────────────────────────────────────────
  const tabs = [...document.querySelectorAll(".tab")];
  const decks = [...document.querySelectorAll(".deck")];
  const showDeck = (id) => {
    decks.forEach((deck) => { deck.hidden = deck.id !== id; });
    tabs.forEach((tab) => tab.setAttribute("aria-current", String(tab.hash === "#" + id)));
  };
  if (tabs.length) {
    tabs.forEach((tab) => tab.addEventListener("click", (event) => {
      event.preventDefault();
      showDeck(tab.hash.slice(1));
      history.replaceState(null, "", tab.hash);
    }));
    const target = location.hash && document.getElementById(location.hash.slice(1));
    const fromHash = target && target.closest(".deck");
    const thisWeek = tabs.find((tab) => tab.dataset.week === weekAB) || tabs[0];
    tabs.forEach((tab) => { if (tab === thisWeek) tab.querySelector(".tab-day").textContent = "this week"; });
    showDeck(fromHash ? fromHash.id : thisWeek.hash.slice(1));
  }

  // ── Decks: pips, Prev/Next, done marks, resume ─────────────
  const doneKey = "done:" + page + ":" + dateKey;
  const done = new Set(store.get(doneKey) || []);
  const lastKey = "card:" + page;

  decks.forEach((deck) => {
    const track = deck.querySelector(".track");
    const cards = [...track.children];
    const pips = deck.querySelector(".pips");
    const prev = deck.querySelector(".deck-prev");
    const next = deck.querySelector(".deck-next");
    prev.hidden = next.hidden = false;
    // long decks show a counter instead of pips on phones
    const counter = document.createElement("p");
    counter.className = "deck-count";
    counter.setAttribute("aria-live", "polite");
    pips.after(counter);
    if (cards.length > 5) deck.classList.add("is-long");

    const pipLinks = cards.map((card) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = "#" + card.id;
      a.textContent = card.querySelector(".card-num").textContent;
      a.setAttribute("aria-label", card.querySelector("h3").textContent);
      a.addEventListener("click", (event) => { event.preventDefault(); go(cards.indexOf(card)); });
      li.append(a);
      pips.append(li);
      return a;
    });

    let current = 0;
    const offset = (card) => card.offsetLeft - track.offsetLeft - parseFloat(getComputedStyle(track).paddingLeft);
    const go = (i) => {
      const card = cards[Math.max(0, Math.min(cards.length - 1, i))];
      track.scrollTo({ left: offset(card), behavior: "smooth" });
      if (deck.getBoundingClientRect().top < 0) deck.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    // the deck is as tall as the tallest card in view (one on phones, two on wide screens)
    const fit = () => {
      const left = track.scrollLeft, right = left + track.clientWidth;
      const shown = (card) => Math.min(right, offset(card) + card.offsetWidth) - Math.max(left, offset(card));
      const inView = cards.filter((card) => shown(card) > card.offsetWidth * 0.6);
      track.style.height = Math.max(...(inView.length ? inView : [cards[current]]).map((card) => card.offsetHeight)) + "px";
    };
    const mark = (i, save = true) => {
      current = i;
      pipLinks.forEach((a, n) => a.setAttribute("aria-current", String(n === i)));
      const doneHere = cards.filter((card) => done.has(card.id)).length;
      counter.textContent = `${i + 1} / ${cards.length}` + (doneHere ? ` · ${doneHere} done` : "");
      fit();
      prev.disabled = i === 0;
      next.disabled = i === cards.length - 1;
      if (save) store.set(lastKey, { id: cards[i].id, t: Date.now() });
    };
    prev.addEventListener("click", () => go(current - 1));
    next.addEventListener("click", () => go(current + 1));

    let settle;
    track.addEventListener("scroll", () => {
      clearTimeout(settle);
      settle = setTimeout(() => {
        const nearest = cards.reduce((best, card, n) =>
          Math.abs(offset(card) - track.scrollLeft) < Math.abs(offset(cards[best]) - track.scrollLeft) ? n : best, 0);
        if (nearest !== current) mark(nearest);
      }, 80);
    }, { passive: true });
    // keep the deck as tall as the current card (Notes open/close, images load)
    const resize = new ResizeObserver(fit);
    cards.forEach((card) => resize.observe(card));

    cards.forEach((card, i) => {
      const button = card.querySelector(".done");
      const render = () => {
        const isDone = done.has(card.id);
        card.classList.toggle("is-done", isDone);
        pipLinks[i].classList.toggle("is-done", isDone);
        button.setAttribute("aria-pressed", String(isDone));
        button.textContent = isDone ? "Done ✓ — tap to undo" : "Mark done";
      };
      button.hidden = false;
      button.addEventListener("click", () => {
        if (done.has(card.id)) done.delete(card.id); else done.add(card.id);
        store.set(doneKey, [...done]);
        render();
        mark(current, false);
        if (done.has(card.id) && i < cards.length - 1) setTimeout(() => go(i + 1), 450);
      });
      render();
    });
    mark(0, false);
  });

  // Reopen on the card from the URL, or the last card viewed in the past 3 hours
  const last = store.get(lastKey);
  const startId = (location.hash && location.hash.slice(1)) || (last && Date.now() - last.t < 3 * 3600e3 && last.id);
  const startCard = startId && document.getElementById(startId);
  if (startCard && startCard.classList.contains("card")) {
    const deck = startCard.closest(".deck");
    if (tabs.length) showDeck(deck.id);
    requestAnimationFrame(() => {
      const track = deck.querySelector(".track");
      track.scrollLeft = startCard.offsetLeft - track.offsetLeft - parseFloat(getComputedStyle(track).paddingLeft);
      track.dispatchEvent(new Event("scroll"));
    });
  }

  // ── Reading pages: highlight the chip of the section in view ─
  const chips = [...document.querySelectorAll(".chips a")];
  if (chips.length) {
    const byId = new Map(chips.map((a) => [a.hash.slice(1), a]));
    const spy = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        chips.forEach((a) => a.removeAttribute("aria-current"));
        const chip = byId.get(entry.target.id);
        if (chip) { chip.setAttribute("aria-current", "true"); chip.scrollIntoView({ block: "nearest", inline: "nearest" }); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll(".panel > h2[id]").forEach((h) => spy.observe(h));
  }

  // ── Home: today's session ─────────────────────────────────
  document.querySelectorAll(".week-ab").forEach((el) => {
    if (el.textContent === "1 / 2") el.textContent = weekAB === "A" ? "week A · 1" : "week B · 2";
  });
  const day = document.querySelector(`.week [data-day="${today}"]`);
  const todayLink = document.querySelector(".today");
  if (day) {
    day.classList.add("is-today");
    const link = day.querySelector("a");
    if (todayLink && link) {
      todayLink.href = link.getAttribute("href");
      const session = day.querySelector(".week-ab") ? `${link.textContent} ${weekAB === "A" ? 1 : 2}` : link.textContent;
      todayLink.querySelector(".today-name").textContent = session.toLowerCase();
      todayLink.style.setProperty("--field", getComputedStyle(day).getPropertyValue("--field"));
      todayLink.hidden = false;
    }
  }
})();
