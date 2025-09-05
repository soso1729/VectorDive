from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QSplitter, QApplication, QLabel
from PyQt5.QtGui import QKeySequence
from vectordive.config import base
from vectordive.ui.widgets.telemetry_bars import ProgressBar

class MainWindow(QMainWindow):
    ##テスト用でtelemetry_bars.pyのみを表示する
    def __init__(self, connection_info=None):
        super().__init__()
        
        # 接続情報を保存
        self.connection_info = connection_info
        
        # ウィンドウタイトルに接続情報を表示
        if connection_info:
            title = f"Vector Dive - Main Window ({connection_info['ip']}:{connection_info['port']})"
        else:
            title = "Vector Dive - Main Window"
        
        self.setWindowTitle(title)
        # ウィンドウサイズを適切なサイズに設定
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)  # 最小サイズ
        self.setMaximumSize(1600, 1200)  # 最大サイズ
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        
        # ウィンドウを中央に配置
        self.center_window()
        self.init_ui()
        
        # QSplitterのスタイルを設定
        self.setStyleSheet(self.styleSheet() + """
            QSplitter::handle {
                background-color: #555555;
                border: 1px solid #777777;
            }
            QSplitter::handle:hover {
                background-color: #777777;
            }
        """)
        
        # テレメトリ更新タイマーを初期化
        self.init_telemetry_timer()
        
        # デバッグ用バックドアの設定
        self.setup_debug_backdoor()

    def init_ui(self):
        # メインウィジェットの設定
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # メインレイアウト（水平分割）
        self.main_layout = QHBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # 左側の空欄（将来の実装用）
        self.left_panel = self.create_left_panel()
        self.main_layout.addWidget(self.left_panel)

        # 右側のメインコンテンツ
        self.right_panel = self.create_right_panel()
        self.main_layout.addWidget(self.right_panel)

        # 左右の比率を設定（左:右 = 1:4）
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 4)

    def create_left_panel(self):
        """左側の空欄パネルを作成"""
        panel = QGroupBox("Future Implementation")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #1e1e1e;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # 将来の実装用のプレースホルダー
        placeholder = QLabel("Future Features\n\n• Navigation\n• Settings\n• Status\n• Control Panel")
        placeholder.setStyleSheet("color: #888888; font-style: italic; font-size: 12px;")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)
        
        return panel

    def create_right_panel(self):
        """右側のメインコンテンツパネルを作成"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # 上部セクション（テレメトリ、深度グラフ、マップを横並び）
        self.top_section = self.create_top_section()
        layout.addWidget(self.top_section)

        # 下部セクション（ログ）
        self.bottom_section = self.create_bottom_section()
        layout.addWidget(self.bottom_section)

        # 比率を設定（上:下 = 5:1）- マップにより多くのスペース
        layout.setStretch(0, 5)
        layout.setStretch(1, 1)
        
        return panel

    def create_top_section(self):
        """上部セクションを作成（2分割：テレメトリ、深度+マップ）"""
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)

        # QSplitterを使用してリサイズ可能な分割を作成
        self.top_splitter = QSplitter(Qt.Horizontal)
        
        # 左側パーティション（テレメトリ情報）
        telemetry_partition = self.create_telemetry_partition()
        self.top_splitter.addWidget(telemetry_partition)

        # 右側パーティション（深度グラフとマップを縦に並べ）
        right_partition = self.create_right_partition()
        self.top_splitter.addWidget(right_partition)

        # 分割比率を設定（テレメトリ:深度+マップ = 1:4）- マップにより多くのスペース
        self.top_splitter.setSizes([250, 950])
        
        top_layout.addWidget(self.top_splitter)
        return top_widget

    def create_right_partition(self):
        """右側パーティション（深度グラフとマップを縦に並べ）"""
        partition = QWidget()
        layout = QVBoxLayout()
        partition.setLayout(layout)

        # 上部：深度グラフ（細長）
        depth_partition = self.create_depth_graph_partition()
        layout.addWidget(depth_partition)

        # 下部：マップ
        map_partition = self.create_middle_section()
        layout.addWidget(map_partition)

        # 比率を設定（深度:マップ = 1:5）- マップにより多くのスペース
        layout.setStretch(0, 1)
        layout.setStretch(1, 5)
        
        return partition

    def create_bottom_section(self):
        """下部セクションを作成（横長ログ、タイトルなし）"""
        section = QWidget()
        layout = QVBoxLayout()
        section.setLayout(layout)

        # ログ・ステータスパーティション
        log_partition = self.create_log_status_partition()
        layout.addWidget(log_partition)
        
        return section

    def create_middle_section(self):
        """中部セクション（マップ）を作成"""
        section = QWidget()
        layout = QVBoxLayout()
        section.setLayout(layout)
        
        # マップウィジェット（グリッド表示）
        self.map_widget = self.create_map_widget()
        layout.addWidget(self.map_widget)
        
        return section

    def create_map_widget(self):
        """マップウィジェットを作成（グリッド表示）"""
        from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
        from PyQt5.QtGui import QPen, QBrush, QColor
        
        # グラフィックスシーンを作成
        self.map_scene = QGraphicsScene()
        
        # グリッドサイズ（より大きな範囲）
        self.grid_size = 15
        self.grid_width = 60
        self.grid_height = 45
        
        # グリッドを描画
        for x in range(self.grid_width + 1):
            for y in range(self.grid_height + 1):
                # 縦線
                if x <= self.grid_width:
                    line = self.map_scene.addLine(x * self.grid_size, 0, x * self.grid_size, self.grid_height * self.grid_size, 
                                       QPen(QColor(100, 100, 100), 1))
                # 横線
                if y <= self.grid_height:
                    line = self.map_scene.addLine(0, y * self.grid_size, self.grid_width * self.grid_size, y * self.grid_size, 
                                       QPen(QColor(100, 100, 100), 1))
        
        # 中心点をマーク
        self.center_x = self.grid_width // 2 * self.grid_size
        self.center_y = self.grid_height // 2 * self.grid_size
        self.center_marker = self.map_scene.addEllipse(self.center_x - 5, self.center_y - 5, 10, 10, 
                                        QPen(QColor(255, 0, 0), 2), 
                                        QBrush(QColor(255, 0, 0)))
        
        # 中心点のラベル
        self.center_text = self.map_scene.addText("CENTER")
        self.center_text.setDefaultTextColor(QColor(255, 0, 0))
        self.center_text.setPos(self.center_x + 15, self.center_y - 10)
        
        # 座標軸のラベル
        x_label = self.map_scene.addText("X")
        x_label.setDefaultTextColor(QColor(255, 255, 255))
        x_label.setPos(self.grid_width * self.grid_size + 10, self.grid_height * self.grid_size // 2)
        
        y_label = self.map_scene.addText("Y")
        y_label.setDefaultTextColor(QColor(255, 255, 255))
        y_label.setPos(self.grid_width * self.grid_size // 2, -20)
        
        # 位置推定マーカー（初期化）
        self.position_marker = None
        self.position_text = None
        
        # グラフィックスビューを作成
        view = QGraphicsView(self.map_scene)
        view.setStyleSheet("""
            QGraphicsView {
                background-color: #2b2b2b;
                border: 1px solid #555555;
            }
        """)
        from PyQt5.QtGui import QPainter
        view.setRenderHint(QPainter.Antialiasing)
        
        return view

    def create_telemetry_partition(self):
        """テレメトリ情報パーティション（縦並び）"""
        partition = QWidget()
        layout = QVBoxLayout()
        partition.setLayout(layout)

        # 6つのスラスター用の縦並びプログレスバー
        self.progress_bar = ProgressBar()
        layout.addWidget(self.progress_bar.get_widget())
        
        # 位置推定ウィジェットを追加
        try:
            from vectordive.ui.widgets.position_estimation import PositionEstimationManager
            self.position_estimation_manager = PositionEstimationManager(self.connection_info, self)
            layout.addWidget(self.position_estimation_manager.get_widget())
        except ImportError as e:
            # インポートエラーの場合はプレースホルダーを表示
            from PyQt5.QtWidgets import QLabel
            placeholder = QLabel("Position Estimation Widget\n(Not available)")
            placeholder.setStyleSheet("color: #888888; font-style: italic;")
            placeholder.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder)
            self.position_estimation_manager = None

        return partition

    def create_depth_graph_partition(self):
        """深度グラフパーティション"""
        partition = QWidget()
        layout = QVBoxLayout()
        partition.setLayout(layout)

        # 深度グラフウィジェットを追加
        try:
            from vectordive.ui.widgets.depth_graph import DepthGraph
            self.depth_graph = DepthGraph()
            layout.addWidget(self.depth_graph.get_widget())
        except ImportError as e:
            # インポートエラーの場合はプレースホルダーを表示
            from PyQt5.QtWidgets import QLabel
            placeholder = QLabel("Depth Graph Widget\n(Not available)")
            placeholder.setStyleSheet("color: #888888; font-style: italic;")
            placeholder.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder)
            self.depth_graph = None

        return partition



    def create_log_status_partition(self):
        """ログ・ステータスパーティション"""
        partition = QWidget()
        layout = QVBoxLayout()
        partition.setLayout(layout)

        # ログコンソールウィジェットを追加
        try:
            from vectordive.ui.widgets.log_console import LogConsole
            self.log_console = LogConsole()
            layout.addWidget(self.log_console.get_widget())
        except ImportError as e:
            # インポートエラーの場合はプレースホルダーを表示
            from PyQt5.QtWidgets import QLabel
            placeholder = QLabel("Log Console Widget\n(Not available)")
            placeholder.setStyleSheet("color: #888888; font-style: italic;")
            placeholder.setAlignment(Qt.AlignCenter)
            layout.addWidget(placeholder)
            self.log_console = None

        return partition

    def center_window(self):
        """ウィンドウを画面中央に配置する"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    def setup_debug_backdoor(self):
        """デバッグ用バックドアの設定"""
        # キーボードショートカットの設定
        from PyQt5.QtWidgets import QShortcut
        
        # Ctrl+Shift+D でデバッグモード切り替え
        self.debug_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.debug_shortcut.activated.connect(self.toggle_debug_mode)
        
        # Ctrl+Shift+T でテレメトリテストデータ生成
        self.test_data_shortcut = QShortcut(QKeySequence("Ctrl+Shift+T"), self)
        self.test_data_shortcut.activated.connect(self.generate_test_telemetry)
        
        # Ctrl+Shift+R でリセット
        self.reset_shortcut = QShortcut(QKeySequence("Ctrl+Shift+R"), self)
        self.reset_shortcut.activated.connect(self.reset_debug_mode)
        
        # Ctrl+Shift+P で位置推定リセット
        self.position_reset_shortcut = QShortcut(QKeySequence("Ctrl+Shift+P"), self)
        self.position_reset_shortcut.activated.connect(self.reset_position_estimation)
        
        # キーボードショートカットの説明をコンソールに出力
        print("キーボードショートカット:")
        print("  Ctrl+Shift+D: デバッグモード切り替え")
        print("  Ctrl+Shift+T: テレメトリテストデータ生成")
        print("  Ctrl+Shift+R: デバッグモードリセット")
        print("  Ctrl+Shift+P: 位置推定リセット")
        
        # デバッグモードフラグ
        self.debug_mode = False
        self.test_data_counter = 0

    def init_telemetry_timer(self):
        """テレメトリ更新タイマーを初期化する"""
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.update_telemetry)
        
        # 接続情報がある場合はテレメトリ更新を開始
        if self.connection_info:
            self.telemetry_timer.start(2000)  # 2秒間隔で更新（より安定）
            
    def update_telemetry(self):
        """テレメトリデータを更新する"""
        try:
            # デバッグモードの場合はテストデータを使用
            if self.debug_mode:
                self.update_debug_telemetry()
                return
                
            if self.connection_info:
                # テレメトリデータを取得
                from vectordive.connections.telemetry import GetTelemetry
                telemetry = GetTelemetry(self.connection_info)
                
                # 接続状態を確認
                if telemetry.is_connected():
                    # スラスター値を取得
                    servo_data = telemetry.get_servo_output_raw_data()
                    
                    # テレメトリバーを更新
                    if hasattr(self, 'progress_bar') and self.progress_bar:
                        # 6つのスラスター値で更新
                        self.progress_bar.update_from_servo_data(*servo_data)
                else:
                    # 接続されていない場合の処理
                    if hasattr(self, 'progress_bar') and self.progress_bar:
                        self.progress_bar.telemetry_label.setText("Telemetry: No connection to MAVLink")
                        # デフォルト値を表示
                        default_data = (0, 0, 0, 0, 0, 0)
                        self.progress_bar.update_from_servo_data(*default_data)
                    
        except Exception as e:
            # エラー時はテレメトリバーにエラー状態を表示
            if hasattr(self, 'progress_bar') and self.progress_bar:
                self.progress_bar.telemetry_label.setText(f"Telemetry Error: {str(e)}")
                # エラー時もデフォルト値を表示
                default_data = (0, 0, 0, 0, 0, 0)
                self.progress_bar.update_from_servo_data(*default_data)

    def toggle_debug_mode(self):
        """デバッグモードの切り替え"""
        self.debug_mode = not self.debug_mode
        status = "ON" if self.debug_mode else "OFF"
        
        # ウィンドウタイトルにデバッグモードを表示
        if self.debug_mode:
            self.setWindowTitle(self.windowTitle() + " [DEBUG MODE]")
        else:
            # デバッグモードをオフにした場合、元のタイトルに戻す
            if self.connection_info:
                title = f"Vector Dive - Main Window ({self.connection_info['ip']}:{self.connection_info['port']})"
            else:
                title = "Vector Dive - Main Window"
            self.setWindowTitle(title)
            
        # テレメトリバーにデバッグモード状態を表示
        if hasattr(self, 'progress_bar') and self.progress_bar:
            self.progress_bar.telemetry_label.setText(f"DEBUG MODE: {status}")
            
    def generate_test_telemetry(self):
        """テスト用テレメトリデータを生成"""
        if not self.debug_mode:
            return
            
        # テストデータを生成（正弦波のような変化）
        import math
        self.test_data_counter += 1
        time = self.test_data_counter * 0.1
        
        # 6つのスラスター用のテストデータ
        test_data = []
        for i in range(6):
            # 各スラスターで異なる位相の正弦波
            value = int(1500 + 200 * math.sin(time + i * math.pi / 3))
            test_data.append(value)
            
        # テレメトリバーを更新
        if hasattr(self, 'progress_bar') and self.progress_bar:
            self.progress_bar.update_from_servo_data(*test_data)
            self.progress_bar.telemetry_label.setText(f"DEBUG: Test Data Generated - Counter: {self.test_data_counter}")
            
    def update_debug_telemetry(self):
        """デバッグモード用のテレメトリ更新"""
        if not self.debug_mode:
            return
            
        # テストデータを生成
        self.generate_test_telemetry()

    def reset_debug_mode(self):
        """デバッグモードをリセット"""
        self.debug_mode = False
        self.test_data_counter = 0
        
        # ウィンドウタイトルを元に戻す
        if self.connection_info:
            title = f"Vector Dive - Main Window ({self.connection_info['ip']}:{self.connection_info['port']})"
        else:
            title = "Vector Dive - Main Window"
        self.setWindowTitle(title)
        
        # テレメトリバーをリセット
        if hasattr(self, 'progress_bar') and self.progress_bar:
            default_data = (0, 0, 0, 0, 0, 0)
            self.progress_bar.update_from_servo_data(*default_data)
            self.progress_bar.telemetry_label.setText("Telemetry: Debug mode reset")
            
    def reset_position_estimation(self):
        """位置推定をリセット"""
        if hasattr(self, 'position_estimation_manager') and self.position_estimation_manager:
            self.position_estimation_manager.reset_position_estimation()
            # マップの位置マーカーもリセット
            self.update_map_position([0, 0, 0])
            print("位置推定をリセットしました")
        else:
            print("位置推定マネージャーが利用できません")
            
    def update_map_position(self, position):
        """マップに位置推定の結果を表示"""
        if not hasattr(self, 'map_scene') or position is None:
            return
            
        try:
            from PyQt5.QtGui import QPen, QBrush, QColor
            
            # スケールファクター（メートルからピクセルへの変換）
            scale_factor = 10  # 1メートル = 10ピクセル
            
            # 位置をピクセル座標に変換
            x_pixel = self.center_x + position[0] * scale_factor
            y_pixel = self.center_y - position[1] * scale_factor  # Y軸は反転
            
            # 既存のマーカーを削除
            if self.position_marker:
                self.map_scene.removeItem(self.position_marker)
            if self.position_text:
                self.map_scene.removeItem(self.position_text)
            
            # 新しいマーカーを作成
            self.position_marker = self.map_scene.addEllipse(
                x_pixel - 8, y_pixel - 8, 16, 16,
                QPen(QColor(0, 255, 0), 2),
                QBrush(QColor(0, 255, 0))
            )
            
            # 位置ラベルを作成
            self.position_text = self.map_scene.addText(f"({position[0]:.1f}, {position[1]:.1f})")
            self.position_text.setDefaultTextColor(QColor(0, 255, 0))
            self.position_text.setPos(x_pixel + 20, y_pixel - 10)
            
        except Exception as e:
            print(f"マップ位置更新エラー: {e}")

    def resize_partitions(self, telemetry_ratio=0.25, right_ratio=0.75):
        """パーティションのサイズを動的に調整する"""
        # 上部の2分割比率を調整
        total_width = self.top_splitter.width()
        telemetry_width = int(total_width * telemetry_ratio)
        right_width = total_width - telemetry_width
        
        self.top_splitter.setSizes([telemetry_width, right_width])

    def closeEvent(self, event):
        """ウィンドウが閉じられる際の処理"""
        if hasattr(self, 'telemetry_timer'):
            self.telemetry_timer.stop()
            
        # 位置推定を停止
        if hasattr(self, 'position_estimation_manager') and self.position_estimation_manager:
            self.position_estimation_manager.stop_position_estimation()
            
        event.accept()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    
    # コマンドライン引数でデバッグモードを指定可能
    debug_mode = "--debug" in sys.argv
    
    main_window = MainWindow()
    
    # デバッグモードが指定されている場合は自動的に有効化
    if debug_mode:
        main_window.debug_mode = True
        main_window.setWindowTitle(main_window.windowTitle() + " [DEBUG MODE]")
        if hasattr(main_window, 'progress_bar') and main_window.progress_bar:
            main_window.progress_bar.telemetry_label.setText("DEBUG MODE: ON (Auto-enabled)")
    
    main_window.show()
    sys.exit(app.exec_())
        