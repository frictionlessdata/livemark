document.addEventListener("DOMContentLoaded", function () {
  const content = document.querySelector("#livemark-main");
  const headings = content.querySelectorAll("h1, h2, h3, h4, h5, h6, h7");
  const headingMap = {};

  // Add identifiers
  Array.prototype.forEach.call(headings, function (heading) {
    const id = heading.id
      ? heading.id
      : heading.textContent
          .trim()
          .toLowerCase()
          .split(" ")
          .join("-")
          .replace(/[!@#$%^&*():]/gi, "")
          .replace(/\//gi, "-");
    headingMap[id] = !isNaN(headingMap[id]) ? ++headingMap[id] : 0;
    if (headingMap[id]) {
      heading.id = id + "-" + headingMap[id];
    } else {
      heading.id = id;
    }
  });

  // Add links
  Array.prototype.forEach.call(headings, function (heading) {
    const link = document.createElement("a");
    link.href = "#" + heading.id;
    link.innerText = "#";
    link.classList.add("heading");
    heading.appendChild(link);
  });
});
