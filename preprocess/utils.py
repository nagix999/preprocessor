from pathlib import Path
import time
from functools import wraps


def log_execution_time(logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info(f"{func.__name__} took {duration:.2f} seconds to complete")
            return result

        return wrapper

    return decorator


def get_stem_and_ext(filepath):
    path = Path(filepath)
    return path.stem, path.suffix
