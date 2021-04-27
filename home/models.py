from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from news.models import PostPage,BlogIndexPage

class HomePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    def latest_news(self):
        try:
            latest_blog = BlogIndexPage.objects.get(slug='latest-news')
            return PostPage.objects.descendant_of(latest_blog).live().order_by('-date')[0:4]
        except models.Model.DoesNotExist as e:
            print(e)
            return []

    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request, *args, **kwargs)
        context['latest_news'] = self.latest_news()
        return context
