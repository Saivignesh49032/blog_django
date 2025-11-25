# blog/urls.py

from django.urls import path
from . import views 

app_name = 'blog' 

urlpatterns = [
    # R: List View (Index) - /
    path('', views.PostListView.as_view(), name='index'),

    # C: Create View - /new/
    path('new/', views.PostCreateView.as_view(), name='post_new'),

    # R: Detail View - /5/ (Uses the Function-Based View to handle comments)
    path('<int:pk>/', views.post_detail, name='detail'), 

    # U: Update View - /5/edit/
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),

    # D: Delete View - /5/delete/
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Like/Unlike Action
    path('<int:pk>/like/', views.post_like, name='post_like'),
    path('<int:pk>/clear-likes/', views.clear_likes, name='clear_likes'),
    
    # Category Filter
    path('category/<str:cats>/', views.category_view, name='category'),
]