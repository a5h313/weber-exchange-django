from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView

from .forms import FeedbackForm
from .models import Product, Feedback


# Create your views here.
def landing(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all().order_by('postedAt')[:5]
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
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = FeedbackForm()

    return render(request, 'landing/contact.html', {
        'form': form
    })

class UserFeedbackListView(ListView):
    template_name = "landing/user-feedback-list.html"
    model = Feedback
    context_object_name = 'feedbacks'

class UserFeedbackDetailView(DetailView):
    template_name = "landing/user-feedback-detail.html"
    model = Feedback
    context_object_name = 'feedback'

def toggle_favorite(request: HttpRequest, post_id) -> HttpResponse:
    favorites = request.session.get('favorites', [])

    if post_id in favorites:
        favorites.remove(post_id)
    else:
        favorites.append(post_id)

    request.session['favorites'] = favorites

def thanks(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/thanks.html')

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/about.html')