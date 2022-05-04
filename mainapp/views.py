from django.views.generic import TemplateView
from datetime import datetime

class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'

class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

class LoginView(TemplateView):
    template_name = 'mainapp/login.html'

class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['object_list'] = [
            {
                'title': 'Интервью с успешным студентом',
                'preview': 'ОБМАН',
                'date': datetime.now(),
            },    {
                'title': 'Высокое качество обучения',
                'preview': 'ЛОЖЬ',
                'date': datetime.now(),
            },    {
                'title': 'Гарантия трудоустройства',
                'preview': 'ВРАНЬЁ',
                'date': datetime.now(),
            },    {
                'title': 'Программа для новичков',
                'preview': 'ЧЕПУХА',
                'date': datetime.now(),
            },    {
                'title': 'ИНТЕНСИВ В ПАВЛОМ ВОЛЕЙ',
                'preview': 'БРЕД',
                'date': datetime.now(),
            },
        ]

        return context