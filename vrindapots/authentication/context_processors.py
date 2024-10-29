from django.contrib.auth.models import User

def users_processor(request):
    users = User.objects.all()  
    return {'users': users}