var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productoId = this.dataset.producto;
        var action = this.dataset.action;
        console.log('productoId:', productoId, 'action:', action);
        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('no tiene una cuenta');
        } else {
            updateUserOrder(productoId, action);
        }
    });
}

function updateUserOrder(productoId, action) {
    console.log('usuario tiene una cuenta, enviando data...');
    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productoId': productoId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        updateCartDisplay(data, productoId);
        showCartModal();
    });
}

function updateCartDisplay(data, productoId) {
    var cartTotal = document.getElementById('cart-total');
    if (cartTotal) {
        cartTotal.innerHTML = data.cartItems;
    }

    var cartTotalAmount = document.getElementById('cart-total-amount');
    if (cartTotalAmount) {
        cartTotalAmount.innerHTML = '$' + data.cartTotal.toFixed(2);
    }

    var itemsCount = document.getElementById('items-count');
    if (itemsCount) {
        itemsCount.innerHTML = data.cartItems;
    }

    if (data.removed) {
        var itemRow = document.querySelector('.cart-row[data-producto="' + productoId + '"]');
        if (itemRow) {
            itemRow.remove();
        }
    } else {
        var itemQuantity = document.getElementById('quantity-' + productoId);
        if (itemQuantity) {
            itemQuantity.innerHTML = data.itemCantidad;
        }

        
        var itemTotal = document.getElementById('item-total-' + productoId);
        if (itemTotal) {
            itemTotal.innerHTML = '$' + data.itemTotal.toFixed(2);
        }
    }
}


function showCartModal() {
    var modal = document.getElementById("cartModal");
    if (modal) {
        modal.style.display = "block";
        var closeModalBtn = document.getElementById("closeModal");
        if (closeModalBtn) {
            closeModalBtn.onclick = function() {
                modal.style.display = "none";
            }

            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        }
    }
}
