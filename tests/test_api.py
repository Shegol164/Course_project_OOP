import unittest
from unittest.mock import patch, Mock
from src.api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self):
        self.api = HeadHunterAPI()
        self.mock_response = {
            'items': [
                {
                    'name': 'Python Developer',
                    'alternate_url': 'https://hh.ru/vacancy/1',
                    'salary': {'from': 100000},
                    'snippet': {
                        'requirement': 'Опыт работы от 3 лет',
                        'responsibility': 'Разработка ПО'
                    }
                }
            ]
        }

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: self.mock_response
        )

        vacancies = self.api.get_vacancies('Python')
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Python Developer')

    @patch('requests.get')
    def test_get_vacancies_with_city(self, mock_get):
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: self.mock_response
        )

        vacancies = self.api.get_vacancies('Python', 'Москва')
        self.assertEqual(len(vacancies), 1)

    @patch('requests.get')
    def test_get_vacancies_failure(self, mock_get):
        mock_get.return_value = Mock(
            status_code=400,
            json=lambda: {'errors': ['Bad request']}
        )

        with self.assertRaises(ConnectionError):
            self.api.get_vacancies('Python')

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = ConnectionError("API недоступен")

        with self.assertRaises(ConnectionError):
            self.api.get_vacancies('Python')


if __name__ == '__main__':
    unittest.main()