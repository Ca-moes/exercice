// Local Quartz transformer: add native lazy-loading to content images so
// off-screen exercise clips don't block the initial page load.
// Shipped pre-built in dist/ so `quartz plugin install` skips the build step.
export default function LazyImages() {
  return {
    name: "LazyImages",
    htmlPlugins() {
      return [
        () => (tree) => {
          const walk = (node) => {
            if (node && node.tagName === "img") {
              node.properties = node.properties || {}
              if (node.properties.loading === undefined) node.properties.loading = "lazy"
              if (node.properties.decoding === undefined) node.properties.decoding = "async"
            }
            if (node && node.children) {
              for (const child of node.children) walk(child)
            }
          }
          walk(tree)
        },
      ]
    },
  }
}
