from sitecompany.celery import app
from .models import Employees, SalaryInformation
from django.db.models import F


@app.task
def delete_salary(row):
    SalaryInformation.objects.filter(employee__id__in=row).delete()


@app.task
def payroll():
    for emp in Employees.objects.all():
        emp.salary = F('salary') + 10
        emp.save()
