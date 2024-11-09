from .models import Category, Wishlist, Cart, CartItem


def categories_processor(request):
    categories = Category.objects.filter(is_deleted=False)  
    return {'categories': categories}

def wishlist_processor(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': wishlist_count}

def cart_item_count(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item_count = CartItem.objects.filter(cart=cart).count()
    return {'cart_item_count': item_count}