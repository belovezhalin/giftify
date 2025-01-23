from decimal import Decimal

class ProductDecorator:
    def __init__(self, product):
        self._product = product

    def __getattr__(self, name):
        return getattr(self._product, name)

class SaleDecorator(ProductDecorator):
    def __init__(self, product, discount):
        super().__init__(product)
        self.discount = discount

    @property
    def sale_price(self):
        return self._product.price * Decimal(1 - self.discount / 100)

class SpecialOccasionDecorator(ProductDecorator):
    def __init__(self, product, occasion):
        super().__init__(product)
        self.occasion = occasion

    @property
    def mark(self):
        return f"Special Occasion: {self.occasion}"