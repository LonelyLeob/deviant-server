from django.db import models
from django.utils import timezone

class Guest(models.Model):
    ip = models.GenericIPAddressField("IP пользователя", protocol="both", unpack_ipv4=False)
    visited_at = models.DateTimeField("Дата захода", default=timezone.now)

    def __str__(self) -> str:
        return str(self.ip)
    
    class Meta:
        verbose_name = 'Уникальный посетитель'
        verbose_name_plural = 'Уникальные посетители'

class GeoCounter(models.Model):
    country = models.CharField("Страна", max_length=50)
    requests_counter = models.IntegerField("Кол-во запросов", default=1)

    def __str__(self) -> str:
        return 

class Source(models.Model):
    name = models.CharField("Название источника", max_length=50)
    shortcut = models.CharField("Сокращение", max_length=10)
    description = models.CharField("Дескриптор", max_length=50)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"


class Mark(models.Model):
    app = models.ForeignKey(Source, verbose_name="Название источника", on_delete=models.CASCADE, related_name="marks")
    requests_counter = models.IntegerField("Кол-во запросов", default=1)

    def __str__(self) -> str:
        return f"Метка от источника {self.app}"

    class Meta:
        verbose_name = "Данные по источникам"
        verbose_name_plural = "Данные по источникам"
