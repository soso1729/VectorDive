#!/usr/bin/env python3
"""
MAVLink接続とデータ取得のテストスクリプト
"""

import sys
import os
import time
import numpy as np

# vectordiveモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mavlink_connection():
    """MAVLink接続のテスト"""
    print("MAVLink接続テストを開始します...")
    
    # テスト用の接続情報
    connection_info = {
        'ip': '0.0.0.0',  # すべてのインターフェースでリッスン
        'port': 14550,
        'mode': 'UDP'
    }
    
    try:
        from vectordive.connections.telemetry import GetTelemetry
        
        print(f"接続情報: {connection_info}")
        print("MAVLink接続を試行中...")
        
        # テレメトリインスタンスを作成
        telemetry = GetTelemetry(connection_info)
        
        # 接続状態を確認
        if telemetry.is_connected():
            print("✅ MAVLink接続が確立されました")
        else:
            print("❌ MAVLink接続に失敗しました（モックデータを使用）")
        
        # データ取得テスト（10秒間）
        print("\nデータ取得テストを開始します（10秒間）...")
        print("時間(s) | 加速度 (X, Y, Z) m/s² | サーボ出力 (1-6)")
        print("-" * 80)
        
        start_time = time.time()
        test_duration = 10
        
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # 加速度データを取得
            acc_data = telemetry.get_imu_output_acc_data()
            
            # サーボデータを取得
            servo_data = telemetry.get_servo_output_raw_data()
            
            # 結果を表示
            print(f"{current_time:6.1f} | "
                  f"({acc_data[0]:7.3f}, {acc_data[1]:7.3f}, {acc_data[2]:7.3f}) | "
                  f"({servo_data[0]:4d}, {servo_data[1]:4d}, {servo_data[2]:4d}, "
                  f"{servo_data[3]:4d}, {servo_data[4]:4d}, {servo_data[5]:4d})")
            
            time.sleep(0.5)  # 0.5秒間隔で更新
        
        print("\nテスト完了")
        
        # 最終統計
        print(f"\n最終統計:")
        print(f"接続状態: {'接続済み' if telemetry.is_connected() else '未接続'}")
        print(f"最終加速度: {acc_data}")
        print(f"最終サーボ出力: {servo_data}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def test_position_estimation_with_mavlink():
    """MAVLinkデータを使った位置推定テスト"""
    print("\nMAVLinkデータを使った位置推定テストを開始します...")
    
    # テスト用の接続情報
    connection_info = {
        'ip': '0.0.0.0',
        'port': 14550,
        'mode': 'UDP'
    }
    
    try:
        from vectordive.workers.telemetry import GetVelocityData
        
        print("GetVelocityDataインスタンスを作成中...")
        velocity_calculator = GetVelocityData(connection_info)
        print("GetVelocityDataインスタンスを作成しました")
        
        print("\n位置推定テストを開始します（10秒間）...")
        print("時間(s) | 位置 (X, Y, Z) m | 速度 (VX, VY, VZ) m/s")
        print("-" * 70)
        
        start_time = time.time()
        test_duration = 10
        
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # 位置データを取得
            position_queue, time_queue = velocity_calculator.get_position_data()
            
            if position_queue and len(position_queue) > 0:
                # 最新の位置と速度を取得
                current_position = velocity_calculator.get_current_position()
                current_velocity = velocity_calculator.get_current_velocity()
                
                # 結果を表示
                print(f"{current_time:6.1f} | "
                      f"({current_position[0]:6.3f}, {current_position[1]:6.3f}, {current_position[2]:6.3f}) | "
                      f"({current_velocity[0]:6.3f}, {current_velocity[1]:6.3f}, {current_velocity[2]:6.3f})")
            else:
                print(f"{current_time:6.1f} | データなし")
            
            time.sleep(0.5)  # 0.5秒間隔で更新
        
        print("\nテスト完了")
        print("最終結果:")
        final_position = velocity_calculator.get_current_position()
        final_velocity = velocity_calculator.get_current_velocity()
        print(f"最終位置: {final_position}")
        print(f"最終速度: {final_velocity}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def interactive_connection_test():
    """インタラクティブな接続テスト"""
    print("\nインタラクティブなMAVLink接続テスト")
    print("=" * 50)
    
    # 接続情報を入力
    ip = input("IPアドレス (デフォルト: 0.0.0.0): ").strip()
    if not ip:
        ip = "0.0.0.0"
    
    port = input("ポート番号 (デフォルト: 14550): ").strip()
    if not port:
        port = "14550"
    else:
        try:
            port = int(port)
        except ValueError:
            print("無効なポート番号です")
            return
    
    connection_info = {
        'ip': ip,
        'port': port,
        'mode': 'UDP'
    }
    
    print(f"\n接続情報: {connection_info}")
    print("MAVLinkデータを受信する準備ができました")
    print("Ctrl+C で停止してください")
    
    try:
        from vectordive.connections.telemetry import GetTelemetry
        
        telemetry = GetTelemetry(connection_info)
        
        if telemetry.is_connected():
            print("✅ MAVLink接続が確立されました")
        else:
            print("❌ MAVLink接続に失敗しました（モックデータを使用）")
        
        print("\nリアルタイムデータ受信を開始...")
        print("時間(s) | 加速度 (X, Y, Z) m/s²")
        print("-" * 50)
        
        start_time = time.time()
        
        while True:
            current_time = time.time() - start_time
            
            # 加速度データを取得
            acc_data = telemetry.get_imu_output_acc_data()
            
            # 結果を表示
            print(f"{current_time:6.1f} | ({acc_data[0]:7.3f}, {acc_data[1]:7.3f}, {acc_data[2]:7.3f})")
            
            time.sleep(1.0)  # 1秒間隔で更新
            
    except KeyboardInterrupt:
        print("\n\nテストを停止しました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("MAVLink接続とデータ取得のテスト")
    print("=" * 50)
    
    print("1. 基本的なMAVLink接続テスト")
    print("2. MAVLinkデータを使った位置推定テスト")
    print("3. インタラクティブな接続テスト")
    
    choice = input("選択してください (1, 2, or 3): ").strip()
    
    if choice == "1":
        test_mavlink_connection()
    elif choice == "2":
        test_position_estimation_with_mavlink()
    elif choice == "3":
        interactive_connection_test()
    else:
        print("無効な選択です")
