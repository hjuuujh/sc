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

from cal import views

app_name = 'cal'


urlpatterns = [
    path('<int:pk>/', views.CalendarView.as_view(), name='calendar'),
    path('<int:pk>/event/new/', views.event_new, name='event_new'),
    path('event/edit/<int:event_id>', views.event_edit, name='event_edit'),
]