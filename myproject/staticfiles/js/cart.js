document.addEventListener("DOMContentLoaded", () => {
    renderCart();
    renderFavorites();
});


/* =========================
   LOCAL STORAGE
========================= */

function getCart() {
    return JSON.parse(localStorage.getItem("novastore_cart")) || [];
}

function getFavorites() {
    return JSON.parse(localStorage.getItem("novastore_favorites")) || [];
}

function saveCart(cart) {
    localStorage.setItem("novastore_cart", JSON.stringify(cart));
}

function saveFavorites(favorites) {
    localStorage.setItem(
        "novastore_favorites",
        JSON.stringify(favorites)
    );
}


/* =========================
   CART
========================= */

function addToCart(product) {

    let cart = getCart();

    const existing = cart.find(
        item => item.id === product.id
    );

    if (existing) {
        existing.quantity += 1;
    } else {
        product.quantity = 1;
        cart.push(product);
    }

    saveCart(cart);

    alert("🛒 Mahsulot savatga qo‘shildi!");
}


function removeFromCart(id) {

    let cart = getCart();

    cart = cart.filter(
        item => item.id !== id
    );

    saveCart(cart);

    renderCart();
}


function changeQuantity(id, amount) {

    let cart = getCart();

    const item = cart.find(
        product => product.id === id
    );

    if (!item) return;

    item.quantity += amount;

    if (item.quantity <= 0) {
        cart = cart.filter(
            product => product.id !== id
        );
    }

    saveCart(cart);

    renderCart();
}


/* =========================
   RENDER CART
========================= */

function renderCart() {

    const container =
        document.getElementById("cart-items");

    const empty =
        document.getElementById("cart-empty");

    const summary =
        document.getElementById("cart-summary");

    const count =
        document.getElementById("cart-count");

    const summaryCount =
        document.getElementById("summary-count");

    const totalElement =
        document.getElementById("cart-total");


    if (!container) return;


    const cart = getCart();


    if (cart.length === 0) {

        container.innerHTML = "";

        empty.style.display = "block";

        summary.style.display = "none";

        count.textContent = "0 ta mahsulot";

        return;
    }


    empty.style.display = "none";

    summary.style.display = "flex";


    let total = 0;
    let totalProducts = 0;


    container.innerHTML = cart.map(item => {

        total += Number(item.price) * item.quantity;

        totalProducts += item.quantity;


        return `
            <div class="cart-item">

                <div class="cart-image">
                    <img
                        src="${item.image}"
                        alt="${item.name}"
                    >
                </div>


                <div class="cart-info">

                    <h3>${item.name}</h3>

                    <div class="cart-price">
                        $${Number(item.price).toFixed(2)}
                    </div>


                    <div class="quantity-box">

                        <button
                            onclick="changeQuantity(${item.id}, -1)"
                        >
                            −
                        </button>

                        <span class="quantity-number">
                            ${item.quantity}
                        </span>

                        <button
                            onclick="changeQuantity(${item.id}, 1)"
                        >
                            +
                        </button>

                    </div>

                </div>


                <div class="cart-right">

                    <div class="item-total">
                        $${(
                            Number(item.price) *
                            item.quantity
                        ).toFixed(2)}
                    </div>

                    <button
                        class="remove-btn"
                        onclick="removeFromCart(${item.id})"
                        title="O‘chirish"
                    >
                        🗑
                    </button>

                </div>

            </div>
        `;

    }).join("");


    count.textContent =
        `${totalProducts} ta mahsulot`;

    summaryCount.textContent =
        totalProducts;

    totalElement.textContent =
        `$${total.toFixed(2)}`;
}


/* =========================
   FAVORITES
========================= */

function addToFavorites(product) {

    let favorites = getFavorites();

    const exists = favorites.some(
        item => item.id === product.id
    );

    if (!exists) {

        favorites.push(product);

        saveFavorites(favorites);

        alert("❤️ Sevimlilarga qo‘shildi!");

        renderFavorites();
    }
}


function removeFromFavorites(id) {

    let favorites = getFavorites();

    favorites = favorites.filter(
        item => item.id !== id
    );

    saveFavorites(favorites);

    renderFavorites();
}


/* =========================
   RENDER FAVORITES
========================= */

function renderFavorites() {

    const container =
        document.getElementById("favorite-items");

    const empty =
        document.getElementById("favorite-empty");

    const count =
        document.getElementById("favorite-count");


    if (!container) return;


    const favorites = getFavorites();


    count.textContent =
        `${favorites.length} ta`;


    if (favorites.length === 0) {

        container.innerHTML = "";

        empty.style.display = "block";

        return;
    }


    empty.style.display = "none";


    container.innerHTML = favorites.map(item => {

        return `
            <div class="favorite-card">

                <div class="favorite-image">

                    <img
                        src="${item.image}"
                        alt="${item.name}"
                    >

                </div>


                <h3>
                    ${item.name}
                </h3>


                <div class="favorite-card-price">
                    $${Number(item.price).toFixed(2)}
                </div>


                <div class="favorite-actions">

                    <button
                        class="favorite-cart-btn"
                        onclick='favoriteToCart(${JSON.stringify(item)})'
                    >
                        🛒 Savatga
                    </button>

                    <button
                        class="favorite-delete-btn"
                        onclick="removeFromFavorites(${item.id})"
                    >
                        ♥
                    </button>

                </div>

            </div>
        `;

    }).join("");
}


/* =========================
   FAVORITE → CART
========================= */

function favoriteToCart(product) {

    addToCart({
        id: product.id,
        name: product.name,
        price: product.price,
        image: product.image
    });
}


/* =========================
   CHECKOUT
========================= */

function checkout() {

    const cart = getCart();

    if (cart.length === 0) {

        alert("Savat bo‘sh!");

        return;
    }


    alert(
        "🎉 Buyurtmangiz qabul qilindi!"
    );
}

/* =========================
   PRODUCT PAGE BUTTONS
========================= */

function getProductFromCard(button) {

    const card = button.closest(".product-card");

    return {
        id: Number(card.dataset.id),

        name: card.dataset.name,

        price: Number(card.dataset.price),

        image: card.dataset.image
    };
}


function cartProduct(button) {

    const product =
        getProductFromCard(button);

    addToCart(product);

    button.classList.add("added");

    button.innerHTML = `
        <span>✓</span>
        <span>Savatga qo‘shildi</span>
    `;

    setTimeout(() => {

        button.classList.remove("added");

        button.innerHTML = `
            <span class="cart-icon">🛒</span>
            <span>Savatga qo‘shish</span>
        `;

    }, 1500);
}


function favoriteProduct(button) {

    const product =
        getProductFromCard(button);

    let favorites =
        getFavorites();

    const exists =
        favorites.some(
            item => item.id === product.id
        );


    if (exists) {

        removeFromFavorites(product.id);

        button.classList.remove("active");

        button.innerHTML = "♡";

    } else {

        addToFavorites(product);

        button.classList.add("active");

        button.innerHTML = "♥";

    }
}