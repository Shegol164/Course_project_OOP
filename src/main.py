from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.storage import JSONStorage
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies, print_vacancies


def user_interaction():
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    print("=== Поиск вакансий на HeadHunter ===")
    keyword = input("Введите профессию: ").strip()
    if not keyword:
        print("Ошибка: Профессия не может быть пустой")
        return

    city = input("Введите город (оставьте пустым для поиска по всей России): ").strip()

    try:
        top_n = int(input("Сколько вакансий показать? "))
        top_n = max(1, top_n)
    except ValueError:
        print("Ошибка: Введите число")
        return

    filter_words = input("Ключевые слова для фильтрации (через пробел): ").split()

    try:
        print("\nИщем вакансии...")
        raw_vacancies = hh_api.get_vacancies(keyword, city if city else None)

        vacancies = []
        for v in raw_vacancies:
            salary = v.get('salary')
            salary_from = salary.get('from') if salary else None

            vacancy = Vacancy(
                title=v.get('name'),
                url=v.get('alternate_url'),
                salary=salary_from,
                description=v.get('snippet', {}).get('responsibility'),
                requirements=v.get('snippet', {}).get('requirement')
            )
            vacancies.append(vacancy)

        # Фильтрация по зарплате
        salary_filters = [int(word) for word in filter_words if word.isdigit()]
        if salary_filters:
            min_salary = max(salary_filters)
            vacancies = [v for v in vacancies if v.salary and v.salary >= min_salary]

        # Фильтрация по ключевым словам
        text_filters = [word for word in filter_words if not word.isdigit()]
        filtered = filter_vacancies(vacancies, text_filters)

        sorted_vac = sort_vacancies(filtered)
        top_vac = get_top_vacancies(sorted_vac, top_n)

        print(f"\nНайдено вакансий: {len(top_vac)}")
        if city:
            print(f"Город: {city}")
        print_vacancies(top_vac)

        # Сохранение только уникальных вакансий
        existing_urls = {v['url'] for v in storage.get_vacancies()}
        new_vacancies = [v for v in top_vac if v.url not in existing_urls]

        for vacancy in new_vacancies:
            storage.add_vacancy(vacancy.to_dict())

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interaction()
