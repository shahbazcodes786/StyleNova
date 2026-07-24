from urllib import request

from django.shortcuts import render,redirect, get_object_or_404
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from orders.models import PaymentMethod

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get selected variations
    product_variation = []

    if request.method == "POST":
        print(request.POST)

        for key, value in request.POST.items():
            print(key, "=", value)
        

            if key == "csrfmiddlewaretoken":
                continue

            if value == "":
                continue

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__name__iexact=key,
                    variation_value__iexact=value,
                    is_active=True,
                )
                print("FOUND:", variation)
                product_variation.append(variation)

            except Exception as e:
                print("ERROR:", e)

    # ================= AUTHENTICATED USER =================

    if request.user.is_authenticated:

        cart_items = CartItem.objects.filter(
            user=request.user,
            product=product
        )

        existing_variations = []
        cart_item_ids = []

        for item in cart_items:
            existing_variations.append(list(item.variations.all()))
            cart_item_ids.append(item.id)

        if product_variation in existing_variations:
            index = existing_variations.index(product_variation)

            cart_item = CartItem.objects.get(
                id=cart_item_ids[index]
            )

            cart_item.quantity += 1
            cart_item.save()

        else:
            cart_item = CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=1,
            )

            if product_variation:
                cart_item.variations.set(product_variation)

        return redirect("cart")

    # ================= GUEST USER =================

    else:

        cart, created = Cart.objects.get_or_create(
            cart_id=_cart_id(request)
        )

        cart_items = CartItem.objects.filter(
            cart=cart,
            product=product
        )

        existing_variations = []
        cart_item_ids = []

        for item in cart_items:
            existing_variations.append(list(item.variations.all()))
            cart_item_ids.append(item.id)

        if product_variation in existing_variations:
            index = existing_variations.index(product_variation)

            cart_item = CartItem.objects.get(
                id=cart_item_ids[index]
            )

            cart_item.quantity += 1
            cart_item.save()

        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1,
            )

            if product_variation:
                cart_item.variations.set(product_variation)

        return redirect("cart")
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        
        else:
            cart_item.delete()

    except:
        pass
    return redirect('cart')

def remove_cart_items(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_item=None, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    
    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,

    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        
        payment_methods = PaymentMethod.objects.filter(is_active=True)  
    
    except ObjectDoesNotExist:
        pass # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'store/checkout.html', context)
