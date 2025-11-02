from django.contrib import admin
from .models import Post, Comment, NewsletterSubscriber
from .fetch_news import fetch_from_news_api, fetch_from_rss

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'view_count')
    list_filter = ('category', 'published_at')
    search_fields = ('title', 'content')
    readonly_fields = ('view_count',)
    actions = ['import_from_api', 'import_from_rss']

    def import_from_api(self, request, queryset):
        count = fetch_from_news_api()
        self.message_user(request, f"Successfully imported {count} new posts from NewsAPI.")
    import_from_api.short_description = "Import latest news from NewsAPI"

    def import_from_rss(self, request, queryset):
        count = fetch_from_rss()
        self.message_user(request, f"Successfully imported {count} new posts from PunchNG RSS.")
    import_from_rss.short_description = "Import latest news from RSS"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'body')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at')
    search_fields = ('email', 'name')
