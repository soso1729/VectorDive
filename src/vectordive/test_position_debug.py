#!/usr/bin/env python3
"""
位置推定機能のデバッグテストスクリプト
"""

import sys
import os
import time
import numpy as np

# vectordiveモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_position_estimation():
    """位置推定機能のテスト"""
    print("位置推定機能のテストを開始します...")
    
    try:
        from vectordive.workers.telemetry import GetVelocityData
        
        # テスト用の接続情報
        connection_info = {
            'ip': 'localhost',
            'port': 14550
        }
        
        print("GetVelocityDataインスタンスを作成中...")
        velocity_calculator = GetVelocityData(connection_info)
        print("GetVelocityDataインスタンスを作成しました")
        
        print("\n位置推定テストを開始します（10秒間）...")
        print("時間(s) | 位置 (X, Y, Z) | 速度 (VX, VY, VZ)")
        print("-" * 60)
        
        start_time = time.time()
        test_duration = 10  # 10秒間テスト
        
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
        
        # リセットテスト
        print("\nリセットテストを実行...")
        velocity_calculator.reset_integration()
        reset_position = velocity_calculator.get_current_position()
        reset_velocity = velocity_calculator.get_current_velocity()
        print(f"リセット後位置: {reset_position}")
        print(f"リセット後速度: {reset_velocity}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

def test_telemetry_connection():
    """テレメトリ接続のテスト"""
    print("\nテレメトリ接続のテストを開始します...")
    
    try:
        from vectordive.connections.telemetry import GetTelemetry
        
        # テスト用の接続情報
        connection_info = {
            'ip': 'localhost',
            'port': 14550
        }
        
        print("GetTelemetryインスタンスを作成中...")
        telemetry = GetTelemetry(connection_info)
        print("GetTelemetryインスタンスを作成しました")
        
        print(f"接続状態: {'接続済み' if telemetry.is_connected() else '未接続（モックデータ使用）'}")
        
        # 加速度データを取得
        print("\n加速度データのテスト（5秒間）...")
        print("時間(s) | 加速度 (X, Y, Z)")
        print("-" * 40)
        
        start_time = time.time()
        test_duration = 5  # 5秒間テスト
        
        while time.time() - start_time < test_duration:
            current_time = time.time() - start_time
            
            # 加速度データを取得
            acc_data = telemetry.get_imu_output_acc_data()
            
            print(f"{current_time:6.1f} | ({acc_data[0]:6.3f}, {acc_data[1]:6.3f}, {acc_data[2]:6.3f})")
            
            time.sleep(0.5)  # 0.5秒間隔で更新
        
        print("テレメトリテスト完了")
        
    except Exception as e:
        print(f"テレメトリエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("位置推定機能のデバッグテスト")
    print("=" * 50)
    
    # テレメトリ接続テスト
    test_telemetry_connection()
    
    # 位置推定テスト
    test_position_estimation()
    
    print("\nすべてのテストが完了しました")
