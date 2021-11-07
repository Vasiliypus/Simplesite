from django.contrib import admin

from .models import * 


class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'rubric', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content',)   
    save_on_top = True

    

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)

admin.site.site_title = 'Админ-панель сайта объявлений'
admin.site.site_header = 'Админ-панель (сайта) объявлений'