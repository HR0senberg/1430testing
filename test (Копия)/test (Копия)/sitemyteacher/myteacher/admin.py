from django.contrib import admin
from .models import Teacher, Comment

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject', 'slug')
    prepopulated_fields = {'slug': ('full_name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'content', 'created_at')

"У этого учителя нет описания"