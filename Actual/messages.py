import queue
import threading

class MessageQueue:
    status_queue = queue.Queue()
    lock = threading.Lock()