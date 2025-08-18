# VectorDive

A PyQt5-based GUI application for ROV (Remotely Operated Vehicle) control and telemetry monitoring.

## Overview

VectorDive is a comprehensive GUI application designed for controlling and monitoring ROV systems. It provides real-time telemetry data visualization, thruster control, depth monitoring, and connection management through a modern, user-friendly interface.

## Features

### 🎮 **Main Interface**
- **Real-time Telemetry Display**: Monitor 6 thruster outputs with live progress bars
- **Depth Graph**: Visual depth tracking over time
- **Interactive Map**: Grid-based positioning system with center point marking
- **Log Console**: Real-time logging and status updates

### 🔌 **Connection Management**
- **UDP/Serial Support**: Connect via UDP or Serial communication
- **Heartbeat Monitoring**: Automatic connection health checks
- **Configurable Settings**: IP address and port configuration
- **Connection Status**: Real-time connection state display

### 🎛️ **Control Features**
- **Thruster Control**: Individual control of 6 thrusters (T1-T6)
- **MAVLink Integration**: Compatible with MAVLink protocol
- **Servo Output Monitoring**: Real-time servo position tracking (1100-1900 range)

### 🛠️ **Debug Features**
- **Debug Mode**: Toggle with `Ctrl+Shift+D`
- **Test Data Generation**: Generate simulated telemetry with `Ctrl+Shift+T`
- **Reset Functionality**: Reset debug state with `Ctrl+Shift+R`
- **Auto Debug Mode**: Launch with `--debug` flag

## Project Structure

```
vectordive/
├── app.py                 # Main application entry point
├── config/               # Configuration files
│   ├── base.py          # Base configuration constants
│   ├── dev.py           # Development settings
│   └── prod.py          # Production settings
├── connections/          # Connection management
│   ├── hb_wait.py       # Heartbeat monitoring
│   └── telemetry.py     # MAVLink telemetry interface
├── services/            # Core services
│   └── mavlink_client.py # MAVLink client implementation
├── ui/                  # User interface components
│   ├── entrance_window.py # Connection setup window
│   ├── main_window.py   # Main application window
│   ├── test_window.py   # Testing interface
│   └── widgets/         # Reusable UI components
│       ├── attitude_view.py
│       ├── combo_box.py
│       ├── depth_graph.py
│       ├── line_edit.py
│       ├── log_console.py
│       ├── push_box.py
│       ├── telemetry_bars.py
│       ├── test_depth_graph.py
│       └── thruster_control.py
└── workers/             # Background processing
    ├── connection.py    # Connection worker threads
    └── telemetry.py     # Telemetry processing
```

## Installation

### Prerequisites
- Python 3.10 or higher
- PyQt5
- pymavlink

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd VectorDive
```

2. Install dependencies:
```bash
pip install PyQt5 pymavlink
```

3. Run the application:
```bash
python src/vectordive/app.py
```

## Usage

### Starting the Application
1. Launch the application - the entrance window will appear
2. Configure connection settings:
   - **Connection Mode**: Select UDP or Serial
   - **IP Address**: Enter target IP (default: 0.0.0.0)
   - **Port**: Enter port number (default: 14550)
3. Click "Connect" to establish connection
4. The main window will open automatically

### Main Interface Navigation
- **Left Panel**: Future features (Navigation, Settings, Status, Control Panel)
- **Right Panel**: Main content area
  - **Top Section**: Telemetry bars and depth graph
  - **Bottom Section**: Log console

### Debug Features
- **Debug Mode**: Press `Ctrl+Shift+D` to toggle debug mode
- **Test Data**: Press `Ctrl+Shift+T` to generate test telemetry data
- **Reset**: Press `Ctrl+Shift+R` to reset debug state
- **Auto Debug**: Launch with `python app.py --debug`

### Telemetry Monitoring
- **Thruster Outputs**: Real-time display of 6 thruster values (T1-T6)
- **Value Range**: 1100-1900 (default: 1500)
- **Connection Status**: Displayed in telemetry section
- **Error Handling**: Automatic fallback to default values on connection issues

## Configuration

### Connection Settings
- **Default IP**: 0.0.0.0
- **Default Port**: 14550
- **Heartbeat Timeout**: 7.5 seconds
- **Supported Modes**: UDP, Serial

### Thruster Configuration
- **Minimum Value**: 1100
- **Maximum Value**: 1900
- **Default Value**: 1500
- **Number of Thrusters**: 6

### Graph Settings
- **Depth Graph Title**: "Depth Graph"
- **X-Axis**: Time (seconds)
- **Y-Axis**: Depth (meters)
- **Initial Range**: X[0-60], Y[0-100]
- **Minimum Size**: 200x400 pixels

## Development

### Project Setup
The project uses Poetry for dependency management:
```bash
poetry install
poetry run python src/vectordive/app.py
```

### Code Structure
- **Modular Design**: Separated into logical modules (UI, connections, services)
- **Widget System**: Reusable UI components in `ui/widgets/`
- **Configuration Management**: Environment-specific configs in `config/`
- **Worker Threads**: Background processing in `workers/`

### Testing
- Run tests: `poetry run pytest`
- Test directory: `tests/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT-based License - see [LICENSE](LICENSE) file for details.

