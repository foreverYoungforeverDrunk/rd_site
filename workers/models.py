from django.db import models
from django.db.models import Sum, CheckConstraint, Q
# from mptt.models import MPTTModel, TreeForeignKey


# class CompanyStructure(MPTTModel):
#     """ Структура компании """
#     name = models.CharField('структурная единица', max_length=150)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="уровень",
#                             related_name='children')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         constraints = [
#             CheckConstraint(
#                 check=Q(level__lt=5),
#                 name='level_lt_5'
#             )
#         ]
#         verbose_name = 'Cтруктура компании'
#         verbose_name_plural = 'Cтруктура компании'

class CompanyStructure(models.Model):
    """ Структура компании """
    name = models.CharField('структурная единица', max_length=150)
    level_number = models.IntegerField('уровень')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(level_number__lt=6),
                name='level_lt_5'
            )
        ]
        verbose_name = 'Cтруктура компании'
        verbose_name_plural = 'Cтруктура компании'


class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            get_sum_salary=Sum('paid__paid_out')
        )


class Employees(models.Model):
    """ Сотрудники """
    objects = CustomManager()
    fullname = models.CharField('ФИО', max_length=150)
    position = models.CharField('Должность', max_length=150)
    employment_date = models.DateField('Дата приема на работу', auto_now=True)
    salary = models.DecimalField('Начислено з/п', max_digits=12, decimal_places=2)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, )
    level = models.ForeignKey(CompanyStructure, on_delete=models.CASCADE, null=True, )
    email = models.EmailField('электроная почта', max_length=150)

    # def get_sum_salary(self):
    #     sum = self.paid.aggregate(sum_sal=Sum('paid_out'))
    #     return sum['sum_sal']

    def get_sum_salary(self):
        return self.get_sum_salary

    get_sum_salary.short_description = ('Всего выплачено')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['fullname']


class SalaryInformation(models.Model):
    """ Информация о заработной плате """
    employee = models.ForeignKey(Employees, verbose_name='Сотрудник', on_delete=models.CASCADE, related_name="paid")
    paid_out = models.DecimalField('Выплачено', max_digits=12, decimal_places=2)
    date_paid = models.DateField('Дата выплаты')

    class Meta:
        verbose_name = 'Заработная плата'
        verbose_name_plural = 'Заработная плата'
