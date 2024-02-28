from moralis import sol_api
from datetime import datetime
import sqlite3
import os.path
import time
from requests import Session
import os
import json

# ====================== CONSTANT ==========================

WALLET_ADDRESS = "EhP6VtW3jPjoZ475rpxDZbxzq7pdWSsuhtcyktpZ3Xrb"
MORALIS_API_KEY = "vCgsJoVqrb1n2Yoi8H6HGGyPrtO3yqt0ZD7wcvcInp0alTk2KXfxUOGryBfYg3jv"
COINMARKETCAP_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
COINMARKETCAP_API_KEY = "24d06be6-dbcc-4bd3-bf24-c4f156546917"

# ==========================================================

address = WALLET_ADDRESS
api_key = MORALIS_API_KEY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "solana.db")
with sqlite3.connect(db_path, check_same_thread=False) as con:
    cur = con.cursor()

sql_create_pnl_table  = "CREATE TABLE IF NOT EXISTS pnl (id integer PRIMARY KEY AUTOINCREMENT,wallet text NOT NULL,price float,current_time text NOT NULL, timestamp text NOT NULL);"

if con is not None:
    cur.execute(sql_create_pnl_table)
else:
    print("Error! cannot create the database connection.")

params = {
"network": "mainnet",
"address": address
}

def doCal():   
    
    # =================== GET market sol price ================================
    url = COINMARKETCAP_URL # Coinmarketcap API url
    api = COINMARKETCAP_API_KEY # Replace this with your API key
    parameters = { 'slug': 'solana', 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api
    } # Headers for the API request

    session = Session() # Create new session object to manage API requests
    session.headers.update(headers) # Update the session headers with the specified headers

    response = session.get(url, params = parameters) # Receiving the response from the API
    
    # print('NUMBER', json.loads(response.text)['data'])
    sol_price = json.loads(response.text)['data']['5426']['quote']['USD']['price']
    
    # ==================== GET all tokens ====================================
        
    timestamp    = datetime.now().timestamp()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    result  = sol_api.account.get_portfolio(
    api_key = api_key,
    params  = params,
    )
    native_token = result['nativeBalance']
    spl_tokens   = result['tokens']

    print("Symbol, balance, eachPrice, price, TotalPrice")
    price = 0
    for i in spl_tokens:
        tokenAddress = i["mint"]
        params1 = {
            "network": "mainnet",
            "address": tokenAddress
        }
        try:
            response = sol_api.token.get_token_price(
                api_key = api_key,
                params  = params1
            )
            # print(i['symbol'], i['mint'], response)
            # if response['usdPrice'] is not None:
            # print(float(i['amount']) * float(response['usdPrice']))
            price += float(i['amount']) * float(response['usdPrice'])
            print(i['symbol'], float(i['amount']), float(response['usdPrice']), float(i['amount']) * float(response['usdPrice']), price)
            # break
        except:
            continue
            # break
    
    price += float(native_token['solana']) * float(sol_price)

    print("Native-Token", native_token['solana'], sol_price, float(native_token['solana']) * float(sol_price), price)
    
    print("price", price)
    sql = "INSERT INTO pnl(wallet, price, timestamp, current_time) VALUES(?, ?, ?, ?)"

    cur.execute(sql, (address, price, timestamp, current_time))
 

    con.commit()
    print('success')

# doCal()
while True:
    doCal()
    time.sleep(60 * 5) # gain wallet price per 5 minutes 
# con.close()