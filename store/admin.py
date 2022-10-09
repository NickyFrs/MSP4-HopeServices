from django.contrib import admin

from .models import Category, Product


# models from here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']  # will show what to show in the admin area
    prepopulated_fields = {'slug': ('name',)}
    ''' 
    will specify what field to 
    be prepopulated or populated base 
    on what is typed in this case the 
    slug of the field will be populated 
    when something isis typed in this 
    field in the name field
    '''


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'created_by', 'name', 'description',
                    'slug', 'price', 'active', 'created', 'updated', ]
    list_filter = ['category', 'name', 'description',
                   'slug', 'price', 'active', 'created', 'updated', ]
    list_editable = ['price', 'active', ]
    prepopulated_fields = {'slug': ('name',)}
