from rest_framework import serializers
from .models import Employees, CompanyStructure


class CompanySerializer(serializers.ModelSerializer):
    """Структура компании"""

    class Meta:
        model = CompanyStructure
        fields = '__all__'


class EmployeesListSerializer(serializers.ModelSerializer):
    """Список сотрудников"""
    level = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Employees
        fields = ['fullname', 'position', 'level']


class EmployeesDetailSerializer(serializers.ModelSerializer):
    """Информация об отдельном сотруднике"""
    manager = serializers.SlugRelatedField(slug_field="name", read_only=True)
    level = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Employees
        fields = '__all__'
