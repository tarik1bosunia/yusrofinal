"""
@ _session_key(request)
@ try to get previously created session key
@ if session key does not exist. it creates a new session key
@ return session key of the user
"""


def _session_key(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    print("session key: ", session_key)
    return session_key
