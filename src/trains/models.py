from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Номер поезда')
    travel_time = models.PositiveSmallIntegerField(verbose_name='Время в пути')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city_set', verbose_name='из')
    to_city = models.ForeignKey('cities.City', on_delete=models.CASCADE, related_name='to_city_set', verbose_name='до')

    def __str__(self):
        return f'Поезд № {self.name}, {self.from_city} - {self.to_city}'
    
    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError('Измените город прибытия')
        qs = Train.objects.filter(from_city=self.from_city, to_city=self.to_city, 
                                  travel_time=self.travel_time).exclude(pk=self.id)
        # Trian == self.__class__
        if qs.exists():
            raise ValidationError('Нужно изменить время в пути')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('trains:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']