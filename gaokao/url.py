from django.urls import path

from . import views

app_name = 'gaokao'
urlpatterns = [
    # ex: /polls/
    path('listmeta', views.listmeta, name='listmeta'),
    path('list', views.list, name='list'),
    path('detail', views.detail, name='detail'),
    path('recommend', views.recommend, name='recommend'),
    path('searchlist', views.searchlist, name='searchlist'),
    path('majorlist', views.major_list, name='majorlist'),

    # ex: /polls/5/
    # path('<str:school_id>/', views.detail, name='detail'),
]
