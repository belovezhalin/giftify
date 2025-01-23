<div>
<script type="text/javascript" src="{% static 'js/strategy.js' %}"></script>
<script type="text/javascript" src="{% static 'js/cart.js' %}"></script>
</div>

var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        var strategy;
        if (user === 'AnonymousUser') {
            strategy = new UnauthenticatedUserStrategy();
        } else {
            strategy = new AuthenticatedUserStrategy();
        }

        strategy.execute(productId, action);
    });
}