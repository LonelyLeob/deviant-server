import os
from django.db import models
from django.dispatch import receiver

def upload_to_girls(instance, filename):
    return f"girls/{instance.girl.nickname}/{filename}"

class Girl(models.Model):
    nickname = models.CharField("Псевдоним", max_length=50)
    additional_info = models.CharField("Добавочное описание", max_length=200)
    domain = models.CharField("Домен девушки", max_length=200)
    slug = models.SlugField("Ярлык для URL")

    def __str__(self) -> str:
        return self.nickname

    @property
    def links(self):
        return self.links_set.all()
    
    class Meta:
        verbose_name = 'Девочка'
        verbose_name_plural = 'Девочки'

class Avatar(models.Model):
    avatar = models.ImageField("Фото девочки", upload_to=upload_to_girls)
    girl = models.ForeignKey(Girl, verbose_name="Связь к девочке", on_delete=models.CASCADE, related_name="avatars")

    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'

@receiver(models.signals.post_delete, sender=Avatar)
def post_save_image(sender, instance, *args, **kwargs):
    try:
        instance.avatar.delete(save=False)
    except:
        pass

@receiver(models.signals.pre_save, sender=Avatar)
def pre_save_image(sender, instance, *args, **kwargs):
    print(instance)
    try:
        old_img = instance.__class__.objects.get(id=instance.id).avatar.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


class Link(models.Model):
    title = models.CharField("Название ссылки", max_length=200)
    girl = models.ForeignKey(Girl, on_delete=models.PROTECT, related_name="links", verbose_name="Девочка")
    link = models.URLField("Ссылка на источник", max_length=200)
    flag = models.BooleanField("Заглавная ссылка?", default=False)

    def __str__(self) -> str:
        return f"Ресурс для {self.girl.slug}"
    
    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'