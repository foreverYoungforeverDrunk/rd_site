from django.core.management.base import BaseCommand
import faker
from django_seed import Seed

from workers.models import CompanyStructure, Employees, SalaryInformation


class Command(BaseCommand):
    help = 'Заполнение БД тестовыми данными'

    def handle(self, *args, **options):
        fake = faker.Faker('ru_RU')
        seeder = Seed.seeder('ru_RU')

        if CompanyStructure.objects.count() < 5:
            y = (i for i in range(1, 6))
            seeder.add_entity(CompanyStructure, 5,
                              {
                                  'name': lambda x: fake.word(
                                      ext_word_list=('отдел', 'отделение', 'управление', 'цех', 'служба')),
                                  'level_number': lambda x: next(y),
                              }
                              )

        seeder.add_entity(Employees, 10, {
            'fullname': lambda x: fake.name(),
            'position': lambda x: fake.job(),
            'employment_date': lambda x: fake.date(),
            'salary': lambda x: fake.pydecimal(positive=True, right_digits=2, max_value=2000),
            'manager': lambda x: Employees.objects.last(),
            'level': lambda x: CompanyStructure.objects.order_by("?")[0],
            'email': lambda x: fake.unique.email(),
        })

        seeder.add_entity(SalaryInformation, 100, {
            'employee': lambda x: Employees.objects.order_by("?")[0],
            'paid_out': lambda x: fake.pydecimal(positive=True, right_digits=2, max_value=2000),
            'date_paid': lambda x: fake.date(),

        })
        seeder.execute()
