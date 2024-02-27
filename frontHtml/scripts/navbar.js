import loadPage from "./load-page.js"

function navbar() {
  const navbarObject = document.getElementById("navbar");
  console.log(navbarObject);
  for (const child of navbarObject.children) {
    const button = child.getElementsByTagName("button")[0];
    button.addEventListener("click", function() {
      loadPage(button);
    });
  }
}

navbar();
