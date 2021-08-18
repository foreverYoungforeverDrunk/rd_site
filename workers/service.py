from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Employees


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class EmployeesFilter(filters.FilterSet):
    level = CharFilterInFilter(field_name='level__name', lookup_expr='in')
    position = CharFilterInFilter(lookup_expr='in')
    manager = CharFilterInFilter(lookup_expr='in')

    class Meta:
        model = Employees
        fields = ['level', 'position', 'manager']


class PaginationEmployees(PageNumberPagination):
    page_size = 4
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
