// TODO: make it remember this setting from prev pages
document.addEventListener("DOMContentLoaded", function () {
  // Plus
  document
    .getElementById("livemark-controls-plus")
    .addEventListener("click", function () {
      document.body.classList.add("with-readability");
    });

  // Minus
  document
    .getElementById("livemark-controls-minus")
    .addEventListener("click", function () {
      document.body.classList.remove("with-readability");
    });

  // Scroll
  const scrollSpeed = parseInt("{{ speed }}");
  UeScroll.init({ element: ".ue-scroll", scrollSpeed });
});
