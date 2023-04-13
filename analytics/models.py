from django.db import models

class Geo(models.Model):
    country = models.CharField("Страна", max_length=50)
    city = models.CharField("Город", max_length=50)
    ip = models.GenericIPAddressField("IP запроса", protocol="both", unpack_ipv4=False)

    def __str__(self) -> str:
        return f"Уникальный посетитель с ip {self.ip}"
    
    class Meta:
        verbose_name = "Данные по гео"
        verbose_name_plural = "Данные по гео"
    
class Source(models.Model):
    name = models.CharField("Название источника", max_length=50)
    description = models.CharField("Дескриптор", max_length=50)

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"

class Mark(models.Model):
    app=models.ForeignKey(Source, verbose_name="Название источника", on_delete=models.CASCADE, related_name="marks")

    class Meta:
        verbose_name = "Данные по источникам"
        verbose_name_plural = "Данные по источникам"