# type: ignore
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import Product, Category, Brand, WishlistItem, Order, OrderItem
from .forms import IndividualRegistrationForm, CorporateRegistrationForm, StudioRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import IndividualRegistrationForm, CorporateRegistrationForm, StudioRegistrationForm
from .models import IndividualProfile, CorporateProfile, StudioProfile


# Group checker
def in_group(group_name):
    def check(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(check)


# --------------------------- Auth Views ---------------------------

def register_view(request):
    account_type = request.GET.get('type', 'individual')

    if request.method == 'POST':
        if account_type == 'individual':
            form = IndividualRegistrationForm(request.POST, request.FILES)
        elif account_type == 'corporate':
            form = CorporateRegistrationForm(request.POST, request.FILES)
        elif account_type == 'studio':
            form = StudioRegistrationForm(request.POST, request.FILES)
        else:
            form = IndividualRegistrationForm(request.POST, request.FILES)  # fallback

        if not request.POST.get('password1') or not request.POST.get('password2'):
            messages.error(request, "Password is required.")
        elif form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()

                if account_type == 'individual':
                    IndividualProfile.objects.create(user=user, full_name=form.cleaned_data.get('full_name', ''))
                elif account_type == 'corporate':
                    CorporateProfile.objects.create(
                        user=user,
                        company_name=form.cleaned_data.get('company_name', ''),
                        ceo_name=form.cleaned_data.get('ceo_name', '')
                    )
                elif account_type == 'studio':
                    StudioProfile.objects.create(user=user, studio_name=form.cleaned_data.get('studio_name', ''))

                login(request, user)
                messages.success(request, "Registration successful!")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Registration error: {str(e)}")
        else:
            messages.error(request, "Please fix the form errors.")
    else:
        form = None

    context = {
        'individual_form': IndividualRegistrationForm(request.POST or None, request.FILES or None) if account_type == 'individual' else IndividualRegistrationForm(),
        'corporate_form': CorporateRegistrationForm(request.POST or None, request.FILES or None) if account_type == 'corporate' else CorporateRegistrationForm(),
        'studio_form': StudioRegistrationForm(request.POST or None, request.FILES or None) if account_type == 'studio' else StudioRegistrationForm(),
        'account_type': account_type
    }

    return render(request, 'rental/register.html', context)

    
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/')
    return render(request, 'rental/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def account_view(request):
    return render(request, 'rental/account.html', {'user': request.user})


# --------------------------- General Views ---------------------------

def home(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    all_products = Product.objects.all()

    filtered_products = all_products
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    if search_query:
        filtered_products = filtered_products.filter(name__icontains=search_query)
    if category_id:
        filtered_products = filtered_products.filter(category__id=category_id)
    if brand_id:
        filtered_products = filtered_products.filter(brand__id=brand_id)

    context = {
        'products': filtered_products,
        'best_sellers': all_products[:10],
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'rental/home.html', context)


def about_view(request):
    return render(request, 'rental/about.html')


def gallery_view(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    products = Product.objects.all()

    if search_query:
        products = products.filter(Q(name_icontains=search_query) | Q(description_icontains=search_query))
    if category_id:
        products = products.filter(category__id=category_id)
    if brand_id:
        products = products.filter(brand__id=brand_id)

    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(request, 'rental/gallery.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'rental/product_detail.html', {'product': product})


@login_required
@in_group('customer')
def customer_dashboard(request):
    return render(request, 'rental/customer_dashboard.html')


# --------------------------- Wishlist Views ---------------------------

@login_required
def wishlist_view(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'rental/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, "Item added successfully ✅")
    else:
        messages.info(request, "Item is already in your wishlist.")
    return redirect(request.META.get('HTTP_REFERER', 'gallery'))


@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, pk=item_id, user=request.user)
    item.delete()
    return redirect('wishlist')


# --------------------------- Cart Views ---------------------------

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key in cart:
        if isinstance(cart[key], dict):
            cart[key]['quantity'] += 1
        else:
            cart[key] = {'quantity': cart[key] + 1, 'price': float(product.price), 'rental_days': 1}
    else:
        cart[key] = {'quantity': 1, 'price': float(product.price), 'rental_days': 1}

    request.session['cart'] = cart
    messages.success(request, "Item added successfully ✅")
    return redirect('gallery')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        if not isinstance(item, dict):
            continue

        quantity = item.get('quantity', 1)
        price = float(item.get('price', product.price))
        rental_days = int(item.get('rental_days', 1))
        subtotal = price * quantity * rental_days

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'rental_days': rental_days,
            'subtotal': subtotal
        })
        total += subtotal

    context = {
        'cart_items': cart_items,
        'total': total,
        'message': request.GET.get('message')
    }
    return render(request, 'rental/cart.html', context)


@require_POST
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    new_quantity = int(request.POST.get('quantity', 1))

    if key in cart:
        if new_quantity > 0:
            if isinstance(cart[key], dict):
                cart[key]['quantity'] = new_quantity
            else:
                cart[key] = {'quantity': new_quantity, 'price': 0, 'rental_days': 1}
        else:
            del cart[key]

    request.session['cart'] = cart
    messages.success(request, "Cart updated successfully.")
    return redirect('cart')


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)

    if key in cart:
        del cart[key]

    request.session['cart'] = cart
    messages.success(request, "Item removed from your cart.")
    return redirect('cart')


# --------------------------- Checkout ---------------------------

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.success(request, "Your order has been placed!")
        return redirect('my_orders')

    if request.method == 'POST':
        try:
            start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Invalid rental dates.")
            return redirect('checkout')

        delivery_option = request.POST.get('delivery_option')
        name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        is_delivery = (delivery_option == 'delivery')
        total_price = 0

        order = Order.objects.create(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            is_delivery=is_delivery,
            delivery_name=name if is_delivery else '',
            delivery_phone=phone if is_delivery else '',
            delivery_address=address if is_delivery else '',
            city=city if is_delivery else '',
            zip_code=zip_code if is_delivery else '',
            total_price=0
        )

        for product_id, item in cart.items():
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                continue

            if not isinstance(item, dict):
                continue

            quantity = int(item.get('quantity', 1))
            price = float(item.get('price', product.price))
            rental_days = (end_date - start_date).days or 1

            total_price += price * quantity * rental_days

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        order.total_price = total_price
        order.save()

        request.session['cart'] = {}
        messages.success(request, "Your order has been placed!")
        return redirect('my_orders')

    # GET request - show checkout page
    cart_items = []
    subtotal = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        if not isinstance(item, dict):
            continue

        quantity = item.get('quantity', 1)
        rental_days = item.get('rental_days', 1)
        price = float(item.get('price', product.price))
        total = quantity * rental_days * price
        subtotal += total

        cart_items.append({
            'id': product_id,
            'product': product,
            'quantity': quantity,
            'rental_days': rental_days,
            'total_price': total,
        })

    delivery_fee = 0
    total = subtotal + delivery_fee

    return render(request, 'rental/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total
    })


@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        # Placeholder for Stripe / Payment integration
        return redirect('home')
    return redirect('checkout')


# ❌ Clear Cart
def clear_cart(request):
    request.session['cart'] = {}
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__product')
    return render(request, 'rental/my_orders.html', {'orders': orders})






@login_required
def my_orders (request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'rental/my_orders.html', {'orders': orders})

def contact_view(request):
    return render(request, 'rental/contact.html')