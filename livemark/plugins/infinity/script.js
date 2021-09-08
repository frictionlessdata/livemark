document.addEventListener("DOMContentLoaded", function () {
  const container = $(".livemark-infinity");
  if (container.length) {
    const elements = container
      .children()
      .map((index, element) => element.outerHTML)
      .get();
    container.html(elements.splice(0, 100));
    container.show();
    window.addEventListener("scroll", () => {
      const element = container.get(0);
      const position = window.scrollY + window.innerHeight + 100;
      const threshold = element.offsetTop + element.scrollHeight;
      if (position > threshold) {
        container.append(elements.splice(0, 100));
      }
    });
  }
});
