document.addEventListener("DOMContentLoaded", function () {
  // Plus
  document
    .getElementById("livemark-display-plus")
    .addEventListener("click", function () {
      document.body.classList.add("with-readability");
    });

  // Minus
  document
    .getElementById("livemark-display-minus")
    .addEventListener("click", function () {
      document.body.classList.remove("with-readability");
    });

  // Scroll
  const scrollSpeed = parseInt("{{ speed }}");
  UeScroll.init({ element: ".ue-scroll", scrollSpeed });
});
