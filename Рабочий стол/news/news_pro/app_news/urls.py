from django.urls import path

from .views import NewsListView, NewsDetailView

urlpatterns = [
    path('news/', NewsListView.as_view({'get': 'list', 'post': 'create'})),
    path('news/<int:pk>/', NewsDetailView.as_view({'get': 'retrieve', 'delete': 'destroy', 'put': 'update'})),
]