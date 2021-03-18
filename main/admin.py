from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from main.models import *

class PostImageInLine(admin.TabularInline):
    model = Image
    max_num = 18
    min_num = 1

@admin.register(Post)
class PostAdmin(TranslationAdmin):
    inlines = [PostImageInLine, ]
    list_display = ('title', )


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Rating)
