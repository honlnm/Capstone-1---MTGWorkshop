function vwToPx(value) {
    var vw = document.documentElement.clientWidth;
    return (value * vw) / 100;
}

function updateDropdownWidth() {
    var dropdownContent = document.querySelector(".dropdown-content");
    var vwWidth = 100;
    var pxWidth = vwToPx(vwWidth);
    if (pxWidth <= 600) {
        dropdownContent.style.marginLeft = (-pxWidth + 54) + "px";
        dropdownContent.style.width = 100 + 'vw';
    }
}

window.addEventListener("resize", updateDropdownWidth);

updateDropdownWidth();

// ############## GENERAL #################

document.querySelectorAll(".closePopup").forEach(function (closeButton) {
    closeButton.addEventListener("click", function () {
        const popup = closeButton.closest(".popup");
        popup.setAttribute("style", "display: none;")
    });
});

document.querySelectorAll(".deck-icon").forEach(function (deckIcon) {
    deckIcon.addEventListener("click", function () {
        const popup = deckIcon.parentElement.querySelector(".popup");
        popup.style.display = "block";
    })
})

// ############## NAVBAR DROPDOWN #################

document.querySelector("#hamburger-icon").addEventListener("click", function () {
    const dropdown = document.getElementById("dropdown")
    if (dropdown.style.display === "none") {
        dropdown.style.display = "block"
    } else {
        dropdown.style.display = "none"
    }
})

// ############## LOADING ANIMATION #################

window.addEventListener('load', function () {
    var loader = document.getElementById('loading-page-container');
    loader.style.display = 'none';
});

// ############## DECK ICON #################

document.querySelectorAll(".form-add-card-to-deck").forEach(function (deckForm) {
    deckForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const selectElement = evt.target.querySelector(".deck-selection")
        const inputData = selectElement.options[selectElement.selectedIndex].value
        console.log(inputData)
        try {
            const response = await fetch("/deck/user/" + userId.toString() + "/deck/" + cardId.toString() + "/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ data: inputData })
            });
            if (!response.ok) {
                throw new Error("Failed to update data");
            }
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    });
});


// ############## INVENTORY ICON #################


