from Global import API
from flask import request
from utils import returnMessage, parseData
import core.match
import threading
import time
import core.session
import core.notifications


@API.on("new-chat-request")
@parseData
def newChatRequest(sessionId):
    print(f'New chat request from {sessionId} (matching)')
    core.match.findMatchFor(sessionId)
    return returnMessage(0, message='New chat request received')
