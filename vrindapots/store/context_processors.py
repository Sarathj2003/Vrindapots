from .models import Category

def categories_processor(request):
    categories = Category.objects.all()  # Fetch all categories from your Category model
    return {'categories': categories}