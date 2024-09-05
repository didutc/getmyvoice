from PyQt5 import QtCore, QtGui, QtWidgets
import time
import pyperclip
import requests
import os
from datetime import datetime
import pyperclip
import time
from PyQt5.QtGui import QIcon
import os
class Worker(QtCore.QThread):
    # 작업이 완료되면 시그널 발생
    finished = QtCore.pyqtSignal()

    def run(self):
        # 여기서 작업을 수행합니다. time.sleep()으로 시뮬레이션
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br"
        }

        t=pyperclip.paste()
        t = t.split('\r\n')
        t_lst = []
        for li in t:
            if 'https://cdn.typecast.ai/data/s/' in li:
                t_lst.append(li)


        for li in t_lst:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{timestamp}.wav"
            response = requests.get(li, headers=headers)
            with open('D:\\audioch\\'+filename, "wb") as file:
                    file.write(response.content)
            time.sleep(1)



        self.finished.emit()  # 작업이 끝나면 시그널 발생

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 150)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(250, 100))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        # 버튼 클릭 시 on_button_click 함수 연결
        self.pushButton.clicked.connect(self.on_button_click)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 작업 스레드 초기화
        self.worker = Worker()
        self.worker.finished.connect(self.on_worker_finished)
        MainWindow.setWindowIcon(QIcon('ico.png'))
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "오디오 다운로드"))
        self.pushButton.setText(_translate("MainWindow", "다운로드"))

    def on_button_click(self):
        # 버튼을 비활성화하고 작업 시작
        self.pushButton.setEnabled(False)
        self.worker.start()

    def on_worker_finished(self):
        # 작업이 끝나면 버튼을 다시 활성화
        self.pushButton.setEnabled(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