## Author

**SoSato** - satou5473@gmail.com

## Support

For issues and questions:
1. Check the debug console for error messages
2. Verify MAVLink connection settings
3. Ensure proper network connectivity
4. Review log console for detailed status information

---

# VectorDive（日本語版）

ROV（遠隔操作無人潜水機）の制御とテレメトリ監視のためのPyQt5ベースのGUIアプリケーション。

## 概要

VectorDiveは、ROVシステムの制御と監視のために設計された包括的なGUIアプリケーションです。リアルタイムのテレメトリデータ可視化、スラスター制御、深度監視、接続管理を現代的なユーザーフレンドリーなインターフェースで提供します。

## 機能

### 🎮 **メインインターフェース**
- **リアルタイムテレメトリ表示**: 6つのスラスター出力をライブプログレスバーで監視
- **深度グラフ**: 時間経過による視覚的な深度追跡
- **インタラクティブマップ**: 中心点マーキング付きのグリッドベース位置システム
- **ログコンソール**: リアルタイムログとステータス更新

### 🔌 **接続管理**
- **UDP/シリアル対応**: UDPまたはシリアル通信で接続
- **ハートビート監視**: 自動接続健全性チェック
- **設定可能**: IPアドレスとポート設定
- **接続状態**: リアルタイム接続状態表示

### 🎛️ **制御機能**
- **スラスター制御**: 6つのスラスター（T1-T6）の個別制御
- **MAVLink統合**: MAVLinkプロトコル対応
- **サーボ出力監視**: リアルタイムサーボ位置追跡（1100-1900範囲）

### 🛠️ **デバッグ機能**
- **デバッグモード**: `Ctrl+Shift+D`で切り替え
- **テストデータ生成**: `Ctrl+Shift+T`でシミュレーションテレメトリ生成
- **リセット機能**: `Ctrl+Shift+R`でデバッグ状態リセット
- **自動デバッグモード**: `--debug`フラグで起動

## プロジェクト構造

```
vectordive/
├── app.py                 # メインアプリケーションエントリーポイント
├── config/               # 設定ファイル
│   ├── base.py          # 基本設定定数
│   ├── dev.py           # 開発設定
│   └── prod.py          # 本番設定
├── connections/          # 接続管理
│   ├── hb_wait.py       # ハートビート監視
│   └── telemetry.py     # MAVLinkテレメトリインターフェース
├── services/            # コアサービス
│   └── mavlink_client.py # MAVLinkクライアント実装
├── ui/                  # ユーザーインターフェースコンポーネント
│   ├── entrance_window.py # 接続設定ウィンドウ
│   ├── main_window.py   # メインアプリケーションウィンドウ
│   ├── test_window.py   # テストインターフェース
│   └── widgets/         # 再利用可能なUIコンポーネント
│       ├── attitude_view.py
│       ├── combo_box.py
│       ├── depth_graph.py
│       ├── line_edit.py
│       ├── log_console.py
│       ├── push_box.py
│       ├── telemetry_bars.py
│       ├── test_depth_graph.py
│       └── thruster_control.py
└── workers/             # バックグラウンド処理
    ├── connection.py    # 接続ワーカースレッド
    └── telemetry.py     # テレメトリ処理
```

