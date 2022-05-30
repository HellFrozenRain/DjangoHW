from django.views.generic import TemplateView
from datetime import datetime
from mainapp import models

class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'

class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["news_query_set"] = models.News.objects.all()
        return context