from .models import Category

def get_categories(request):
    return {'categories': Category.objects.filter(is_active=True).all()}