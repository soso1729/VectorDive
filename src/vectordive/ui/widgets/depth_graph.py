# depth_graph.py
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from vectordive.config import base

class DepthGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---- 設定値の取得 ----
        title   = getattr(base, "GRAPH_TITLE", "Depth")
        label_x = getattr(base, "GRAPH_X_LABEL", "Time [s]")
        label_y = getattr(base, "GRAPH_Y_LABEL", "Depth [m]")
        x_range = getattr(base, "GRAPH_X_RANGE", None)  # 例: (0, 60)
        y_range = getattr(base, "GRAPH_Y_RANGE", None)  # 例: (0, 100)
        min_h   = getattr(base, "GRAPH_MIN_HEIGHT", 200)
        min_w   = getattr(base, "GRAPH_MIN_WIDTH",  300)

        # ---- UI 構築 ----
        self.plot = pg.PlotWidget(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot, alignment=Qt.Alignment(0))

        # ---- Plot 設定 ----
        self.plot.setTitle(title)
        self.plot.setLabel('bottom', label_x)
        self.plot.setLabel('left',   label_y)

        if isinstance(x_range, (tuple, list)) and len(x_range) == 2:
            self.plot.setXRange(*x_range, padding=0)
        if isinstance(y_range, (tuple, list)) and len(y_range) == 2:
            self.plot.setYRange(*y_range, padding=0)

        self.plot.setMinimumHeight(min_h)
        self.plot.setMinimumWidth(min_w)

        # 1本の曲線を保持して setData で更新する
        self.curve = self.plot.plot([], [], symbol='o', symbolSize=5)

    def get_widget(self):
        """埋め込み用の QWidget を返す（自分自身）。"""
        return self

    def update_graph(self, time_data, depth_data):
        """データを更新して再描画。"""
        self.curve.setData(time_data, depth_data)
        if len(time_data) > 1:
            self.plot.setXRange(min(time_data), max(time_data), padding=0.02)
        if len(depth_data) > 1:
            self.plot.setYRange(min(depth_data), max(depth_data), padding=0.02)

    def clear_graph(self):
        """描画をクリアして既定レンジへ。"""
        self.curve.setData([], [])
        x_range = getattr(base, "GRAPH_X_RANGE", (0, 60))
        y_range = getattr(base, "GRAPH_Y_RANGE", (0, 100))
        self.plot.setXRange(*x_range, padding=0)
        self.plot.setYRange(*y_range, padding=0)
