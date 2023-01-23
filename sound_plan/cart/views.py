from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from player.models import Event
from listener.models import Listener
from cart.models import Order, OrderItem
from django.core.mail import send_mail, EmailMultiAlternatives
from sound_plan.settings import EMAIL_HOST_USER, BASE_DIR
from email.mime.image import MIMEImage
import os
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
            listener = Listener.objects.get(id=user['id'])
            # Save Order
            order = Order()
            order.listener = listener
            order.total = cart.get_total_price()
            order.save()

            # Save OrderItem
            for item in cart:
                OrderItem.objects.create(order=order,
                                        event=item['event'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            
            # Send Mail
            name = listener.first_name + ' ' + listener.last_name
            #Send mail here
            subject = 'Order Confirmation at SOUND-PLAN '
            content = f'<p>Hello from Sound-Plan to you!!! <b> { name } </b>,</p>'
            content += '<p>We are happy to received your welcome and Order tickets at Sound-Plan!</p>'
            content += f'<p>Hope that you wil have a wonderful time with your friends and seeing you favorite Artists.</p>'
            content += f'<p>Show this QR code at the Event and You are done.!!!</p>'
            content += f'<img src="cid:QR code.png" />'
            content += f'<p>SoundPlan</p>'
            
            # send_mail(post.subject, content, EMAIL_HOST_USER, [post.email])
            
            msg = EmailMultiAlternatives(
                subject,
                content,
                EMAIL_HOST_USER,
                [listener.email]
            )
            msg.mixed_subtype = 'related'
            msg.attach_alternative(content, "text/html")
            img_dir = 'player/static/player/img/QRcode.png'
            file_path = os.path.join(BASE_DIR, img_dir)
            print('file path')
            print(file_path)
            with open(file_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<{name}>'.format(name='QR code.png'))
                img.add_header('Content-Disposition', 'inline', filename='QR code.png')
            msg.attach(img)
            msg.send()

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
