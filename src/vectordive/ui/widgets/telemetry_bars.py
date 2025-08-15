from PyQt5.QtWidgets import QProgressBar
from vectordive.config import base

class ProgressBar:
    def __init__(self):
        # QProgressBarウィジェットの初期化
        maximum = base.THRUSTER_MAXIMUM
        minimum = base.THRUSTER_MINIMUM  # 修正: MINMUM → MINIMUM
        default = base.THRUSTER_DEFAULT
        title = base.BAR_TITLE

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(minimum)
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(default)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat(title)

    def get_widget(self):
        # QProgressBarウィジェットを返す
        return self.progress_bar

    def set_value(self, value):
        # QProgressBarの値を設定する
        self.progress_bar.setValue(value)

    def get_value(self):
        # QProgressBarの値を取得する
        return self.progress_bar.value()