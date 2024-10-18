from django.contrib.auth.models import User

def users_processor(request):
    users = User.objects.all()  # Fetch all categories from your Category model
    return {'users': users}