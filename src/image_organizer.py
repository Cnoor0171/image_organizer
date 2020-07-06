"""tests"""
import logging

logger = logging.getLogger()


def my_func(string: str):
    """tests"""
    logger.warning(f"asd {2}")
    return string[::-1]
