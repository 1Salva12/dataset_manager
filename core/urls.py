from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dataset/<int:dataset_id>/', views.dataset_detail, name='dataset_detail'),
    path('notebook/<int:notebook_id>/', views.notebook_detail, name='notebook_detail'),
    # Esta es la línea que soluciona el error "NoReverseMatch"
    path('notebook/delete/<int:notebook_id>/', views.delete_notebook, name='delete_notebook'),
]