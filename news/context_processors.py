from .models import Post

def categories_processor(request):
    """Makes the list of categories available to all templates."""
    categories = Post.objects.values_list('category', flat=True).distinct().order_by('category')
    return {'categories': categories}