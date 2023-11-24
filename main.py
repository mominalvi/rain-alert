import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv
load_dotenv()

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {"https": os.environ['https_proxy']}

api_key = os.getenv('API_KEY')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

parameters = {
    "lat": 43.325520,
    "lon": -79.799034,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get("https://api.openweathermap.org/data/2.8/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
first_12_hours = weather_data["hourly"][:12]

will_rain = False

for hour_data in first_12_hours:
    if hour_data["weather"][0]["id"] < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella ☔️",
        from_='+19388887294',
        to='+16475078485'
    )
    print(message.status)

