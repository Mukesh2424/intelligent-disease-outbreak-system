from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),          # login page
    path('signup/', views.signup_view, name='signup'), # signup page
    path('logout/', views.logout_view, name='logout'), # logout
    # Protected pages
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/', views.export_data, name='export_data'),
    path('api/outbreaks/', views.outbreak_data_api, name='outbreak_data_api'),
]
