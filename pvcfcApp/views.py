from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Category
from django.shortcuts import get_object_or_404

def checkout(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)

    # 👇 THÊM ĐOẠN NÀY
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')

        # test trước
        print("Payment method:", payment_method)

        # TODO: sau này tạo Order ở đây

        return render(request, 'pvcfcApp/success.html')  # tạo file này

    return render(request, 'pvcfcApp/checkout.html', {
        'cart': cart,
        'total': total
    })


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    context = {'product': product}

    return render(request, 'pvcfcApp/detail.html', {
        'product': product
    })

def home(request):
    products = Product.objects.all()
    categories = Category.objects.filter(parent=None)

    return render(request, 'pvcfcApp/index.html', {
        'products': products,
        'categories': categories
    })


def cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render(request, 'pvcfcApp/cart.html', {
        'cart': cart,
        'total': total
    })


def add_to_cart(request):
    if request.method == "POST":
        name = request.POST.get('name')
        price = int(request.POST.get('price'))
        product_id = request.POST.get('id')

        cart = request.session.get('cart', [])

        for item in cart:
            if item['name'] == name:
                item['quantity'] += 1
                break
        else:
            cart.append({
                'name': name,
                'price': price,
                'quantity': 1
            })

        request.session['cart'] = cart
        return JsonResponse({'status': 'ok'})


def update_cart(request):
    if request.method == "POST":
        index = int(request.POST.get('index'))
        action = request.POST.get('action')

        cart = request.session.get('cart', [])

        if action == "inc":
            cart[index]['quantity'] += 1
        elif action == "dec":
            cart[index]['quantity'] -= 1
            if cart[index]['quantity'] <= 0:
                cart.pop(index)
        elif action == "remove":
            cart.pop(index)

        request.session['cart'] = cart
        return JsonResponse({'status': 'ok'})