from content.forms import SearchForm
from content.models import Category


class DataMixin:
    title_page = None
    def __init__(self):
        if self.title_page:
            self.extra_context = {'title': self.title_page}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class SearchMixin:

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['search_form'] = SearchForm
        return content


