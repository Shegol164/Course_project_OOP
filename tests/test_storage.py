import unittest
from src.vacancy import Vacancy

class TestVacancy(unittest.TestCase):
    def setUp(self):
        self.vacancy1 = Vacancy(
            title='Python Developer',
            url='https://hh.ru/vacancy/1',
            salary=100000,
            description='Разработка веб-приложений',
            requirements='Опыт работы от 3 лет'
        )
        self.vacancy2 = Vacancy(
            title='Java Developer',
            url='https://hh.ru/vacancy/2',
            salary=120000,
            description='Разработка backend',
            requirements='Опыт работы от 5 лет'
        )
        self.vacancy_no_salary = Vacancy(
            title='Intern',
            url='https://hh.ru/vacancy/3',
            salary=None,
            description='Обучение',
            requirements='Без опыта'
        )

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy1.title, 'Python Developer')
        self.assertEqual(self.vacancy1.salary, 100000)
        self.assertEqual(self.vacancy_no_salary.salary, 0)

    def test_comparison_operators(self):
        self.assertTrue(self.vacancy1 < self.vacancy2)
        self.assertTrue(self.vacancy2 > self.vacancy1)
        self.assertTrue(self.vacancy1 != self.vacancy2)

    def test_to_dict(self):
        vacancy_dict = self.vacancy1.to_dict()
        self.assertEqual(vacancy_dict['title'], 'Python Developer')
        self.assertEqual(vacancy_dict['salary'], 100000)
        self.assertEqual(vacancy_dict['url'], 'https://hh.ru/vacancy/1')

    def test_str_representation(self):
        str_repr = str(self.vacancy1)
        self.assertIn('Python Developer', str_repr)
        self.assertIn('100000 руб.', str_repr)
        self.assertIn('https://hh.ru/vacancy/1', str_repr)

    def test_validation(self):
        invalid_vacancy = Vacancy(
            title=None,
            url='invalid_url',
            salary=-100,
            description=None,
            requirements=None
        )
        self.assertEqual(invalid_vacancy.title, 'Без названия')
        self.assertEqual(invalid_vacancy.url, '#')
        self.assertEqual(invalid_vacancy.salary, 0)

if __name__ == '__main__':
    unittest.main()