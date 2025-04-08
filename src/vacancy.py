class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ['title', 'url', 'salary', 'description', 'requirements']

    def __init__(self, title: str, url: str, salary: int,
                 description: str, requirements: str):
        """
        Args:
            title: Название вакансии
            url: Ссылка на вакансию
            salary: Зарплата
            description: Описание
            requirements: Требования
        """
        self.title = self.__validate_title(title)
        self.url = self.__validate_url(url)
        self.salary = self.__validate_salary(salary)
        self.description = description or "Описание отсутствует"
        self.requirements = requirements or "Требования не указаны"

    def __validate_title(self, title: str) -> str:
        """Валидация названия вакансии"""
        if not title or not isinstance(title, str):
            return "Без названия"
        return title

    def __validate_url(self, url: str) -> str:
        """Валидация URL"""
        if not url or not isinstance(url, str) or not url.startswith('http'):
            return "#"
        return url

    def __validate_salary(self, salary: int) -> int:
        """Валидация зарплаты"""
        if not isinstance(salary, int) or salary < 0:
            return 0
        return salary

    def to_dict(self) -> dict:
        """Преобразовать вакансию в словарь"""
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'description': self.description,
            'requirements': self.requirements
        }

    def __lt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (меньше)"""
        return self.salary < other.salary

    def __gt__(self, other) -> bool:
        """Сравнение вакансий по зарплате (больше)"""
        return self.salary > other.salary

    def __eq__(self, other) -> bool:
        """Сравнение вакансий по зарплате (равно)"""
        return self.salary == other.salary

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_info = f"{self.salary} руб." if self.salary else "не указана"
        return (f"{self.title}\nЗарплата: {salary_info}\n"
                f"Требования: {self.requirements[:100]}...\nСсылка: {self.url}\n")
