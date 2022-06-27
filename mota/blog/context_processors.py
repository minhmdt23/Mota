from .models import Category

def category_processor(request):
    category = Category.objects.all()
    category_active = ''
    search_text = ''
    if request.method == 'GET':
        if request.GET.get('category'):
            category_active = int(request.GET.get('category'))
        if request.GET.get('search'):
            search_text = request.GET.get('search')
    return {
        'categorys': category,
        'category_active': category_active,
        'search_text': search_text,
    }