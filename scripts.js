document.addEventListener("DOMContentLoaded", function () {
  // Simple subtle animation hook if you want to extend later
  const cards = document.querySelectorAll(".metric-container");
  cards.forEach((card, idx) => {
    card.style.opacity = 0;
    card.style.transform = "translateY(10px)";
    setTimeout(() => {
      card.style.transition = "all 300ms ease-out";
      card.style.opacity = 1;
      card.style.transform = "translateY(0)";
    }, 80 * idx);
  });
});
