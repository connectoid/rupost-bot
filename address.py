# -*- coding: utf-8 -*-

import requests
import base64
import json

def to_base64(str):
	return base64.b64encode(str.encode()).decode("utf-8")

#properties
access_token	= "TestAccessToken"
login_password	= to_base64("login:password")
protocol 	= "https://"
host 		= "otpravka-api.pochta.ru"

postalCode 	= "115127"

request_headers = {
	"Content-Type": "application/json",
	"Accept": "application/json;charset=UTF-8",
	"Authorization": "AccessToken " + access_token,
	"X-User-Authorization": "Basic " + login_password
}

path = "/postoffice/1.0/" + postalCode

url = protocol + host + path

response = requests.get(url, headers=request_headers)
print("Status code: ", response.status_code)
print("Response body: ", response.text)