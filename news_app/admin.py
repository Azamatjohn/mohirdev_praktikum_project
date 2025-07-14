from django.contrib import admin

# Register your models here.
from .models import News, Category, Contact, Comments

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'created_time', 'updated_time', "status")
    list_filter = ('category', 'status', 'published_date')
    search_fields = ('title', 'body',)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date', 'status')



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Contact)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['approve', 'reject']
    exclude = ['body']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def enable_comments(self, request, queryset):
        queryset.update(active=True)

