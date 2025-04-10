import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict


class Storage(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Dict) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict = None) -> List[Dict]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Dict) -> None:
        pass


class JSONStorage(Storage):
    def __init__(self, filename: str = 'data/vacancies.json'):
        self.__filename = filename
        self.__ensure_directory_exists()

    def __ensure_directory_exists(self):
        """Создает папку data, если она не существует"""
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)

    def add_vacancy(self, vacancy: Dict) -> None:
        try:
            with open(self.__filename, 'a') as f:
                json.dump(vacancy, f, ensure_ascii=False)
                f.write('\n')
        except IOError as e:
            print(f"Ошибка при сохранении вакансии: {e}")

    def get_vacancies(self, criteria: Dict = None) -> List[Dict]:
        vacancies = []
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        vacancy = json.loads(line)
                        if self.__match_criteria(vacancy, criteria):
                            vacancies.append(vacancy)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        return vacancies

    def delete_vacancy(self, vacancy: Dict) -> None:
        vacancies = self.get_vacancies()
        try:
            with open(self.__filename, 'w', encoding='utf-8') as f:
                for v in vacancies:
                    if v['url'] != vacancy['url']:
                        json.dump(v, f, ensure_ascii=False)
                        f.write('\n')
        except IOError as e:
            print(f"Ошибка при удалении вакансии: {e}")

    def __match_criteria(self, vacancy: Dict, criteria: Dict) -> bool:
        if not criteria:
            return True

        for key, value in criteria.items():
            if key not in vacancy or str(value).lower() not in str(vacancy[key]).lower():
                return False
        return True
