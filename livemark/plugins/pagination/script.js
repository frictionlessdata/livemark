document.addEventListener("DOMContentLoaded", function () {
  const conainer = $(".livemark-pagination");
  const elements = conainer
    .children()
    .map((index, element) => element.outerHTML)
    .get();
  conainer.html(`
    <div class="livemark-pagination-data"></div>
    <div class="livemark-pagination-navs"></div>
  `);
  conainer.find(".livemark-pagination-navs").pagination({
    dataSource: elements,
    callback: (html) => {
      conainer.find(".livemark-pagination-data").html(html);
    },
  });
  conainer.show();
});
