from django.contrib import admin
from .models import CompanyStructure, Employees, SalaryInformation
# from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe
from workers.tasks import delete_salary


@admin.register(CompanyStructure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ("name", "level_number",)
    list_display_links = ("name",)
    save_on_top = True


# @admin.register(CompanyStructure)
# class StructureParentAdmin(DraggableMPTTAdmin):
#     list_display = ('tree_actions', 'indented_title')
#     list_display_links = ('indented_title',)
#     save_on_top = True


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = (
        "fullname", "position", "salary", "get_sum_salary", "get_manager",)
    list_display_links = ("fullname",)
    list_filter = ("position", "level__level_number",)
    readonly_fields = ("employment_date",)
    save_on_top = True
    actions = ['delete_paid_out', ]

    def get_manager(self, obj):
        return mark_safe(f'<a href="{obj.manager_id}">рук-ль</a>')

    get_manager.short_description = "Руководитель"

    def delete_paid_out(self, request, queryset):
        """ Удалить информацию о заработной плате выбраных сотрудников """
        if queryset.count() > 20:
            delete_paid = list(queryset.values_list('id', flat=True))
            delete_salary.delay(delete_paid)
        else:
            SalaryInformation.objects.filter(employee__in=queryset).delete()

    delete_paid_out.short_description = "Удалить информацию о заработной плате выбраных сотрудников"
    delete_paid_out.allowed_permissions = ('change',)


@admin.register(SalaryInformation)
class PaidSalary(admin.ModelAdmin):
    list_display = ('employee', 'paid_out', 'date_paid')
    list_display_links = ('paid_out',)
    save_on_top = True


admin.site.site_title = 'Сотрудники'
admin.site.site_header = 'Сотрудники'
