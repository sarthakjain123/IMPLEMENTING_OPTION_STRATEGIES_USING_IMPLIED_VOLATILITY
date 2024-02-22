import requests

# Define the Binance API endpoint for fetching option data "startTime" : "1694667744"
base_api_url = "https://www.binance.com/en/eoptions/BTCUSDT?symbol=BTC-231014-26750-C" 

# Pass an API key in headers
headers = {
    'X-MBX-APIKEY': 'q5OpDbcs15GWlY23sAuAJWavrkvziGGTl0LTgdUiWOCK5HaoDBkyCvLzACuQpryG'
}
parameters = {     
    "symbol" : "BTC-231014-26500-C",
    "interval": "5m"
    }

# Make the HTTP GET request
response = requests.get(base_api_url)#, params = parameters, headers=headers)
print(response)

print(response.content)

folder_path = "D:\Major_1/test"