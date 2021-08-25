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

  // Print
  document
    .getElementById("livemark-display-print")
    .addEventListener("click", function () {
      window.print();
    });

  // Scroll
  const scrollSpeed = parseInt("{{ plugin.speed }}");
  UeScroll.init({ element: "#livemark-display-scroll .fa", scrollSpeed });
});
