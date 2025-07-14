from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView

from news_project.custom_permissions import OnlyLoggedSuperUser
from .models import News, Category
from .forms import ContactForm, CommentForm


# Create your views here.

def news_list(request):
    news = News.published.all()
    context = {'news_list': news,}
    return render(request, "news/news_list.html", context)




def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)

    # Hit count logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcount_response = HitCountMixin.hit_count(request, hit_count)
    if hitcount_response.hit_counted:
        hits += 1

    # Comments
    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()  # clear form after submit
    else:
        comment_form = CommentForm()

    # Other data
    recent_news = News.published.exclude(id=news.id).order_by('-published_date')[:5]
    categories = Category.objects.all()

    # Final context
    context = {
        'news': news,
        'recent_news': recent_news,
        'categories': categories,
        'comment_form': comment_form,
        'comments': comments,
        'comments_count': comments_count,
        'new_comment': new_comment,
        'hitcount': {
            'pk': hit_count.pk,
            'total_hits': hits,
            'hit_message': hitcount_response.hit_message
        }
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


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    template_name = 'crud/news_update.html'
    fields = ['title', 'body', 'image', 'category', 'status',]
    permission_required = 'news_app.change'
    def get_success_url(self):
        return reverse_lazy('news_app:news_list', kwargs={'slug': self.kwargs['slug']})


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('news_app:news_list')
    permission_required = 'news_app.can_delete_news'


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title', 'slug', 'body', 'image', 'category', 'status',]
    permission_required = 'news_app.can_create_news'

@login_required
def admin_page(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {'admin_users': admin_users,}
    return render(request, 'pages/admin_page.html', context)

class SearchResultsView(ListView):
    model = News
    template_name = "news/search_result.html"
    context_object_name = 'search_results'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        return context









