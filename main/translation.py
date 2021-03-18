from modeltranslation.translator import translator, TranslationOptions

from .models import Post

class PostTranslationOption(TranslationOptions):
    fields = ('title', 'text')

translator.register(Post, PostTranslationOption)