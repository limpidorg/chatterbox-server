def returnMessage(code, message = None, **kw):
    if message == None:
        message = 'Completed'
    
    return {
        "code": code,
        "message": message,
        **kw
    }
