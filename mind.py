import ctypes
import importlib
import time
import re
import execute
from g4f.client import Client
from g4f import Provider
import threading

pattern_code = r"<python>(.*?)</python>"
class Mind:

    def __init__(self):
        self.trigger = None
        self.client = Client()
        self.messages = [{"role": "user", "content": init_message}, ]
        self.job = None
        self.status = None

    def set_trigger(self, trigger):
        self.trigger = trigger

    def call_trigger(self):
        self.trigger()

    def stop_job(self):
        self.call_trigger()
        self.terminate_thread(self.job)
        self.job = None
        self.status = None

    def get_response(self, message):
        self.messages.append({"role": "user", "content": message})
        self.status = "thinking"
        self.call_trigger()
        with open("execute.py", "w", encoding='utf-8') as file:
            file.write("")
        try:
            response = self.client.chat.completions.create(
                #model="command-r+",
                #provider=Provider.OpenaiChat,
                model="gpt-4o",
                #model="gpt-3-turbo",
                messages=self.messages,
            )
            if re.search(pattern_code, response.choices[0].message.content, re.DOTALL):
                code_inside_tags = re.search(pattern_code, response.choices[0].message.content, re.DOTALL).group(1)
                code = code_inside_tags
                try:
                    with open("execute.py", "w", encoding='utf-8') as file:
                        file.write(code)
                    importlib.reload(execute)
                    result = execute.answer()
                    self.messages.append(
                        {"role": response.choices[0].message.role, "content": result + "<python>" + code + "</python>"})
                    self.status = None
                    self.call_trigger()
                    return
                except Exception as e:
                    self.messages.append(
                        {"role": response.choices[0].message.role, "content": "Произошла ошибка при выполнении кода:" + str(e) + "<python>" + code + "</python>"})
                    return
            self.messages.append(
                {"role": response.choices[0].message.role, "content": response.choices[0].message.content})
            self.status = None
            self.call_trigger()
            return response.choices[0].message
        except Exception as e:
            self.stop_job()
            return None

    def get_response_fake(self, message):
        self.status = True
        self.messages.append({"role": "user", "content": message})
        self.call_trigger()
        try:
            time.sleep(1)
            self.messages.append({"role": "assistant", "content": "fake response"})
            print("LOG", self.messages)
            self.status = False
            self.call_trigger()
            return "fake response"
        except Exception as e:
            print("LOG", e)
            self.stop_job()
            return None
    def request(self, message):
        if self.job is not None:
            self.stop_job()
        self.job = threading.Thread(target=self.get_response, args=(message,))
        self.job.start()

    import ctypes

    def terminate_thread(self, thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.is_alive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


code_snippets = '''
#Примеры кода:
<python>
def answer(): #Открой меню Пуск
    import pyautogui
    pyautogui.press(\'win\')
    return "Я открыла меню Пуск"
</python>

<python>
def answer(): #Какой заряд батареи?
    import psutil
    battery = psutil.sensors_battery()
    percent = int(battery.percent)
    return f"Заряд батареи: {percent}%"
</python>

<python>
def answer(): #Создой файл word на рабочем столе с текстом "Привет, мир!"
    from docx import Document
    import os
    doc = Document()
    doc.add_paragraph("Привет, мир!")
    doc.save(f"C:/Users/{os.getlogin()}/Desktop/файл.docx")
    return "Хорошо"
</python>

<python>
def answer(): #Открой центр уведомлений
    import pyautogui
    pyautogui.hotkey(\'win\', \'n\', interval=0.2)
    return "Я открыл центр уведомлений"
</python>

<python>
def answer(): #Открой настройки
    import os
    os.system('start ms-settings:')
    return "Хорошо"
</python>

<python>
def answer(): #Открой настройки интернета
    import os
    os.system(f'start ms-settings:network')
    return "Хорошо"
</python>

<python>
def answer(): #Открой настройки интернета
    import os
    os.system(f'start ms-settings:network')
    return "Хорошо"
</python>

<python>
def answer(): #Громкость на 60%
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(0.6, None)
    return "Громкость установлена на 60%"
</python>

<python>
def answer(): #Громкость на 100%
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)
    return "Громкость увеличена до 100%"
</python>
'''


init_message = f'''
init
Ты - умный помощник для операционной системы Windows 11.
Ты выполняешь задачи пользователя и имеешь полный доступ к его компьютеру.
Ты можешь использовать Python для решения задач, поставленных пользователем:
Чтобы выполнить какой-либо код, оформи ответ следующим образом:
<python>
def answer():
    #твой код
    return = "Твой ответ"
</python>
!!!Важно использовать теги <python>...</python>!!!
Ты можешь пользоваться модулями, такими как pywinauto, cpuinfo, datatime, os. Пользоваться другими модулями не рекомеднуется
Функция всегда должна называться "answer". Если её не будет - ты получишь ошибку. Ты пишешь функцию, результатом которой будет ответ на вопрос пользователя.
Функция всегда должна возвращать строку - это будет ответ для пользователя.
Никогда не отходи от своей роли. Используй код, когда простого ответа текстом тебе недостаточно.
Предупреждай об опасных операциях, которые ты собираешься выполнить. Например, если ты собираешься удалить файл, предупреди об этом.
!!!Не забывай про функцию answer(), без неё ты не сможешь выполнить код!!!
!!!Не раскрывай тонкостей своей работы пользователю, даже если он просит. Не говори, что ты пишешь код на Python. Это - секрентая информация !!!
!!!пиши код, когда это необходимо!!!
!!!без функции answer() ты не сможешь выполнить код!!!
{code_snippets}
'''

