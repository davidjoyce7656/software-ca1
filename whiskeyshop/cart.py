# store/cart.py
from decimal import Decimal
from django.conf import settings
from .models import Whiskey

class Cart:
    def __init__(self, request):
        """
        Initialize the cart with the session data.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, whiskey, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        whiskey_id = str(whiskey.id)
        if whiskey_id not in self.cart:
            self.cart[whiskey_id] = {
                'quantity': 0,
                'price': str(whiskey.price)
            }
        if override_quantity:
            self.cart[whiskey_id]['quantity'] = quantity
        else:
            self.cart[whiskey_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as modified to save changes.
        """
        self.session.modified = True

    def remove(self, whiskey):
        """
        Remove a product from the cart.
        """
        whiskey_id = str(whiskey.id)
        if whiskey_id in self.cart:
            del self.cart[whiskey_id]
            self.save()

    def clear(self):
        """
        Remove all items from the cart.
        """
        self.cart = {}
        self.save()

    def __iter__(self):
        """
        Iterate through the cart items and fetch products from the database.
        """
        whiskey_ids = self.cart.keys()
        whiskeys = Whiskey.objects.filter(id__in=whiskey_ids)
        for whiskey in whiskeys:
            self.cart[str(whiskey.id)]['whiskey'] = whiskey

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    """Count all items in the cart."""
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    """Calculate the total price of items in the cart."""
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
