from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from .forms import EbookForm
from .models import *

# Create your views here.
def ebookList(request):
    ebooks = Ebook.objects.all()
    return render(request, "ebooks.html", {"ebooks": ebooks, 'title': 'Ebooks'})


class EbooksAdd(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model=Ebook
    fields='__all__'
    template_name = 'ebooks_add.html'
    success_url = reverse_lazy('ebooks:ebook_admin_list')
    success_message = "New Ebook added successfully"

    def get_context_data(self, **kwargs):
        data = super(EbooksAdd, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = EbookForm(self.request.POST)
        else:
            data['items'] = EbookForm()
            data['title'] = 'Ebooks'
            
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form=context['form']
        if form.is_valid():
            form.save()
        return super(EbooksAdd, self).form_valid(form)


class EbookUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ebook
    template_name = 'ebooks_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('ebooks:ebook_admin_list')
    success_message = "Updated Successfully"
    
    def get_context_data(self, **kwargs):
        data = super(EbookUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = EbookForm(self.request.POST)
        else:
            data['items'] = EbookForm()
            data['title'] = 'Ebooks'
        return data

class EbookDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ebook
    template_name = 'modal/confirm_delete.html'
    success_url = reverse_lazy('ebooks:ebook_admin_list')
    
    def get_context_data(self, **kwargs):
        data = super(EbookDelete, self).get_context_data(**kwargs)
        data['title'] = 'Ebooks'
        return data
