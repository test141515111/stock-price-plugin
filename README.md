# Stock Price Plugin 📈

Claude Code用の株価取得プラグイン（MCPツール統合）

## 概要

このプラグインは、Alpha Vantage APIを使用してリアルタイムの株価データを取得する**Model Context Protocol (MCP)** ツールを提供します。

Claudeに自然言語で「Amazonの株価を教えて」と尋ねると、自動的にこのツールを呼び出して最新の株価を返します。

## 機能

- **リアルタイム株価取得**: Alpha Vantage APIから最新の株価データを取得
- **MCPツール統合**: Claude Codeのツール利用機能と完全統合
- **自然言語対話**: ユーザーは自然な日本語で株価を尋ねるだけ

## 提供されるツール

### `get_stock_price`

**説明**: 指定されたティッカーシンボルの現在の株価を取得します

**パラメータ**:
- `ticker_symbol` (string, 必須): 株価を取得したい企業のティッカーシンボル
  - 例: `AMZN` (Amazon), `GOOGL` (Google), `AAPL` (Apple)

**返り値**:
```json
{
  "symbol": "AMZN",
  "price": 175.32,
  "currency": "USD",
  "change": "+2.45",
  "change_percent": "+1.42%"
}
```

## インストール

### 1. 依存関係のインストール

```bash
cd .claude/plugins/stock-price-plugin
pip install -r requirements.txt
```

### 2. プラグインをClaude Codeに認識させる

プロジェクトレベルにインストール済みです。Claude Codeを再起動すると自動的に読み込まれます。

```bash
claude
```

## 使用方法

### 基本的な質問

Claude Codeを起動して、以下のように自然言語で質問してください：

```
Amazonの株価を教えて
```

```
GoogleとAppleの株価はいくら？
```

```
Tesla (TSLA) の現在価格を知りたい
```

### Claudeの動作

1. ユーザーの質問を解析
2. 企業名をティッカーシンボルに変換（例: Amazon → AMZN）
3. `get_stock_price` ツールを呼び出し
4. 取得した株価データを自然言語で整形して回答

## 設定

### Alpha Vantage APIキー

デフォルトでAPIキー `RONQWNN6SY7YQVHH` が設定されています。

独自のAPIキーを使用したい場合は、`.mcp.json` の `env` セクションを編集してください：

```json
{
  "mcpServers": {
    "stock-price": {
      "command": "python3",
      "args": ["mcp_server.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

#### APIキーの取得方法

1. [Alpha Vantage](https://www.alphavantage.co/support/#api-key) にアクセス
2. メールアドレスを入力して「GET FREE API KEY」をクリック
3. 受信したメールからAPIキーを取得

## トラブルシューティング

### エラー: `APIレート制限に達しました`

**原因**: Alpha Vantage無料版の制限（1日500リクエスト、1分5リクエスト）

**解決策**: 1分待ってから再試行

### エラー: `無効なティッカーシンボル`

**原因**: ティッカーシンボルが存在しないか、米国市場に上場していない

**解決策**: 正しいティッカーシンボルを確認（例: Amazon = AMZN, Google = GOOGL）

### プラグインが認識されない

**解決策**:
1. プラグイン構造を確認:
   ```bash
   ls -la .claude/plugins/stock-price-plugin/
   ```
2. Claude Codeを再起動
3. MCPサーバーのログを確認

## プラグイン構造

```
stock-price-plugin/
├── .claude-plugin/
│   └── plugin.json          # プラグインメタデータ
├── .mcp.json                 # MCPサーバー設定
├── mcp_server.py             # MCPサーバー実装
├── requirements.txt          # Python依存関係
└── README.md                 # このファイル
```

## 技術的詳細

### MCPプロトコル

このプラグインはModel Context Protocol (MCP) を使用してClaude Codeと通信します：

- **通信方式**: stdio（標準入出力）
- **プロトコル**: JSON-RPC 2.0
- **サポートメソッド**:
  - `tools/list`: 利用可能なツール一覧を返却
  - `tools/call`: ツールを実行して結果を返却

### Alpha Vantage API

- **エンドポイント**: `GLOBAL_QUOTE`
- **レート制限**: 無料版 - 1日500リクエスト、1分5リクエスト
- **対応市場**: 米国株式市場（NYSE, NASDAQ）

## 参考リンク

- [Claude Code プラグインドキュメント](https://docs.claude.com/ja/docs/claude-code/plugins)
- [Alpha Vantage API](https://www.alphavantage.co/documentation/)
- [Model Context Protocol](https://docs.claude.com/ja/docs/claude-code/mcp)

## ライセンス

このプラグインは教育目的で作成されています。
