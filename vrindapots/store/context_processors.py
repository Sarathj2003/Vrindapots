from .models import Category

def categories_processor(request):
    categories = Category.objects.filter(is_deleted=False)  # Fetch all categories from your Category model
    return {'categories': categories}