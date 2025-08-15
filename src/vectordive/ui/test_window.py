# realtime_threaded.py
import sys, collections, time, random
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg

class DataWorker(QThread):
    new_data = pyqtSignal(float, float)  # (t, depth)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True
        self._t0 = time.time()

    def run(self):
        while self._running:
            t = time.time() - self._t0
            depth = 10 + random.uniform(-0.2, 0.2)  # ここを実センサ値に置換
            self.new_data.emit(t, depth)
            self.msleep(20)  # ~50Hz

    def stop(self):
        self._running = False

class RealTimePlot(pg.PlotWidget):
    def __init__(self, maxlen=500):
        super().__init__()
        self.setWindowTitle("Realtime Depth (thread-safe)")
        self.setLabel('bottom', 'time', units='s')
        self.setLabel('left', 'depth', units='m')
        self.enableAutoRange('y', True)

        self.t = collections.deque(maxlen=maxlen)
        self.z = collections.deque(maxlen=maxlen)
        self.curve = self.plot([], [])

        # worker 起動
        self.worker = DataWorker()
        self.worker.new_data.connect(self.on_new_data)  # GUIスレッドで実行される
        self.worker.start()

        # 画面更新は適度に間引く（重い場合）
        self._dirty = False
        self._refresh = QTimer(self)
        self._refresh.timeout.connect(self.flush)
        self._refresh.start(33)  # ~30fps

    def on_new_data(self, t, depth):
        self.t.append(t)
        self.z.append(depth)
        self._dirty = True

    def flush(self):
        if not self._dirty:
            return
        self.curve.setData(self.t, self.z)
        if len(self.t) >= 2:
            self.setXRange(self.t[0], self.t[-1], padding=0)
        self._dirty = False

    def closeEvent(self, e):
        # 終了時にワーカを確実に停止
        if self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(1000)
        super().closeEvent(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RealTimePlot()
    win.resize(800, 400)
    win.show()
    sys.exit(app.exec_())
