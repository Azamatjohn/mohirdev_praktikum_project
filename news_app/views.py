from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import News, Category
from .forms import ContactForm
# Create your views here.

def news_list(request):
    news = News.published.all()
    context = {'news_list': news}
    return render(request, "news/news_list.html", context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    recent_news = News.published.exclude(id=news.id).order_by('-published_date')[:5]
    categories = Category.objects.all()

    context = {
        'news': news,
        'recent_news': recent_news,
        'categories': categories
    }
    return render(request, "news/news_detail.html", context)


def index(request):
    news_list = News.published.all().order_by('-published_date')[:6]
    popular = News.published.all().order_by('-published_date')[:3]
    recent_views = News.published.all().order_by('-published_date')[:3]
    categories = Category.objects.all()
    context = {'news_list': news_list,
               'categories': categories,
               'popular': popular,
               'recent_views': recent_views,
               }

    return render(request, 'news/tech-index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/tech-contact.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['categories'] = self.model.objects.all()
        context['news_list'] = News.published.all().order_by('-published_date')[:4]
        context['recent_views'] = News.published.all().order_by('-published_date')[:3]
        context['technology'] = News.published.all().filter(category__name='technology')
        return context



def contact(request):
    print(request.POST)
    if request.method == 'POST':
        form = ContactForm(request.POST)
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse('<h2> Thank you for contacting us! </h2>')
    context = {
        'form': form
    }
    return render(request, 'news/tech-contact.html', context)

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'local_news'
    def get_queryset(self):
        return News.published.all().filter(category__name='local')

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign.html'
    context_object_name = 'foreign_news'
    def get_queryset(self):
        return News.published.all().filter(category__name='foreign news')

class SportsNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sports'
    def get_queryset(self):
        return News.published.all().filter(category__name='sport')

class SiyosatNewsView(ListView):
    model = News
    template_name = 'news/siyosat.html'
    context_object_name = 'siyosat'
    def get_queryset(self):
        return News.published.all().filter(category__name='siyosat')


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'technology'
    def get_queryset(self):
        return News.published.all().filter(category__name='technology')





