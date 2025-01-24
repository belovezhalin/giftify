// class ActionStrategy {
//     execute(productId, action) {
//         throw new Error("This method should be overridden");
//     }
// }

// class AuthenticatedUserStrategy extends ActionStrategy {
//     execute(productId, action) {
//         console.log('User is authenticated, sending data...');

//         var url = '/update_item/';

//         fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-type': 'application/json',
//                 'X-CSRFToken': csrftoken,
//             },
//             body: JSON.stringify({ 'productId': productId, 'action': action })
//         })
//         .then((response) => {
//             return response.json();
//         })
//         .then((data) => {
//             location.reload();
//         });
//     }
// }

// class UnauthenticatedUserStrategy extends ActionStrategy {
//     execute(productId, action) {
//         console.log('User is not authenticated');

//         if (action == 'add') {
//             if (cart[productId] == undefined) {
//                 cart[productId] = { 'quantity': 1 };
//             } else {
//                 cart[productId]['quantity'] += 1;
//             }
//         }

//         if (action == 'remove') {
//             cart[productId]['quantity'] -= 1;

//             if (cart[productId]['quantity'] <= 0) {
//                 console.log('Item should be deleted');
//                 delete cart[productId];
//             }
//         }

//         console.log('Cart:', cart);
//         document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";

//         location.reload();
//     }
// }