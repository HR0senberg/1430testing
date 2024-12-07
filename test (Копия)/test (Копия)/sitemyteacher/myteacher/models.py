from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Teacher(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    subject = models.CharField(max_length=100, verbose_name="Предмет")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='teachers_photos/', null=True, blank=True, verbose_name="Фото")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Слаг", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'slug': self.slug})

class Comment(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Учитель"
    )
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий к {self.teacher.full_name} ({self.created_at:%d-%m-%Y})"
