from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from cities.models import City
from cities.forms import HtmlForm, CityForm


def home(request, pk=None):

    '''
    if pk:
        #city = City.objects.filter(id=pk).first()
        city = get_object_or_404(City, id=pk)
        context = {'object': city}
        return render(request, 'cities/detail.html', context)
    '''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()

    form = CityForm()

    qs = City.objects.all()

    # пагинация
    lst = Paginator(qs, 2)
    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)

    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'cities/home.html', context)


class CityListView(ListView):
    paginate_by = 2
    model = City
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CityForm()
        return context


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно добавлен'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_message = 'Город успешно обновлен'


class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    #template_name = 'cities/delete.html' # удаление с подтверждением
    success_url = reverse_lazy('cities:home')

    # удаление без подтверждения
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Город успешно удалён')
        return self.post(request, *args, **kwargs)