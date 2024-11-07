from .models import Category, Wishlist

def categories_processor(request):
    categories = Category.objects.filter(is_deleted=False)  
    return {'categories': categories}

def wishlist_processor(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_count': wishlist_count}
