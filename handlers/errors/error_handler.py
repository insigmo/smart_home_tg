
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)

from loader import dp
from utils.misc.logging import logger


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logging
    """
    exceptions = {
        CantDemoteChatCreator: "Can't demote chat creator",
        MessageNotModified: "Message is not modified",
        MessageCantBeDeleted: "Message can't be deleted",
        MessageToDeleteNotFound: "Message to delete not found",
        MessageTextIsEmpty: "MessageTextIsEmpty",
        Unauthorized: f'Unauthorized: {exception}',
        InvalidQueryID: f'InvalidQueryID: {exception} \nUpdate: {update}',
        TelegramAPIError: f'TelegramAPIError: {exception} \nUpdate: {update}',
        RetryAfter: f'RetryAfter: {exception} \nUpdate: {update}',
        CantParseEntities: f'CantParseEntities: {exception} \nUpdate: {update}',
    }
    if exceptions.get(exception):
        msg = exceptions.get(exception)
        logger.exception(msg)
    else:
        logger.exception(f'Update: {update} \n{exception}')
    return exceptions.get(exception)
