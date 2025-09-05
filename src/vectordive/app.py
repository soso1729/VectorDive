from ast import main
from vectordive.ui.entrance_window import EntranceWindow
from vectordive.ui.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        
        print("Vector Dive アプリケーションを起動中...")
        print("EntranceWindowからMAVLink接続を設定してください")
        
        # EntranceWindowを起動
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
        
        print("EntranceWindowが表示されました")
        print("IPアドレスとポートを設定してConnectボタンを押してください")
        print("または、Debug Modeボタンでテストモードを開始できます")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)