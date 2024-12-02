import threading

class Processed_Screenshot:
    index = 0
    frames = []
    lock = threading.Lock()