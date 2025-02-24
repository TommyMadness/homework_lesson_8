"""
Протестируйте классы из модуля homework/models.py
"""

import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity

        assert product.check_quantity(0) is True
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1001) is False
        product.buy(300)
        assert product.check_quantity(700)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        initial_quantity = product.quantity
        product.buy(100)
        final_quantity = product.quantity
        assert product.quantity == initial_quantity - 100
        assert initial_quantity != final_quantity
        product.buy(900)
        quantity_final = product.quantity
        assert quantity_final == 0

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        buy_values = [1001, 1002, 1300, 1500, 1800, 2000]

        for value in buy_values:
            with pytest.raises(ValueError):
                product.buy(value)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, product, cart):
        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 2
        cart.add_product(product, buy_count=3)
        assert cart.products[product] == 5

    def test_remove_product_whole(self, product, cart):
        cart.add_product(product, buy_count=5)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_partial(self, product, cart):
        cart.add_product(product, buy_count=5)
        cart.remove_product(product, remove_count=2)
        assert cart.products[product] == 3

    def test_clear(self, product, cart):
        cart.add_product(product, buy_count=5)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, product, cart):
        cart.add_product(product, buy_count=3)
        expected_total_price = product.price * 3
        assert cart.get_total_price() == expected_total_price

    def test_cart_buy_success(self, product, cart):
        cart.add_product(product, buy_count=10)
        initial_quantity = product.quantity
        cart.buy()
        assert product.quantity == initial_quantity - 10
        assert len(cart.products) == 0

    def test_cart_buy_insufficient(self, product, cart):
        cart.add_product(product, buy_count=product.quantity + 1)
        with pytest.raises(ValueError):
            cart.buy()
        assert product in cart.products
