from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category')
    search_fields = ('name', 'year')
    list_filter = ('category',)
    list_display_links = ('name',)
    empty_value_display = '-пусто-'
    # filter_horizontal = ('genre',)


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        TitleInline,
    )
    list_display = (
        'name',
    )


admin.site.register(Title, ReviewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
