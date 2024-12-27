import threading

class Processed_Screenshot:
    index = 0
    frames = [None] * 20
    lock = threading.Lock()