## インストール

### 前提条件
- Python 3.10以上
- PyQt5
- pymavlink

### セットアップ
1. リポジトリをクローン:
```bash
git clone <repository-url>
cd VectorDive
```

2. 依存関係をインストール:
```bash
pip install PyQt5 pymavlink
```

3. アプリケーションを実行:
```bash
python src/vectordive/app.py
```

## 使用方法

### アプリケーション起動
1. アプリケーションを起動 - エントランスウィンドウが表示されます
2. 接続設定を構成:
   - **接続モード**: UDPまたはシリアルを選択
   - **IPアドレス**: ターゲットIPを入力（デフォルト: 0.0.0.0）
   - **ポート**: ポート番号を入力（デフォルト: 14550）
3. 「Connect」をクリックして接続を確立
4. メインウィンドウが自動的に開きます

### メインインターフェースナビゲーション
- **左パネル**: 将来の機能（ナビゲーション、設定、ステータス、制御パネル）
- **右パネル**: メインコンテンツエリア
  - **上部セクション**: テレメトリバーと深度グラフ
  - **下部セクション**: ログコンソール

### デバッグ機能
- **デバッグモード**: `Ctrl+Shift+D`を押してデバッグモードを切り替え
- **テストデータ**: `Ctrl+Shift+T`を押してテストテレメトリデータを生成
- **リセット**: `Ctrl+Shift+R`を押してデバッグ状態をリセット
- **自動デバッグ**: `python app.py --debug`で起動

### テレメトリ監視
- **スラスター出力**: 6つのスラスター値（T1-T6）のリアルタイム表示
- **値の範囲**: 1100-1900（デフォルト: 1500）
- **接続状態**: テレメトリセクションに表示
- **エラー処理**: 接続問題時にデフォルト値に自動フォールバック

## 設定

### 接続設定
- **デフォルトIP**: 0.0.0.0
- **デフォルトポート**: 14550
- **ハートビートタイムアウト**: 7.5秒
- **対応モード**: UDP、シリアル

### スラスター設定
- **最小値**: 1100
- **最大値**: 1900
- **デフォルト値**: 1500
- **スラスター数**: 6

### グラフ設定
- **深度グラフタイトル**: "Depth Graph"
- **X軸**: 時間（秒）
- **Y軸**: 深度（メートル）
- **初期範囲**: X[0-60]、Y[0-100]
- **最小サイズ**: 200x400ピクセル

## 開発

### プロジェクトセットアップ
プロジェクトはPoetryを使用して依存関係管理を行います:
```bash
poetry install
poetry run python src/vectordive/app.py
```

### コード構造
- **モジュラー設計**: 論理モジュール（UI、接続、サービス）に分離
- **ウィジェットシステム**: `ui/widgets/`の再利用可能なUIコンポーネント
- **設定管理**: `config/`の環境固有設定
- **ワーカースレッド**: `workers/`のバックグラウンド処理

### テスト
- テスト実行: `poetry run pytest`
- テストディレクトリ: `tests/`

## 貢献

1. リポジトリをフォーク
2. 機能ブランチを作成
3. 変更を加える
4. 該当する場合はテストを追加
5. プルリクエストを提出

## ライセンス

MITベースライセンス - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 作者

**SoSato** - satou5473@gmail.com

## サポート

問題や質問がある場合:
1. デバッグコンソールでエラーメッセージを確認
2. MAVLink接続設定を確認
3. 適切なネットワーク接続を確保
4. 詳細なステータス情報についてはログコンソールを確認
