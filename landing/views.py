from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect

from .forms import FeedbackForm
from .models import Product

# Create your views here.
def landing(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by('postedAt')
    return render(request, 'landing/home.html', {
        'products': products
    })

def detail(request: HttpRequest, slug) -> HttpResponse:
    try:
        product = Product.objects.get(slug=slug)
    except:
        raise Http404
    return render(request, 'landing/detail.html', {
        'product': product,
        'title': product.title,
        'price': product.price,
        'category': product.category,
        'condition': product.condition,
        'location': product.location,
        'available': product.available,
        'postedAt': product.postedAt,
        'seller': product.seller,
        'image': product.image,
        'description': product.description,
    })

def contact(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = FeedbackForm()

    return render(request, 'landing/contact.html', {
        'form': form
    })

def thanks(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/thanks.html')

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/about.html')