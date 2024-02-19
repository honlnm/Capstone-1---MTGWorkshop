document.querySelectorAll(".deck-icon").forEach(function (deckIcon) {
    deckIcon.addEventListener("click", function () {
        const popup = deckIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
    });
});

document.querySelectorAll(".closePopup").forEach(function (closeButton) {
    closeButton.addEventListener("click", function () {
        const popup = closeButton.closest(".popup");
        popup.style.display = "none";
    });
});

// --------------INVENTORY-------------

document.querySelectorAll(".inv-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        const popup = qtyIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        evt.target.closest(".card-div").querySelector(".inv-qty-div > .inv-qty").setAttribute("id", `inv-${userId.toString()}-${cardId.toString()}`);
    });
});

document.querySelectorAll(".form-inv-qty").forEach(function (invQtyForm) {
    invQtyForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const inputData = evt.target.querySelector(".inv-qty-field").value
        try {
            const response = await fetch("/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/adjust-qty", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ data: inputData })
            });

            if (!response.ok) {
                throw new Error("Failed to update data");
            }

            const responseData = await response.json();
            document.getElementById(`inv-${userId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
        }
    })
});

// --------------WISHLIST-------------

document.querySelectorAll(".wl-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        const popup = qtyIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        evt.target.closest(".card-div").querySelector(".wl-qty-div > .wl-qty").setAttribute("id", `wl-${userId.toString()}-${cardId.toString()}`);
    });
});

document.querySelectorAll(".form-wl-qty").forEach(function (wlQtyForm) {
    wlQtyForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const inputData = evt.target.querySelector(".wl-qty-field").value
        try {
            const response = await fetch("/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/adjust-qty", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ data: inputData })
            });

            if (!response.ok) {
                throw new Error("Failed to update data");
            }

            const responseData = await response.json();
            document.getElementById(`wl-${userId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
        }
    })
});

// --------------DECK-------------

document.querySelectorAll(".deck-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        const popup = qtyIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const deckId = evt.target.closest(".card-div").getAttribute("data-deck-id");
        evt.target.closest(".card-div").querySelector(".deck-qty-div > .deck-qty").setAttribute("id", `deck-${userId.toString()}-${deckId.toString()}-${cardId.toString()}`);
    });
});

document.querySelectorAll(".form-deck-qty").forEach(function (deckQtyForm) {
    deckQtyForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const deckId = evt.target.closest(".card-div").getAttribute("data-deck-id");
        const inputData = evt.target.querySelector(".deck-qty-field").value
        try {
            const response = await fetch("/user/" + userId.toString() + "/deck/" + deckId.toString() + "/" + cardId.toString() + "/adjust-qty", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ data: inputData })
            });

            if (!response.ok) {
                throw new Error("Failed to update data");
            }

            const responseData = await response.json();
            document.getElementById(`deck-${userId}-${deckId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
        }
    })
});