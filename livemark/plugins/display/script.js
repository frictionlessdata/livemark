document.addEventListener("DOMContentLoaded", function () {
  // Init
  const readability = localStorage.getItem("livemark-display-readability");
  if (readability === "plus") {
    document.body.classList.add("with-readability");
  } else {
    document.body.classList.remove("with-readability");
  }

  // Plus
  document
    .getElementById("livemark-display-plus")
    .addEventListener("click", function () {
      document.body.classList.add("with-readability");
      localStorage.setItem("livemark-display-readability", "plus");
    });

  // Minus
  document
    .getElementById("livemark-display-minus")
    .addEventListener("click", function () {
      document.body.classList.remove("with-readability");
      localStorage.setItem("livemark-display-readability", "minus");
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
