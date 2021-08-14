"""studycheck URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from board import views
from django.conf import settings
from django.conf.urls.static import static

app_name='board'
urlpatterns = [
    path('mgr/<int:pk>/', views.BoardListView.as_view(), name='board_list'),
    path('<int:group_id>/board/create/', views.board_create, name='board_create'),
    path('<int:group_id>/board/delete/<int:pk>/', views.board_delete, name='board_delete'),

    path('<int:group_id>/<int:pk>/', views.PostListView.as_view(), name='post_list'),
    path('<int:group_id>/<int:board_id>/post/create/', views.post_create, name='post_create'),
    path('<int:group_id>/<int:board_id>/post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:group_id>/<int:board_id>/post/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('<int:board_id>/post/modify/<int:pk>/', views.post_modify, name='post_modify'),

    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
