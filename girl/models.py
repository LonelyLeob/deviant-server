from django.db import models

def upload_to_girls(instance, filename):
    return f"girls/{instance.nickname}/{filename}"

class Girl(models.Model):
    avatar = models.ImageField("Фото девочки", upload_to=upload_to_girls)
    nickname = models.CharField("Псевдоним", max_length=50)
    additional_info = models.CharField("Добавочное описание", max_length=200)
    slug = models.SlugField("Ярлык для URL")

    def __str__(self) -> str:
        return self.nickname
    
    class Meta:
        verbose_name = 'Девочка'
        verbose_name_plural = 'Девочки'

def upload_to_logos(_, filename):
    return f"logos/{filename}"

class Link(models.Model):
    title = models.CharField("Название ссылки", max_length=200)
    girl = models.ForeignKey(Girl, on_delete=models.PROTECT, related_name="links", verbose_name="Девочка")
    link = models.URLField("Ссылка на источник", max_length=200)
    pic = models.ImageField("Лого источника", upload_to=upload_to_logos)

    def __str__(self) -> str:
        return f"Ресурс для {self.girl.slug}"
    
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'