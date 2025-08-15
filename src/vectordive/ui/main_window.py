from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from vectordive.config import base
from vectordive.ui.widgets.telemetry_bars import ProgressBar

class MainWindow(QMainWindow):
    ##テスト用でtelemetry_bars.pyのみを表示する
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector Dive - Thruster Control")
        self.setGeometry(100, 100, 600, 400)

        # メインウィジェットの設定
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # レイアウトの設定
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # プログレスバーの初期化
        self.progress_bar = ProgressBar()
        self.layout.addWidget(self.progress_bar.get_widget())

class telemetry_window:
    def __init__(self):
        self.main_window = MainWindow()
        self.main_window.show()

    def update_thruster_value(self, value):
        """Update the thruster value in the progress bar."""
        self.progress_bar.set_value(value)

    def get_thruster_value(self):
        """Get the current thruster value from the progress bar."""
        return self.progress_bar.get_value()

class depth_graph_window:
    def __init__(self):
        from vectordive.ui.widgets.depth_graph import DepthGraph
        self.depth_graph = DepthGraph()
        self.layout.addWidget(self.depth_graph.get_widget())

    def update_depth_graph(self, time_data, depth_data):
        """Update the depth graph with new data."""
        self.depth_graph.update_graph(time_data, depth_data)

    def clear_depth_graph(self):
        """Clear the depth graph."""
        self.depth_graph.clear_graph()
        
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())