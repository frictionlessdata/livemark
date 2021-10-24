document.addEventListener("DOMContentLoaded", function () {
  const container = $(".livemark-pagination");
  if (container.length) {
    const elements = container
      .children()
      .map((index, element) => element.outerHTML)
      .get();
    container.html(`
      <div class="livemark-pagination-data"></div>
      <div class="livemark-pagination-navs"></div>
    `);
    container.find(".livemark-pagination-navs").pagination({
      dataSource: elements,
      callback: (html) => {
        container.find(".livemark-pagination-data").html(html);
      },
    });
    container.show();
  }
});
