from django.urls import path
from .views import *

app_name="ebooks"

urlpatterns = [
    path('all-ebooks', ebookList, name='ebook_admin_list'),
    path('add/',EbooksAdd.as_view(),name='ebook_add'),
    path('edit/<int:pk>',EbookUpdate.as_view(),name='ebook_edit'),
   path('delete/<int:pk>',EbookDelete.as_view(),name='ebook_delete'),
]