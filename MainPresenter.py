from network_scan.CoreModel import CoreModel
from address_generation.Parser import Parser
import threading
import datetime
from PyQt5.Qt import *
from address_generation.IpGenerator import IpGenerator
from storage.JSONStorage import JSONStorage


class MainPresenter:
    def __init__(self, ui):
        self.ui = ui
        self.threads = []
        self.isScanEnabled = False
        self.parser = Parser()
        #needed config to specify path
        self.storage = JSONStorage("results.json")

    def startScan(self, ipRanges, portsStr, threadNumber, timeout):
        if timeout == '':
            timeout = '3'
        addresses = self.parser.parse_address_field(ipRanges)
        ports = self.parser.parse_port_field(portsStr)
        print(ports)
        self.ip_generator = IpGenerator(addresses,ports)
        for i in range(int(threadNumber)):
            self.threads.append(ScanThread(self.ip_generator, ports, timeout, self))
            self.setCurrentThreadsLabel(len(self.threads))
        for thread in self.threads:
            thread.signal.connect(self.setLogText)
            thread.exit_signal.connect(self.on_thread_exit)
            thread.start()

    def on_thread_exit(self):
        count = 0
        for thr in self.threads:
            if thr.is_running:
                count = count + 1
        if count == len(self.threads):
            self.on_end_scanning()
        self.setCurrentThreadsLabel(count)

    def on_end_scanning(self):
            self.isScanEnabled = False
            self.ui.startButton.setText("Start")
            self.storage.save()

    def stopScan(self):
        self.isScanEnabled = False
        for thread in self.threads:
            thread.exit()
        for thread in self.threads:
            thread.wait()
        self.on_end_scanning()
        self.threads.clear()
        self.ui.currentThreadsLabel.setText("0")

    def setLogText(self, string):
        self.ui.dataText.append("[" + str(datetime.datetime.now()) + "] " + str(string))

    def setCurrentThreadsLabel(self, threadNumber):
        self.ui.currentThreadsLabel.setText(str(threadNumber))


class ScanThread(QThread):

    signal = pyqtSignal(str)
    exit_signal = pyqtSignal()

    def __init__(self, ip_generator, ports, timeout, presenter, parent=None):
        QThread.__init__(self, parent)
        self.ip_generator = ip_generator
        self.previous_address = None
        self.coreModel = CoreModel(timeout)
        self._stop_event = threading.Event()
        self.timeout = timeout
        self.presenter = presenter
        self.is_running = True

    def run(self):
        while True:
            scan_address = self.ip_generator.get_next_address(self.previous_address)
            if not scan_address:
                break
            self.previous_address = scan_address
            scan_result = self.coreModel.scan_address(scan_address)
            self.presenter.storage.put_responce(scan_address, scan_result)
            if scan_result == 0:
                self.signal.emit('%s has open port: %s' % scan_address)
            else:
                self.signal.emit('%s has closed port: %s' % scan_address)
        self.is_running = False
        self.exit_signal.emit()
        self.exit(1)
