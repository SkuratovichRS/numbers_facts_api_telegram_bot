import requests
from tools import status_code_logger


class NumbersApi:
    def __init__(self):
        self.base_url = "http://numbersapi.com/"

    @status_code_logger
    def get_trivia_fact(self, number: int = None) -> requests.Response:
        if not number:
            url = self.random_url()
        else:
            url = f"{self.base_url}{str(number)}"
        response = requests.get(url=url)
        return response

    @status_code_logger
    def get_math_fact(self, number: int = None) -> requests.Response:
        if not number:
            url = f"{self.random_url()}math"
        else:
            url = f"{self.base_url}{str(number)}/math"
        response = requests.get(url=url)
        return response

    @status_code_logger
    def get_date_fact(self, date: str = None) -> requests.Response:
        """
        Use date in month/day format
        :param date: str
        :return: str
        """
        if not date:
            url = f"{self.random_url()}date"
        else:
            url = f"{self.base_url}{date}/date"
        response = requests.get(url=url)
        return response

    @status_code_logger
    def get_year_fact(self, year: int = None) -> requests.Response:
        if not year:
            url = f"{self.random_url()}year"
        else:
            url = f"{self.base_url}{str(year)}/year"
        response = requests.get(url=url)
        return response

    def random_url(self) -> str:
        return f"{self.base_url}random/"
