from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path("employees/", views.EmployeesViewSet.as_view({'get': 'list'})),
    path("employees/<int:pk>/", views.EmployeesViewSet.as_view({'get': 'retrieve'})),
])
