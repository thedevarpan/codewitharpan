// Function to update cart quantity
function updateCartQuantity(event, element, itemId, action) {
    event.preventDefault();
    const url = `/shop/update-cart-quantity/${itemId}/`;
    
    // AJAX call to update cart quantity
    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'action': action,
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function(response) {
            // Update the quantity and subtotal in the DOM
            element.parentNode.querySelector('input').value = response.new_quantity;
            document.getElementById(`subtotal-${response.item_id}`).innerText = `₹${response.new_subtotal}`;
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', status, error);
        }
    });
}

// Function to remove an item from the cart
function removeFromCart(event, itemId) {
    event.preventDefault();
    const url = `/shop/remove-from-cart/${itemId}/`;

    // AJAX call to remove item
    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        success: function(response) {
            if (response.success) {
                // Remove the item's row from the DOM
                document.querySelector(`#subtotal-${itemId}`).closest('tr').remove();
            }
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', status, error);
        }
    });
}
