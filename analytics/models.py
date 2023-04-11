from django.db import models

class Geo(models.Model):
    country = models.CharField("Страна", max_length=50)
    city = models.CharField("Город", max_length=50)
    ip = models.GenericIPAddressField("IP запроса", protocol="both", unpack_ipv4=False)

    def __str__(self) -> str:
        return f"Уникальный посетитель с ip {self.ip}"