import CoreModel
import Parser
import threading
import queue
import datetime
from PyQt5.Qt import *
from netaddr import IPNetwork


class MainPresenter:
    def __init__(self, ui):
        self.ui = ui
        self.threads = []
        self.isScanEnabled = False
        self.queue = queue.Queue()

    def startScan(self, ipRanges, portsStr, threadNumber, timeout):
        if timeout == '':
            timeout = '3'
        cidrIPRanges = Parser.getCIDRFromRanges(ipRanges)
        ports = Parser.getPortsFromString(portsStr)
        ips = []
        for cidr in cidrIPRanges[0]:
            for ip in IPNetwork(cidr):
                ips.append(str(ip))
        for ip in ips:
            self.queue.put(ip)
        for i in range(int(threadNumber)):
            self.threads.append(ScanThread(self.queue, ports, timeout, self))
            self.setCurrentThreadsLabel(len(self.threads))
        for thread in self.threads:
            thread.signal.connect(self.setLogText)
            thread.exit_signal.connect(self.on_thread_exit)
            thread.start()

    def on_thread_exit(self, is_last):
        if is_last:
            self.isScanEnabled = False
            self.ui.startButton.setText("Start")
            return
        count = 0
        for thr in self.threads:
            if thr.is_running:
                count = count + 1
        self.setCurrentThreadsLabel(count)

    def stopScan(self):
        self.isScanEnabled = False
        for thread in self.threads:
            thread.exit()
            thread.is_running = False
            count = 0
            is_last_thread = False
            for i in self.threads:
                if not i.is_running:
                    count += 1
            if count == len(self.threads):
                is_last_thread = True
            thread.exit_signal.emit(is_last_thread)
        self.threads.clear()
        self.ui.currentThreadsLabel.setText("0")
        self.queue = queue.Queue()

    def setLogText(self, string):
        self.ui.dataText.append("[" + str(datetime.datetime.now()) + "] " + str(string))

    def setCurrentThreadsLabel(self, threadNumber):
        self.ui.currentThreadsLabel.setText(str(threadNumber))


class ScanThread(QThread):

    signal = pyqtSignal(str)
    exit_signal = pyqtSignal(bool)

    def __init__(self, scanQueue, ports, timeout, presenter, parent=None):
        QThread.__init__(self, parent)
        self.scanQueue = scanQueue
        self.coreModel = CoreModel.CoreModel(timeout)
        self.ports = ports
        self._stop_event = threading.Event()
        self.timeout = timeout
        self.presenter = presenter
        self.is_running = True

    def run(self):
        while True:
            if self.scanQueue.empty():
                self.is_running = False
                count = 0
                is_last_thread = False
                for i in self.presenter.threads:
                    if not i.isRunning():
                        count += 1
                if count == len(self.presenter.threads):
                    is_last_thread = True
                self.exit_signal.emit(is_last_thread)
                self.exit(1)
            hostObject = self.scanQueue.get()
            open_ports = self.coreModel.scanIP(str(hostObject), self.ports)
            signalStr = ', '.join(open_ports)
            if signalStr != '':
                self.signal.emit(str(hostObject) + ' has open ports: ' + signalStr)
            self.scanQueue.task_done()
