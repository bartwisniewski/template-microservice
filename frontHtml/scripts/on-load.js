import includeHtml from "./include.js";
import navbar from "./navbar.js";

document.addEventListener("DOMContentLoaded", function() {
    console.log("for include");
  includeHtml();
      console.log("after include");
  navbar();
        console.log("after navbar");
});