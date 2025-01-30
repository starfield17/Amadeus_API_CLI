# DeepSeek Chat CLI

DeepSeek Chat CLIは、コマンドラインから直接DeepSeek APIと対話できる高機能なチャットインターフェースです。

## 特徴

- インタラクティブなチャット機能
- チャット履歴の保存と読み込み
- コードのシンタックスハイライト
- プロキシサポート
- キーボードショートカット
- 推論チェーンの表示

## 必要条件

- Python 3.7以上
- pip（Pythonパッケージマネージャー）
- DeepSeek APIキー

## インストール方法

1. 必要なパッケージをインストールします：

```bash
pip install openai httpx httpx_socks rich prompt_toolkit pygments pyperclip
```

2. ソースコードをダウンロードまたはクローンします：

```bash
git clone <repository-url>
cd deepseek-chat-cli
```

## 設定

1. DeepSeek APIキーを取得します（https://platform.deepseek.com）

2. 以下のいずれかの方法でAPIキーを設定できます：
   - 初回起動時に対話的に入力
   - コマンドライン引数で指定
   - 設定ファイルに保存（`~/.deepseek_config`）

## 使用方法

### 基本的な起動

```bash
python deepseek_api.py
```

### コマンドライン引数の使用

```bash
python deepseek_api.py --api-key YOUR_API_KEY --model deepseek-reasoner --proxy socks5://127.0.0.1:7890
```

### 利用可能なコマンドライン引数

- `--api-key`: DeepSeek APIキー
- `--model`: 使用するモデル（デフォルト: deepseek-reasoner）
- `--proxy`: プロキシサーバーアドレス（例: socks5://127.0.0.1:7890）

## チャットコマンド

- `/clear`: チャット履歴をクリア
- `/save [ファイル名]`: チャット履歴を保存
- `/load [ファイル名]`: チャット履歴を読み込み
- `/help`: ヘルプメッセージを表示

## キーボードショートカット

- `Enter`: 新しい行を開始
- `Ctrl+D`: メッセージを送信
- `Ctrl+V`: クリップボードからテキストを貼り付け
- `Ctrl+Z`: テキストの変更を元に戻す
- `Ctrl+Y`: 元に戻した変更をやり直す
- `↑/↓`: コマンド履歴をナビゲート

## トラブルシューティング

### よくある問題と解決方法

1. APIキーエラー
   - APIキーが正しく設定されているか確認
   - DeepSeekダッシュボードでAPIキーの有効性を確認

2. プロキシ接続エラー
   - プロキシサーバーが稼働しているか確認
   - プロキシのフォーマットが正しいか確認（例：socks5://127.0.0.1:7890）

3. パッケージのインストールエラー
   - Pythonのバージョンが3.7以上であることを確認
   - pip を最新バージョンに更新：`pip install --upgrade pip`
   - 必要に応じて仮想環境を使用

### エラーメッセージの意味

- "API Error": APIキーまたはネットワーク接続の問題
- "Failed to save config": 設定ファイルの保存権限の問題
- "File not found": 指定されたチャット履歴ファイルが存在しない

## セキュリティ注意事項

- APIキーは安全に保管し、共有しないでください
- 設定ファイル（`.deepseek_config`）のパーミッションは自動的に600に設定されます
- チャット履歴には機密情報が含まれる可能性があるため、適切に管理してください

## サポートとコントリビューション

バグ報告や機能リクエストは、GitHubのIssuesページでお願いします。
プルリクエストも歓迎します。
