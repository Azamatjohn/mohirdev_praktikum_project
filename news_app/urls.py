from django.urls import path
from .views import news_list, news_detail, index, contact, LocalNewsView, ForeignNewsView, SportsNewsView, \
    SiyosatNewsView, TechnologyNewsView, \
    NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page, SearchResultsView

urlpatterns = [
    path('', index, name='home'),
    path('contact-us/', contact, name='contact_us'),
    path('news/', news_list, name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug:slug>', news_detail, name='news_detail_page'),
    path('news/<slug:slug>/update', NewsUpdateView.as_view(), name='news_update_page'),
    path('news/<slug:slug>/delete', NewsDeleteView.as_view(), name='news_delete_page'),
    path('siyosat/', SiyosatNewsView.as_view(), name='siyosat_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign_news_page'),
    path('sports/', SportsNewsView.as_view(), name='sports_news_page'),
    path('adminpage/', admin_page, name='admin_page'),
    path('searchresults/', SearchResultsView.as_view(), name='search_results'),

]