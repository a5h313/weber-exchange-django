from django.shortcuts import render, get_object_or_404, redirect
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
    """Display a gallery of submitted feedback entries and highlight session favorites."""
    template_name = "landing/user-feedback-list.html"
    model = Feedback
    context_object_name = 'feedbacks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = self.request.session.get('favorites', [])
        return context


class UserFeedbackDetailView(DetailView):
    """Display the details of a single feedback entry and indicate favorite status."""
    template_name = "landing/user-feedback-detail.html"
    model = Feedback
    context_object_name = 'feedback'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = self.request.session.get('favorites', [])
        return context

def toggle_favorite(request: HttpRequest, feedback_id: int) -> HttpResponse:
    feedback = get_object_or_404(Feedback, id=feedback_id)
    favorites = request.session.get('favorites', [])

    if feedback_id in favorites:
        favorites.remove(feedback_id)
    else:
        favorites.append(feedback_id)

    request.session['favorites'] = favorites
    return redirect('feedback-detail', pk=feedback_id)

def thanks(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/thanks.html')

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/about.html')