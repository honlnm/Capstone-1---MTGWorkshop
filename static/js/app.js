document.querySelectorAll(".deck-icon").forEach(function (deckIcon) {
    deckIcon.addEventListener("click", function () {
        var popup = deckIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
    });
});

document.querySelectorAll(".closePopup").forEach(function (closeButton) {
    closeButton.addEventListener("click", function () {
        var popup = closeButton.closest(".popup");
        popup.style.display = "none";
    });
});




document.querySelectorAll(".qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function () {
        var popup = qtyIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
    });
});