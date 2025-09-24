from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Product, CartItem, Order, OrderItem
import uuid
from decimal import Decimal

# Create your views here.

def product_list(request, category_slug=None):
    """Display all products or products in a specific category"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'store/product/list.html', context)


def product_detail(request, product_slug):
    """Display a single product's details"""
    product = get_object_or_404(Product, slug=product_slug, available=True)
    context = {
        'product': product,
        'categories': Category.objects.all()
    }
    return render(request, 'store/product/detail.html', context)


def get_cart_items(request):
    """Helper function to get cart items for current user/session"""
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        return CartItem.objects.filter(session_id=session_key)


def cart_detail(request):
    """Display cart contents"""
    cart_items = get_cart_items(request)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'categories': Category.objects.all()
    }
    return render(request, 'store/cart/detail.html', context)


@require_POST
def cart_add(request, product_id):
    """Add a product to cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f'Sorry, only {product.stock} items available in stock.')
        return redirect('store:product_detail', product_slug=product.slug)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
                messages.warning(request, f'Quantity adjusted to available stock ({product.stock})')
            cart_item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
            
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_key,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
                messages.warning(request, f'Quantity adjusted to available stock ({product.stock})')
            cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('store:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove a product from cart"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user, product=product).delete()
    else:
        session_key = request.session.session_key
        if session_key:
            CartItem.objects.filter(session_id=session_key, product=product).delete()
    
    messages.success(request, f'{product.name} removed from cart!')
    return redirect('store:cart_detail')


@require_POST
def cart_update(request):
    """Update cart quantities via AJAX"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        
        if quantity > product.stock:
            return JsonResponse({'error': f'Only {product.stock} items available'})
        
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, user=request.user, product=product)
        else:
            session_key = request.session.session_key
            cart_item = get_object_or_404(CartItem, session_id=session_key, product=product)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            item_total = cart_item.get_total_price()
        else:
            cart_item.delete()
            item_total = 0
        
        # Calculate new cart total
        cart_items = get_cart_items(request)
        cart_total = sum(item.get_total_price() for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'item_total': float(item_total),
            'cart_total': float(cart_total)
        })
    
    return redirect('store:cart_detail')


@login_required
def checkout(request):
    """Checkout process"""
    cart_items = get_cart_items(request)
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('store:cart_detail')
    
    if request.method == 'POST':
        # Create order
        total = sum(item.get_total_price() for item in cart_items)
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            user=request.user,
            order_id=order_id,
            total=total,
            shipping_address=request.POST.get('address', ''),
            shipping_city=request.POST.get('city', ''),
            shipping_zip=request.POST.get('zip_code', ''),
        )
        
        # Create order items and update stock
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order {order_id} placed successfully!')
        return redirect('store:order_detail', order_id=order_id)
    
    total = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total': total,
        'categories': Category.objects.all()
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    context = {
        'order': order,
        'categories': Category.objects.all()
    }
    return render(request, 'store/order/detail.html', context)


@login_required
def order_list(request):
    """Display user's order history"""
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders,
        'categories': Category.objects.all()
    }
    return render(request, 'store/order/list.html', context)


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Merge session cart with user cart
            session_key = request.session.session_key
            if session_key:
                session_cart_items = CartItem.objects.filter(session_id=session_key)
                for session_item in session_cart_items:
                    user_cart_item, created = CartItem.objects.get_or_create(
                        user=user,
                        product=session_item.product,
                        defaults={'quantity': session_item.quantity}
                    )
                    if not created:
                        user_cart_item.quantity += session_item.quantity
                        user_cart_item.save()
                    session_item.delete()
            
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('store:product_list')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all()
    }
    return render(request, 'registration/register.html', context)
