from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from store.models import Product
from .forms import OrderForm
import datetime
from .models import Order, OrderProduct, Payment, PaymentMethod
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Create your views here.

def payments(request, order_number):
    order = Order.objects.get(
        order_number=order_number,
        user=request.user,
        is_ordered=False
    )

    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        payment_screenshot = request.FILES.get('payment_screenshot')
        
        payment = Payment()

        payment.user = request.user
        payment.payment_method = order.payment_method
        payment.amount_paid = order.order_total
        payment.transaction_id = transaction_id
        payment.payment_screenshot = payment_screenshot
        payment.status = 'Pending'

        payment.save()
    
        order.payment = payment
        order.save()
        
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:

            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product.id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            
            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()

            orderproduct.variations.set(product_variation)
            
            
            #reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        #clear the cart item
        CartItem.objects.filter(user=request.user).delete()
        
        order.is_ordered = True
        order.save()
        
        
        
        
        #send order received email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()

        return redirect('home')
    
    

    context = {
        'order': order,
        'payment_method': order.payment_method,
        'grand_total': order.order_total,
        'cart_items': cart_items,
    }

    return render(request, 'orders/payments.html', context)


def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    else:
    
        grand_total = 0
        tax = 0
        
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                payment_method_id = request.POST.get('payment_method')
                payment_method = PaymentMethod.objects.get(id=payment_method_id)
                #store all billing information inside Order table
                data = Order()
                data.user = current_user
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.order_note = form.cleaned_data['order_note']
                data.order_total = grand_total
                data.tax = tax
                data.ip = request.META.get('REMOTE_ADDR')
                data.payment_method = payment_method
                data.save()
                
                #generate order number
                yr = int(datetime.date.today().strftime('%Y')) 
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.datetime(yr,mt,dt)
                current_date = d.strftime('%Y%m%d') #20260714
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

                context = {
                    'order':order,
                    'cart_items':cart_items,
                    'total':total,
                    'tax':tax,
                    'grand_total':grand_total,
                    'payment_method':payment_method
                    
                }
                return redirect('payments', order_number=order.order_number)
                
            else:
                return redirect('checkout')
            
        else:
            return redirect('checkout')
        
        

        


