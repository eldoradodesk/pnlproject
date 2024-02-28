import requests

url = "https://public-api.birdeye.so/public/history_price?address=HxRELUQfvvjToVbacjr9YECdfQMUqGgPYB68jVDYxkbr&address_type=token&time_from=1707845866955&time_to=1707847917864"

headers = {
    "x-chain": "solana",
    "X-API-KEY": "97384de4c33b46789206f4f6837b30a6"
}

response = requests.get(url, headers=headers)

print(response.text)