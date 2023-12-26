import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "EMAIL GOES HERE"
MY_PASSWORD = "PASSWORD HERE"
MY_LAT = 33.307575
MY_LNG = -111.844940


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # your position is within +5 or -5 degrees of the ISS position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG-5 <= iss_longitude <= MY_LNG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,  # toggles 12 hour format to 24 hour format, toggle back with value : 1
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])  # We split by the letter T into a 2 item list and further split it by index 1
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


    time_now = int(datetime.now().hour)

    if time_now <= sunrise or time_now >= sunset:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:look Up!\n\nThe ISS is above you in the sky!"
        )
