import requests
from datetime import datetime

MY_LAT = 33.307575
MY_LNG = -111.844940

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,  # toggles 12 hour format to 24 hour format, toggle back with value : 1
}

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# your position is within +5 or -5 degrees of the ISS position

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])  # We split by the letter T into a 2 item list and further split it by index 1
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
print(sunrise)
print(sunset)

time_now = datetime.now()

print(time_now.hour)
