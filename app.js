// Replace the Google Forms placeholder once you have the live URL.
// Set this to your live form (e.g. "https://docs.google.com/forms/d/e/.../viewform")
// and the apply buttons will start opening it in a new tab.
const FORM_URL = ""; // TODO: paste Google Forms URL here

document.addEventListener("DOMContentLoaded", () => {
  const formLinks = document.querySelectorAll("[data-form-link]");
  if (FORM_URL) {
    formLinks.forEach((el) => {
      el.setAttribute("href", FORM_URL);
      el.textContent = "応募フォームを開く →";
    });
  }

  // Smooth-scroll polish (browsers without CSS scroll-behavior fallback).
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href").slice(1);
      if (!id) return;
      const target = document.getElementById(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", `#${id}`);
    });
  });
});
