from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.template import Context

# Create your views here.

def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    
    if request.method == 'POST':
        print("I'm here")
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order = order, product = item['product'], price = item['fee'], quantity = item['quantity'])
            
            #send email
            body_email = "Cám ơn bạn! Đơn hàng của bạn đã được đặt thành công, mã đơn hàng là " + str(order.id)
            email = EmailMessage(subject='Thông tin đặt hàng', body=body_email, to=[order.email], from_email='discovery.info1993@gmail.com')
            email.send()
            #remove giỏ hàng
            cart.clear()

            return render(request, 'orders/created.html', context= {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', context={'form': form})