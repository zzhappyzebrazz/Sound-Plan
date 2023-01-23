from decimal import Decimal
from django.conf import settings
from player.models import Event


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the events
        from the database.
        """
        event_ids = self.cart.keys()
        # get the event objects and add them to the cart
        events = Event.objects.filter(id__in=event_ids)

        cart = self.cart.copy()
        for event in events:
            cart[str(event.id)]['event'] = event

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            '''
            The yield statement suspends a function’s execution and sends a value back to the caller, but retains enough
            state to enable the function to resume where it left off. When the function resumes, it continues execution 
            immediately after the last yield run. This allows its code to produce a series of values over time, rather 
            than computing them at once and sending them back like a list.
            '''
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, event, quantity=1, override_quantity=False):
        """
        Add a event to the cart or update its quantity.
        """
        event_id = str(event.id)
        if event_id not in self.cart:
            self.cart[event_id] = {'quantity': quantity, 'price': str(event.price)}
        else:
            self.cart[event_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, event):
        """
        Remove a event from the cart.
        """
        event_id = str(event.id)
        if event_id in self.cart:
            del self.cart[event_id]
            self.save()

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] * 1 for item in self.cart.values())
