from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin


from trains.models import Train
from trains.forms import TrainForm


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно добавлен'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_message = 'Поезд успешно обновлен'


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    #template_name = 'trains/delete.html' # удаление с подтверждением
    success_url = reverse_lazy('trains:home')

    # удаление без подтверждения
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удалён')
        return self.post(request, *args, **kwargs)
