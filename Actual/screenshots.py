import threading

class Screenshot:
    frames = {}
    lock = threading.Lock()