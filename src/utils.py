from typing import List
from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """Фильтровать вакансии по ключевым словам (исключая цифры)"""
    if not keywords:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        for keyword in keywords:
            if keyword.isdigit():
                continue  # Цифры обрабатываем отдельно
            if (keyword.lower() in vacancy.title.lower() or
                    keyword.lower() in vacancy.description.lower() or
                    keyword.lower() in vacancy.requirements.lower()):
                filtered.append(vacancy)
                break
    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировать вакансии по зарплате (по убыванию)"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получить топ N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывести вакансии в консоль"""
    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. {vacancy}")
        print("-" * 50)
