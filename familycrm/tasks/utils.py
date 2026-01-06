from .models import Task

class DataMixin:
    title_page = None
    def __init__(self):
        if self.title_page:
            self.extra_context = {'title': self.title_page}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Task.Status.choices
        return context