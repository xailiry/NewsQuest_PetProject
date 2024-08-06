from django.contrib import admin

from newsfeed.models import Article


# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_short')
    search_fields = ('author_name', 'title', 'id')
    list_display_links = ('id', 'title')
    actions = ['duplicate_article']

    def content_short(self, obj: Article) -> str:
        if len(obj.content) < 48:
            return obj.content
        return obj.content[:48] + "..."

    def duplicate_article(self, request, queryset):
        for article in queryset:
            for _ in range(20):
                article.pk = None  # Reset the primary key to create a new instance
                article.save()
        self.message_user(request, "Selected articles have been duplicated 20 times each.")

    duplicate_article.short_description = "Duplicate selected articles 20 times"