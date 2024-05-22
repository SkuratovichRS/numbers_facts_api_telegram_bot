from functools import wraps


def status_code_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        print(f"{func.__name__}: {response.status_code=}")
        return response.text

    return wrapper
