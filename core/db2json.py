def Session(Session):
    'For the sake of security & privacy, we would like to manually limit what information should be sent through'
    return {
        'sessionId': Session.sessionId,
        'created': Session.created,
        'activeChats': Session.activeChats,
    }
