from abc import ABC, abstractmethod
import requests
from typing import List, Dict, Any


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def get_vacancies(self, keyword: str, city: str = None) -> List[Dict[str, Any]]:
        """Получить вакансии по ключевому слову и городу"""
        pass


class HeadHunterAPI(JobAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__areas_url = "https://api.hh.ru/areas"
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__cities_cache = {}

    def __connect(self) -> bool:
        """Проверка соединения с API"""
        try:
            response = requests.get(self.__base_url, headers=self.__headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def __get_city_id(self, city_name: str) -> int:
        """Получить ID города по названию"""
        if city_name in self.__cities_cache:
            return self.__cities_cache[city_name]

        try:
            response = requests.get(self.__areas_url, headers=self.__headers)
            response.raise_for_status()

            for country in response.json():
                for area in country['areas']:
                    if area['name'].lower() == city_name.lower():
                        self.__cities_cache[city_name] = area['id']
                        return area['id']
                    for sub_area in area['areas']:
                        if sub_area['name'].lower() == city_name.lower():
                            self.__cities_cache[city_name] = sub_area['id']
                            return sub_area['id']
        except requests.exceptions.RequestException:
            pass

        return 113  # Россия по умолчанию

    def get_vacancies(self, keyword: str, city: str = None) -> List[Dict[str, Any]]:
        """
        Получить вакансии по ключевому слову и городу

        Args:
            keyword: Ключевое слово для поиска
            city: Город для поиска (необязательно)

        Returns:
            Список вакансий в виде словарей
        """
        if not self.__connect():
            raise ConnectionError("Не удалось подключиться к API HeadHunter")

        params = {
            'text': keyword,
            'per_page': 100,
            'page': 0
        }

        if city:
            city_id = self.__get_city_id(city)
            params['area'] = city_id

        try:
            response = requests.get(self.__base_url, headers=self.__headers, params=params)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка при запросе к API: {e}")
