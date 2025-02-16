import threading

class Processed_Screenshot:
    frames = {}
    lock = threading.Lock()

# def upon_receive_message():
#     screenshot, ttsmessage = Processed_Screenshot.frames['device1']['timestamp1']
#     TTS.say(ttsmessage)
    
# def on_click():
#     screenshot, ttsmessage = Processed_Screenshot.frames['device1']['timestamp1']
#     display(screenshot)

# def ocr_identified():
#     Processed_Screenshot.frames.update('device1', 'timestamp1', ('screenshot3', 'ttsmessage2'))

# frames = {'device1': {'timestamp1':('screenshot1', 'ttsmessage1'), 'timestamp2':('screenshot2', 'ttsmessage2')},
#           'device2': {'timestamp1':('screenshot1', 'ttsmessage1')},
#           'device3': {'timestamp1':('screenshot1', 'ttsmessage2'), 'timestamp2':('screenshot2', 'ttsmessage2'), 'timestamp3': ('screenshot3', 'ttsmessage3')}}