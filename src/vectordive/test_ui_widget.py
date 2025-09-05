#!/usr/bin/env python3
"""
UIウィジェットのデバッグテストスクリプト
"""

import sys
import os
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

# vectordiveモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_position_estimation_widget():
    """位置推定ウィジェットのテスト"""
    print("位置推定UIウィジェットのテストを開始します...")
    
    try:
        from vectordive.ui.widgets.position_estimation import PositionEstimationWidget
        
        # QApplicationを作成
        app = QApplication(sys.argv)
        
        # メインウィンドウを作成
        main_window = QMainWindow()
        main_window.setWindowTitle("位置推定ウィジェットテスト")
        main_window.setGeometry(100, 100, 400, 600)
        
        # 中央ウィジェットを作成
        central_widget = QWidget()
        main_window.setCentralWidget(central_widget)
        
        # レイアウトを作成
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 位置推定ウィジェットを作成
        print("位置推定ウィジェットを作成中...")
        position_widget = PositionEstimationWidget()
        layout.addWidget(position_widget)
        
        # ウィンドウを表示
        main_window.show()
        print("位置推定ウィジェットを表示しました")
        
        # テストデータを生成して更新
        def update_test_data():
            import math
            current_time = time.time()
            
            # テスト用の位置データを生成
            test_position = [
                2.0 * math.sin(current_time * 0.5),
                1.5 * math.cos(current_time * 0.3),
                0.5 * math.sin(current_time * 0.2)
            ]
            
            # テスト用の速度データを生成
            test_velocity = [
                1.0 * math.cos(current_time * 0.5),
                -0.45 * math.sin(current_time * 0.3),
                0.1 * math.cos(current_time * 0.2)
            ]
            
            # UIを更新
            position_widget.update_position(test_position)
            position_widget.update_velocity(test_velocity)
            
            # 状態を更新
            status_text = f"テスト実行中 - 時間: {current_time:.1f}s"
            position_widget.update_status(status_text, "#4CAF50")
        
        # タイマーを設定して定期的に更新
        timer = QTimer()
        timer.timeout.connect(update_test_data)
        timer.start(100)  # 100ms間隔で更新
        
        print("テストデータの更新を開始しました（10秒間）")
        print("ウィンドウを閉じるか、10秒後に自動終了します")
        
        # 10秒後に自動終了
        def auto_exit():
            print("テスト完了")
            app.quit()
        
        exit_timer = QTimer()
        exit_timer.timeout.connect(auto_exit)
        exit_timer.start(10000)  # 10秒後に終了
        
        # アプリケーションを実行
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def test_position_estimation_manager():
    """位置推定マネージャーのテスト"""
    print("\n位置推定マネージャーのテストを開始します...")
    
    try:
        from vectordive.ui.widgets.position_estimation import PositionEstimationManager
        
        # テスト用の接続情報
        connection_info = {
            'ip': 'localhost',
            'port': 14550
        }
        
        # QApplicationを作成
        app = QApplication(sys.argv)
        
        # メインウィンドウを作成
        main_window = QMainWindow()
        main_window.setWindowTitle("位置推定マネージャーテスト")
        main_window.setGeometry(100, 100, 400, 600)
        
        # 中央ウィジェットを作成
        central_widget = QWidget()
        main_window.setCentralWidget(central_widget)
        
        # レイアウトを作成
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 位置推定マネージャーを作成
        print("位置推定マネージャーを作成中...")
        position_manager = PositionEstimationManager(connection_info)
        layout.addWidget(position_manager.get_widget())
        
        # ウィンドウを表示
        main_window.show()
        print("位置推定マネージャーを表示しました")
        
        # 5秒後にリセットテスト
        def reset_test():
            print("リセットテストを実行...")
            position_manager.reset_position_estimation()
        
        reset_timer = QTimer()
        reset_timer.timeout.connect(reset_test)
        reset_timer.start(5000)  # 5秒後にリセット
        
        # 10秒後に自動終了
        def auto_exit():
            print("マネージャーテスト完了")
            app.quit()
        
        exit_timer = QTimer()
        exit_timer.timeout.connect(auto_exit)
        exit_timer.start(10000)  # 10秒後に終了
        
        # アプリケーションを実行
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("UIウィジェットのデバッグテスト")
    print("=" * 50)
    
    # テストの選択
    print("1. 位置推定ウィジェットテスト")
    print("2. 位置推定マネージャーテスト")
    
    choice = input("選択してください (1 or 2): ").strip()
    
    if choice == "1":
        test_position_estimation_widget()
    elif choice == "2":
        test_position_estimation_manager()
    else:
        print("無効な選択です")
