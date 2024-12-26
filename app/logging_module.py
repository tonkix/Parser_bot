import logging


async def write_error_to_log(message):
    print(message)
    logging.error(message)
