import threading

class Processed_Screenshot:
    frames = {}
    sentence_dict = {}
    lock = threading.Lock()

# def upon_receive_message():
#     TTS.say(ttsmessage)
    
# def on_click():
#     screenshot = Processed_Screenshot.frames['device1']['timestamp1']
#     display(screenshot)

# def ocr_identified():
#     Processed_Screenshot.frames.update('device1', 'timestamp1', 'screenshot3')

# frames = {'device1': {'timestamp1':'screenshot1', 'timestamp2':'screenshot2'},
#           'device2': {'timestamp1':'screenshot1'},
#           'device3': {'timestamp1':'screenshot1', 'timestamp2':'screenshot2', 'timestamp3':'screenshot3'}}