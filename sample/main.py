from PyQt5.QtWidgets import QApplication, QMessageBox, QStatusBar
from PyQt5 import uic


class Test:
    def __init__(self):
        self.ui = uic.loadUi("test2.ui")
        self.ui.pushButton.clicked.connect(self.disconnect)
        self.ui.pushButton_2.clicked.connect(self.serial_connect)
        self.ui.pushButton_3.clicked.connect(self.ssh_connect)
        self.ui.pushButton_4.clicked.connect(self.power_set)
        self.ui.pushButton_5.clicked.connect(self.common_test)

        # self.ui.pushButton_9.clicked.connect(lambda: self.gotoStack(0))
        # self.ui.pushButton_10.clicked.connect(lambda: self.gotoStack(1))
        self.RS232_COMMAND = {
            # 设置电压220V
            'command_hex1': '64 06 00 08 08 98 07 97',
            # 设置电压264V
            'command_hex2': '64 06 00 08 0A 50 07 61',
            # 设置电压176V
            'command_hex3': '64 06 00 08 06 E0 03 D5'

        }
        self.serial = None
        self.ui.textBrowser.setPlainText('未连接')
        self.ui.pushButton.setEnabled(False)
        self.statusBar = QStatusBar()
        self.ui.setStatusBar(self.statusBar)
        self.statusBar.showMessage("当前未连接")


    def disconnect(self):
        self.ui.textBrowser.setPlainText('未连接')
        QMessageBox.about(self.ui, '结果', '已断开连接')
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.serial = None
        self.statusBar.showMessage("当前未连接")

    def serial_connect(self):
        serial_no = self.ui.lineEdit_1.text()
        bps = self.ui.lineEdit_2.text()
        timeout = self.ui.lineEdit_3.text()

        if not serial_no:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入串口号')
            return

        if not bps:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入波特率')
            return

        if not timeout:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入超时时间')
            return

        if serial_no == 'COM3' and bps == '115200' and timeout == '3':
            self.ui.textBrowser.setPlainText('已连接!串口号：%s, 波特率：%s， 超时时间： %s' % (
                serial_no, bps, timeout))
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton.setEnabled(True)
            self.serial = 'ok'
            self.statusBar.showMessage("已建立连接")
        else:
            self.ui.textBrowser.setPlainText('连接失败...')

    def ssh_connect(self):
        ssh_ip = self.ui.lineEdit_4.text()
        ssh_port = self.ui.lineEdit_5.text()
        username = self.ui.lineEdit_6.text()
        password = self.ui.lineEdit_7.text()

        if not ssh_ip:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入IP地址')
            return

        if not ssh_port:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入端口号')
            return

        if not username:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入用户名')
            return

        if not password:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入密码')
            return

        if ssh_ip == '1.1.1.1' and ssh_port == '22' and username == 'root' and password == 'abc12345':
            self.ui.textBrowser.setPlainText('已连接!IP地址：%s, 端口：%s, 登录用户：%s' % (ssh_ip, ssh_port, username))
            self.ui.pushButton_2.setEnabled(False)
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton.setEnabled(True)
            self.serial = 'ok'
            self.statusBar.showMessage("已建立连接")
        else:
            self.ui.textBrowser.setPlainText('连接失败...')

    def power_set(self):
        if not self.serial:
            QMessageBox.warning(
                self.ui,
                '错误', '请先连接设备！')
            return
        power = self.ui.comboBox.currentText()
        sleep_time = self.ui.lineEdit_8.text()

        if not sleep_time:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入时间')
            return

        QMessageBox.about(self.ui,
                          '统计结果',
                          f'''电压为：\n{power}
                          \n时间为：\n{sleep_time}s'''
                          )

    def common_test(self):
        if not self.serial:
            QMessageBox.warning(
                self.ui,
                '错误', '请先连接设备！')
            return
        duty_cycle = self.ui.lineEdit_9.text()
        frequency = self.ui.lineEdit_10.text()

        if not duty_cycle:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入占空比')
            return
        elif not duty_cycle.isdigit():
            QMessageBox.warning(
                self.ui,
                '错误', '占空比需要为数字')
            return
        elif int(duty_cycle) > 100 or int(duty_cycle) < 1:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入1-100的占空比')
            return

        if not frequency:
            QMessageBox.warning(
                self.ui,
                '错误', '请输入频率')
            return

        QMessageBox.about(self.ui,
                          '统计结果',
                          f'''占空比为：\n{duty_cycle}
                                  \n频率为：\n{frequency}'''
                          )

    # def gotoStack(self, index):
    #     self.ui.stackedWidget.setCurrentIndex(index)

    def serial_sent_hex(self, command):
        var = bytes.fromhex(self.RS232_COMMAND[command])
        self.serial.write(var)
        data = self.serial.read(1024)
        data = str(data, encoding='utf-8')
        return data


app = QApplication([])
test = Test()
test.ui.show()
app.exec_()
