import threading

class Processed_Screenshot:
    frames = {}
    lock = threading.Lock()