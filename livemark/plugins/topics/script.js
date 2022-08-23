document.addEventListener("DOMContentLoaded", function () {
  // Start tocbot
  tocbot.init({
    // Where to render the table of contents.
    tocSelector: ".toc",
    // Where to grab the headings to build the table of contents.
    contentSelector: "#livemark-main",
    // Which headings to grab inside of the contentSelector element.
    headingSelector: "{{ plugin.selector }}",
    // For headings inside relative or absolute positioned containers within content.
    hasInnerContainers: true,
    // Called each time a heading is parsed. Expects a string in return.
    headingLabelCallback: (label) => {
      label = label.replace(/(^#|#$)/g, "").trim();
      // label = label.replace(/\(.*?\)$/g, "");
      return label;
    },
    // Disable generating ordered lists (ol)
    orderedList: false,
    // Fix active link class
    onClick: syncList,
    scrollEndCallback: syncList,
  });

  // Style list
  $("#livemark-topics .toc > ul").addClass("primary");
  $("#livemark-topics .toc > ul > li").addClass("primary");
  $("#livemark-topics .toc > ul > li > a").addClass("primary");
  $("#livemark-topics .toc ul.is-collapsible").addClass("secondary");
  $("#livemark-topics .toc ul.is-collapsible li").addClass("secondary");
  $("#livemark-topics .toc ul.is-collapsible li > a").addClass("secondary");
  for (const element of $("#livemark-topics .primary")) {
    if ($(element).find(".secondary").length) {
      $(element).addClass("group");
    }
  }

  // Sync list
  function syncList() {
    for (const element of $("#livemark-topics li.primary")) {
      if ($(element).find(".is-active-li").length) {
        $(element).addClass("is-active-li");
      }
    }
  }
  syncList();
});
