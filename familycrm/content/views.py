from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.shortcuts import redirect, get_object_or_404
from django.template.defaultfilters import lower
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from content.forms import EditContentForm, CommentForm
from content.models import Content, Category, Comment
from content.utils import DataMixin, SearchMixin


class ContentList(DataMixin, SearchMixin, ListView):
    model = Content
    context_object_name = 'contents'
    paginate_by = 9
    template_name = 'content/index.html'
    title_page = "Наш контент"

    def get_queryset(self):
        if not self.request.GET.get('search'):
            return Content.objects.all()
        else:
            return Content.objects.filter(name__icontains=lower(self.request.GET.get('search')))


class ContentListByCategory(DataMixin, SearchMixin, ListView):
    model = Content
    context_object_name = 'contents'
    paginate_by = 10
    template_name = 'content/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = category.name
        return context

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        if not self.request.GET.get('search'):
            queryset = Content.objects.filter(category=category)
        else:
            queryset = Content.objects.filter(category=category, name__icontains=lower(self.request.GET.get('search')))
        return queryset

class ContentDetail(DataMixin, DetailView):
    model = Content
    context_object_name = 'content'
    template_name = 'content/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['for_comment_object'] = self.object
        context['comments'] = self.object.comments.all()

        edited_comment_id = self.request.GET.get('edit_comment')


        if edited_comment_id:
            comment = get_object_or_404(Comment, id=edited_comment_id)
            context['edit_comment_id'] = edited_comment_id
            if comment.can_edit(self.request.user, self.object):
                context['comment_form'] = CommentForm(instance=comment)
            else:
                context['comment_form'] = CommentForm()
        else:
            context['comment_form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if 'edit_comment_id' in context:
            edited_comment_id = context['edit_comment_id']
            comment = get_object_or_404(Comment, id=edited_comment_id)
            if comment.can_edit(self.request.user, self.object):
                form = CommentForm(request.POST, instance=comment)
                if form.is_valid():
                    comment.message = form.cleaned_data['message']
                    comment.save()
                    return redirect(reverse_lazy('content-detail', kwargs={'pk': self.object.pk}))
            else:
                return redirect(reverse_lazy('content-detail', kwargs={'pk': self.object.pk}))
        else:
            self.object = self.get_object()
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.content = self.object
                comment.save()
                return redirect(reverse_lazy('content-detail', kwargs={'pk': self.object.pk}))

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

class AddContent(LoginRequiredMixin, DataMixin, CreateView):
    model = Content
    context_object_name = 'content'
    fields = ('name', 'category', 'picture')
    template_name = 'content/add_content.html'
    title_page = "Добавить контент"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = Content.Status.NOT_STARTED
        form.instance.rating = 0
        form.instance.name = lower(form.instance.name)
        form.save()
        return super().form_valid(form)

class EditContent(LoginRequiredMixin, DataMixin, UpdateView):
    model = Content
    context_object_name = 'content'
    form_class = EditContentForm
    template_name = 'content/edit_content.html'
    title_page = "Редактировать"

    def form_valid(self, form):
        form.instance.name = lower(form.instance.name)
        form.save()
        return super().form_valid(form)

class DeleteContent(LoginRequiredMixin, DataMixin, DeleteView):
    model = Content
    template_name = 'content/delete_content.html'
    success_url = reverse_lazy('index')
    title_page = 'Удалить'

class DeleteCommentContent(LoginRequiredMixin, DataMixin, DeleteView):
    model = Comment
    template_name = 'content/delete_comment_content.html'
    success_url = reverse_lazy('index')
    title_page = "Удалить коммент"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.object.content
        return context

    def get_success_url(self):
        context = self.get_context_data()
        return reverse_lazy('content-detail', kwargs={'pk': context['content'].id})

