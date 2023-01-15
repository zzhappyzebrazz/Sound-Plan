from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from player.models import Event
from listener.models import Listener
from cart.models import Order, OrderItem

# Create your views here.

def cart(request):
    cart = Cart(request)

    check_out = ''
    user = 0

    if 's_user' in request.session:
        user = request.session['s_user']
    #Update tickets quantity
    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for item in cart:
            print('quantity2_' + str(item['event'].id))
            quantity_new = int(request.POST.get('quantity2_' + str(item['event'].id)))
            print('quantity_new ', quantity_new)
            if quantity_new != 0:
                product_cart = {
                    str(item['event'].pk): {
                        'quantity': quantity_new, 
                        'price': str(item['price']), 
                    }
                }
                cart_new.update(product_cart)
                item['quantity'] = quantity_new
            else:
                cart.remove(item['event'])
        else:
            request.session['cart'] = cart_new

    if request.POST.get('btnCheckout'):
        if user:
            listerner = Listener.objects.get(id=user['id'])
            # Save Order
            order = Order()
            order.listener = listerner
            order.total = cart.get_total_price()
            order.save()

            # Save OrderItem
            for item in cart:
                OrderItem.objects.create(order=order,
                                        event=item['event'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            
            # Send Mail

            # Clear Cart
            cart.clear()
            # print(user['id'])
            return render(request, 'player/checkout.html')
        else:
            check_out = '''
            <div class="alert alert-danger" role="alert">
                You must Login before checkout!
            </div>
            '''
            print('s_user = request.session')


    return render(request, 'player/cart.html', {
        'cart': cart,
        'check_out' : check_out,
        'user' : user,
    })

def checkout(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        return redirect('cart:cart')
    
    if request.POST.get('bntPlayOrder'):
        listener = Listener.objects.get(id=request.session.get('s_user')['id'])
        
        #save order
        order = Order()
        order.listener = listener
        order.total = cart.get_total_price()
        order.save()
        
        # save Order Item
        for item in cart:
            OrderItem.objects.create(order=order,
                                     event=item['event'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            
        #Send mail here
        
        # Play Order successful
        return render(request, 'player/order-result.html', {
            'cart' : cart,
        })
        
    return render(request, 'player/checkout.html', {
        'cart' : cart,
    })

def buy_now(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    print(event)
    print(cart)
    if request.POST.get('quantity'):
        
        quantity = int(request.POST.get('quantity'))
        print("quantity =", quantity)
        cart.add(event, quantity)
    print(len(cart))
    return redirect('cart:cart')

def delete(request, event_id):
    cart = Cart(request)
    event = get_object_or_404(Event, id=event_id)
    cart.remove(event)
    return redirect('cart:cart')
