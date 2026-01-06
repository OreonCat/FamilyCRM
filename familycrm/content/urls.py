from django.contrib import admin
from django.urls import path, include

from content import views

urlpatterns = [
    path('', views.ContentList.as_view(), name='index'),
    path('content/category/<slug:slug>', views.ContentListByCategory.as_view(), name='category'),
    path('content/<int:pk>', views.ContentDetail.as_view(), name='content-detail'),
    path('content/add', views.AddContent.as_view(), name='add-content'),
    path('content/edit/<int:pk>', views.EditContent.as_view(), name='edit-content'),
    path('content/delete/<int:pk>', views.DeleteContent.as_view(), name='delete-content'),
    path('content/comment/delete/<int:pk>', views.DeleteCommentContent.as_view(), name='delete-comment-content'),
]