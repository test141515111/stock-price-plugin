#!/usr/bin/env python3
"""
Stock Price MCP Server
Alpha Vantage APIを使用して株価データを取得するMCPサーバー
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "RONQWNN6SY7YQVHH")


def get_stock_price(ticker_symbol: str) -> dict:
    """Alpha Vantage APIから株価を取得"""
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker_symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            return {"error": f"無効なティッカーシンボル: {ticker_symbol}"}

        if "Note" in data:
            return {"error": "APIレート制限に達しました"}

        quote = data.get("Global Quote", {})
        if not quote:
            return {"error": f"株価データが見つかりません: {ticker_symbol}"}

        return {
            "symbol": ticker_symbol,
            "price": float(quote.get("05. price", 0)),
            "currency": "USD",
            "change": quote.get("09. change", "N/A"),
            "change_percent": quote.get("10. change percent", "N/A")
        }

    except Exception as e:
        return {"error": str(e)}


def handle_request(request: dict) -> dict:
    """MCPリクエストを処理"""
    method = request.get("method")

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "get_stock_price",
                    "description": "指定されたティッカーシンボルの現在の株価を取得します",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "ticker_symbol": {
                                "type": "string",
                                "description": "株価を取得したい企業のティッカーシンボル（例: AMZN, GOOGL）"
                            }
                        },
                        "required": ["ticker_symbol"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})

        if tool_name == "get_stock_price":
            result = get_stock_price(arguments.get("ticker_symbol"))
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, ensure_ascii=False)
                    }
                ]
            }

    return {"error": "Unknown method"}


def main():
    """MCPサーバーのメインループ"""
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)

            # JSONRPCレスポンス形式
            output = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": response
            }

            print(json.dumps(output), flush=True)

        except Exception as e:
            error_output = {
                "jsonrpc": "2.0",
                "id": request.get("id", None),
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_output), flush=True)


if __name__ == "__main__":
    main()
