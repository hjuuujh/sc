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
# """

from django.urls import path

from group import views

app_name = 'group'


urlpatterns = [
    path('joined/', views.IndexView.as_view(), name='group_list'), # 가입한 그룹 보기
    path('create/', views.group_create, name='group_create'),
    path('<int:pk>/', views.DetailView.as_view(), name='group_detail'),   #그룹 검색 후 그룹 상세보기
    path('mgr/', views.GroupCreateView.as_view(), name='group_mgr'),
    path('delete/<int:pk>/', views.group_delete, name='group_delete'),
    path('search_list/', views.index, name='search_list'),  # 그룹 검색
    path('page/<int:pk>', views.group_page, name='group_page'),
    path('join/list/', views.GroupJoinView.as_view(), name='group_join'),
    path('leave/<int:group_id>', views.group_leave, name='group_leave'),
    path('request/<int:group_id>', views.join_request, name='join_request'),
    path('join/request/', views.GroupJoinRequestView.as_view(), name='group_join_request'),
    path('approve/<int:user_id>/<int:group_id>/<int:approve>', views.approve_request, name='approve_request'),
]
