// TODO: make it remember this setting from prev pages
document.addEventListener("DOMContentLoaded", function () {
  // Plus
  document
    .getElementById("livemark-panel-plus")
    .addEventListener("click", function () {
      document.body.classList.add("with-readability");
    });

  // Minus
  document
    .getElementById("livemark-panel-minus")
    .addEventListener("click", function () {
      document.body.classList.remove("with-readability");
    });
});
