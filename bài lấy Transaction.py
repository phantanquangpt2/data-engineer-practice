import requests
import pandas as pd
import sqlite3
from datetime import datetime

ETHERSCAN_KEY = "expl_bd3oLn4q6JArCtJTDBYHh1HCknsi3lOG"

# ===== BITCOIN =====
def get_bitcoin_transactions():
    response = requests.get("https://blockchain.info/latestblock")
    block_hash = response.json()["hash"]
    
    response2 = requests.get(f"https://blockchain.info/rawblock/{block_hash}")
    block_data = response2.json()
    
    transactions = []
    for tx in block_data["tx"][:10]:
        transactions.append({
            "hash":      tx["hash"],
            "time":      datetime.fromtimestamp(tx["time"]).strftime("%Y-%m-%d %H:%M:%S"),
            "n_inputs":  len(tx["inputs"]),
            "n_outputs": len(tx["out"]),
            "total_btc": sum(o["value"] for o in tx["out"]) / 100000000
        })
    return pd.DataFrame(transactions)

# ===== ETHEREUM =====
def get_ethereum_transactions():
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": ["latest", True],
        "id": 1
    }
    headers = {"Content-Type": "application/json"}

    # Danh sách RPC công khai để thử lần lượt
    endpoints = [
        "https://eth.llamarpc.com",
        "https://rpc.ankr.com/eth",
        "https://cloudflare-eth.com",
        "https://ethereum-rpc.publicnode.com",
    ]

    data = None
    for url in endpoints:
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"[{url}] status={response.status_code}")
            if response.status_code != 200:
                continue
            data = response.json()
            if data.get("result"):
                print(f"-> Dùng thành công endpoint: {url}")
                break
        except Exception as e:
            print(f"[{url}] lỗi: {e}")
            continue

    if not data or not data.get("result"):
        raise RuntimeError(f"Không lấy được dữ liệu từ bất kỳ RPC nào. Response cuối: {data}")

    txs = data["result"]["transactions"]

    transactions = []
    for tx in txs[:10]:
        transactions.append({
            "hash":      tx["hash"],
            "from":      tx["from"],
            "to":        tx["to"],
            "value_eth": int(tx["value"], 16) / 10**18
        })
    return pd.DataFrame(transactions)

# ===== LƯU VÀO SQLITE =====
conn = sqlite3.connect("transactions.db")

df_btc = get_bitcoin_transactions()
df_btc.to_sql("bitcoin", conn, if_exists="replace", index=False)
print("Bitcoin:")
print(df_btc)

df_eth = get_ethereum_transactions()
df_eth.to_sql("ethereum", conn, if_exists="replace", index=False)
print("\nEthereum:")
print(df_eth)

conn.close()
print("\nLuu 2 bang xong!")