document.querySelectorAll(".g-inv-icon").forEach(function (invIcon) {
    invIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const cardClass = evt.target.getAttribute("class")
        try {
            if (cardClass == "bw-inv-icon card-icons") {
                const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/add", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/in_inventory_icon.png")
                evt.target.setAttribute("class", "g-inv-icon card-icons")
            } else {
                const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/remove", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/inventory_icon.png")
                evt.target.setAttribute("class", "bw-inv-icon card-icons")
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

document.querySelectorAll(".bw-inv-icon").forEach(function (invIcon) {
    invIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const cardClass = evt.target.getAttribute("class")
        try {
            if (cardClass == "bw-inv-icon card-icons") {
                const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/add", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/in_inventory_icon.png")
                evt.target.setAttribute("class", "g-inv-icon card-icons")
            } else {
                const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/remove", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/inventory_icon.png")
                evt.target.setAttribute("class", "bw-inv-icon card-icons")
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## WISH LIST ICON #################

document.querySelectorAll(".g-wl-icon").forEach(function (wlIcon) {
    wlIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const cardClass = evt.target.getAttribute("class")
        try {
            if (cardClass == "bw-wl-icon card-icons") {
                const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/add", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/in_wishlist_icon.png")
                evt.target.setAttribute("class", "g-wl-icon card-icons")
            } else {
                const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/remove", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/wishlist_icon.png")
                evt.target.setAttribute("class", "bw-wl-icon card-icons")
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

document.querySelectorAll(".bw-wl-icon").forEach(function (wlIcon) {
    wlIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const cardClass = evt.target.getAttribute("class")
        try {
            if (cardClass == "bw-wl-icon card-icons") {
                const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/add", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/in_wishlist_icon.png")
                evt.target.setAttribute("class", "g-wl-icon card-icons")
            } else {
                const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/remove", {
                    method: "POST"
                });
                if (!response.ok) {
                    throw new Error("Failed to update data");
                }
                document.getElementById("loading-page-container").setAttribute("style", "display: none;")
                evt.target.setAttribute("src", "/static/images/wishlist_icon.png")
                evt.target.setAttribute("class", "bw-wl-icon card-icons")
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## DECK REMOVE ICON #################

document.querySelectorAll(".deck-rmv-icon").forEach(function (rmvIcon) {
    rmvIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const deckId = evt.target.closest(".card-div").getAttribute("data-deck-id");
        try {
            const response = await fetch("/deck/user/" + userId.toString() + "/deck/" + deckId.toString() + "/" + cardId.toString() + "/remove", {
                method: "POST"
            });
            if (!response.ok) {
                throw new Error("Failed to update data");
            }
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            evt.target.closest(".card-div").remove()
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## WISH LIST REMOVE ICON #################

document.querySelectorAll(".wl-rmv-icon").forEach(function (rmvIcon) {
    rmvIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        try {
            const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/remove", {
                method: "POST"
            });
            if (!response.ok) {
                throw new Error("Failed to update data");
            }
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            evt.target.closest(".card-div").remove()
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## INVENTORY REMOVE ICON #################

document.querySelectorAll(".inv-rmv-icon").forEach(function (rmvIcon) {
    rmvIcon.addEventListener("click", async function (evt) {
        evt.preventDefault()
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        try {
            const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/remove", {
                method: "POST"
            });
            if (!response.ok) {
                throw new Error("Failed to update data");
            }
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            evt.target.closest(".card-div").remove()
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});


// ############## INVENTORY CARD QTY #################

document.querySelectorAll(".inv-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        fetch('/update-last-activity', { method: 'POST' });
        const popup = qtyIcon.nextElementSibling;
        popup.style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        evt.target.closest(".card-div").querySelector(".inv-qty-div > .inv-qty").setAttribute("id", `inv-${userId.toString()}-${cardId.toString()}`);
    });
});

document.querySelectorAll(".form-inv-qty").forEach(function (invQtyForm) {
    invQtyForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const inputData = evt.target.querySelector(".inv-qty-field").value
        try {
            const response = await fetch("/inv/user/" + userId.toString() + "/inventory/" + cardId.toString() + "/adjust-qty", {
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
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            document.getElementById(`inv-${userId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## WISH LIST CARD QTY #################

document.querySelectorAll(".wl-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        fetch('/update-last-activity', { method: 'POST' });
        const popup = qtyIcon.nextElementSibling;
        popup.style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        evt.target.closest(".card-div").querySelector(".wl-qty-div > .wl-qty").setAttribute("id", `wl-${userId.toString()}-${cardId.toString()}`);
    });
});

document.querySelectorAll(".form-wl-qty").forEach(function (wlQtyForm) {
    wlQtyForm.addEventListener("submit", async function (evt) {
        evt.preventDefault();
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const inputData = evt.target.querySelector(".wl-qty-field").value
        try {
            const response = await fetch("/wl/user/" + userId.toString() + "/wishlist/" + cardId.toString() + "/adjust-qty", {
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
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            document.getElementById(`wl-${userId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});

// ############## DECK CARD QTY #################

document.querySelectorAll(".deck-qty-icon").forEach(function (qtyIcon) {
    qtyIcon.addEventListener("click", function (evt) {
        fetch('/update-last-activity', { method: 'POST' });
        const popup = qtyIcon.nextElementSibling;
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
        fetch('/update-last-activity', { method: 'POST' });
        document.getElementById("loading-page-container").style.display = "block";
        const userId = evt.target.closest(".card-div").getAttribute("data-user-id");
        const cardId = evt.target.closest(".card-div").getAttribute("data-card-id");
        const deckId = evt.target.closest(".card-div").getAttribute("data-deck-id");
        const inputData = evt.target.querySelector(".deck-qty-field").value
        try {
            const response = await fetch("/deck/user/" + userId.toString() + "/deck/" + deckId.toString() + "/" + cardId.toString() + "/adjust-qty", {
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
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
            document.getElementById(`deck-${userId}-${deckId}-${cardId}`).textContent = `Qty ${responseData.updatedData}`
            evt.target.closest(".popup").style.display = "none"
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("loading-page-container").setAttribute("style", "display: none;")
        }
    })
});