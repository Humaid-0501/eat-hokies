from django.urls import path
from . import views
app_name = 'eatHokies'
urlpatterns = [
    # dining_list views
    path('', views.dining_home, name='dining_home'),
    path('add', views.dining_add_item, name='dining_add_item'),
    path('edit/<int:item_id>', views.edit_item, name='edit_item'),
    path('list', views.dining_list, name='dining_list'),
    path('list/add', views.create_item, name='create_item'),
    path('list/edited/<int:item_id>', views.edit, name='edit'),
    path('list/<int:restaurant_id>', views.dining_list, name='dining_list'),
    path('list/sort/<int:restaurant_id>', views.dining_sort, name='dining_sort'),
    path('<int:item_id>', views.dining_details, name='dining_details'),
    path('item/plus', views.item_quantity_plus, name='item_quantity_plus'),
    path('item/minus', views.item_quantity_minus, name='item_quantity_minus'),
    path('delete/<int:item_id>', views.delete_item, name='delete_item'),
    path('list/delete', views.delete, name='delete'),
    path('comment/<int:item_id>', views.comment, name='comment'),
    path('comment/view/<int:item_id>', views.view_comment, name='view_comment'),
    path('comment/edit', views.edit_comment, name='edit_comment'),
    path('comment/delete', views.delete_comment, name='delete_comment'),
]