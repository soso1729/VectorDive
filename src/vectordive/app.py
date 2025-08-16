from ast import main
from vectordive.ui.entrance_window import EntranceWindow
from vectordive.ui.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EntranceWindow()
    window.show()
    # EntranceWindowからMainWindowに遷移するためのコード
    def show_main_window():
        main_window = MainWindow()
        main_window.show()
        return main_window

    # EntranceWindowのcloseイベントでMainWindowを表示
    def on_entrance_closed():
        global main_window_instance
        main_window_instance = show_main_window()

    window.destroyed.connect(on_entrance_closed)
    sys.exit(app.exec_())