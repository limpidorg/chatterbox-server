import core.notifications
from utils import returnMessage

MESSAGE_TYPES = {

}


def classifyMessage(message):
    """
    Classify a message based on its contents.
    """
    pass


def messageValidation(sessionId, chatId, message, socketId):
    allowed = notARealFunction(message)
    if not allowed:
        # Sends warning message to the client
        core.notifications.sendNotificationToSocketId(socketId, 'show-alert', returnMessage(0, message='You are not allowed to use that word.', title="Warning", actions=[
            {
                'type': 'normal',
                'title': 'Learn Why',
                'link': "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            {
                'type': 'cancel',
                'title': 'OK'
            }
        ]))
        return False # Return false in messageValidation stops the message from being sent.
    return True



def notARealFunction(message):
    if 'fuck' in message.lower():
        return False
    return True
