from django.urls import path, include
from article import views

app_name = 'article'

urlpatterns = [
    # path('', views.ArticleList.as_view(), name='list'),
    # path('<int:pk>/', views.ArticleDetail.as_view(), name='detail'),
    # path('crsf/', views.get_csrf, name='crsf'),
]