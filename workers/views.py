from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Employees
from .serializers import EmployeesListSerializer, EmployeesDetailSerializer, CompanySerializer
from .service import EmployeesFilter, PaginationEmployees
from .permissions import IsRocketDetailUser


class EmployeesViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод информации о сотрудниках"""
    queryset = Employees.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EmployeesFilter
    pagination_class = PaginationEmployees

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeesListSerializer
        elif self.action == "retrieve":
            return EmployeesDetailSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsRocketDetailUser]
        return [permission() for permission in permission_classes]
