from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import is_seller_required, is_seller_product
from django.contrib import messages
from .forms import ProductForm, BookForm, PhoneForm
from django.urls import reverse
from .models import *


###--------------------------------------------------
###-----------------------Home Page------------------
###--------------------------------------------------

#main page, showing the 6 items with more visualizations
def home(request):
    top_products = Products.objects.all().order_by('-views')[:6]
    return render(request, 'loja/home.html', {'products': top_products})

#search a product
def product_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Products.objects.filter(name__icontains=query)
    else:
        products = Products.objects.all()

    return render(request, 'loja/product_search.html', {'products': products, 'query': query})

#Filter by category. We get the categories automaticaly by the context_processors file
def category_details(request, class_name):
    subclasses = Products.__subclasses__()
    class_map = {cls.__name__: cls for cls in subclasses}
    class_map['Products'] = Products
    if class_name in class_map:
        model_class = class_map[class_name]
        products = Products.objects.instance_of(model_class)
    else:
        products = []

    return render(request, 'loja/category_detail.html', {'class_name': class_name, 'products': products})

###---------------------------------------------------
###-----------------------Login Page------------------
###---------------------------------------------------

#Allows to register into the shop
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'loja/register.html', {'form': form})

#Allows to login into the shop
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'loja/login.html', {'error': 'User and/or password are wrong'})
    return render(request, 'loja/login.html')

#Allows to logout
def custom_logout(request):
    logout(request)
    return redirect('home')

###--------------------------------------------------
###-----------------------User Page------------------
###--------------------------------------------------

#open the menu for the user. Needs to be login decorator
@login_required
def user_settings(request):
    return render(request, 'loja/user_settings.html', {'user': request.user})

#Option to become a seller
@login_required
def user_settings(request):
    if request.method == "POST" and "become_seller" in request.POST:
        user = request.user
        user.is_seller = True
        user.save()
        messages.success(request, "Parabéns! Você agora é um vendedor.")
        return redirect('user_settings')

    return render(request, 'loja/user_settings.html', {'user': request.user})


#Allows to sell an item. needs to be a seller. interactively via JS we'll know which category it is
@is_seller_required
def offer_product(request):
    product_type = request.POST.get('product_type','other')
    form = None

    if product_type == 'book':
        form = BookForm(request.POST or None, request.FILES or None)
    elif product_type == 'phone':
        form = PhoneForm(request.POST or None, request.FILES or None)
    else:
        form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return redirect(reverse('product_detail', args=[product.id]))

    return render(request, 'loja/offer_product.html', {'form': form, 'product_type': product_type})

#Follow your stock and sales
def my_sales(request):
    sales = Purchase.objects.filter(seller_id=request.user.id)
    products = Products.objects.filter(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update":
            product_id = request.POST.get("product_id")
            new_stock = request.POST.get("stock")
            product = Products.objects.get(id=product_id, user=request.user)
            product.stock = new_stock
            product.save()
            messages.success(request, "Stock updated successfully!")
            return redirect("my_items")


    return render(request, 'loja/my_items.html', {'sales': sales,'products': products})

#Update your sales status
def update_status(request, purchase_id):
    sale = get_object_or_404(Purchase, id=purchase_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in dict(Purchase.STATUS_CHOICES).keys():
            sale.status = new_status
            sale.save()

    return redirect('my_items')

#follow your shopping
@login_required
def follow_shopping(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('product')
    return render(request, 'loja/follow_shopping.html',{'purchases': purchases})


###-----------------------------------------------------
###-----------------------Product Page------------------
###-----------------------------------------------------

#Page of the product
def product_detail(request, product_id):
    product = Products.objects.get(id=product_id)
    product.views += 1
    product.save()

    return render(request, 'loja/product_detail.html', {'product': product, 'product_type': product.__class__.__name__})

#option to buy a product
@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if product.stock < 1:
        messages.error(request, "This product is out of stock!")
        return redirect('product_detail', product_id=product.id)

    if request.method == 'POST':
        Purchase.objects.create(user=request.user,seller=product.user, product=product, quantity=1, status='pending')
        product.stock -= 1
        product.save()
        return redirect('follow_shopping')

    return render(request, 'loja/buy_product.html', {'product': product})

#Option to delete a product
@is_seller_product
def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('home')

    return render(request, 'loja/delete_product.html', {'product': product})

#Option to edit a product
@is_seller_product
def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'loja/edit_product.html', {'form': form, 'product': product, 'product_type': product.__class__.__name__})





