from django.shortcuts import render, get_object_or_404, redirect
from urllib3 import request
from .models import Product, ReviewRating
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from orders.models import OrderProduct

# Create your views here.
def store(request, category_slug = None):
    categories = None
    products = None
    if not(category_slug == None):
        categories = get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products' : paged_products,
        'product_count' : product_count
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    
    #product variations
    variation_categories = single_product.variation_categories.all()
    #product reviews
    reviews = ReviewRating.objects.filter( product=single_product, is_approved=True).order_by('-created_at')    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'variation_categories': variation_categories,
        'reviews': reviews,
        "review_form": ReviewForm()
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html', context)


@login_required(login_url='login')
def submit_review(request, product_id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        product = get_object_or_404(Product, id=product_id)

        # Check purchased product
        has_purchased = OrderProduct.objects.filter(user=request.user, product=product, ordered=True).exists()
        

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.user = request.user
            review.product = product
            review.rating = request.POST.get('rating')
            review.ip = request.META.get('REMOTE_ADDR')
            review.is_verified_purchase = has_purchased

            review.save()

            messages.success(request, "Thank you! Your review has been submitted.")

    return redirect(url)