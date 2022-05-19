import string

import cv2
import numpy as np
import requests
import io
import json
import regex as re
from flask import jsonify

path = r'C:\Users\andre\Documents\School Work\OtherCourses\OpenCVProject\mum.jpg'
img = cv2.imread(path)

cv2.imshow("image", img)
cv2.waitKey()

url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", img)
file_bytes = io.BytesIO(compressedimage)

results = requests.post(url_api,
              files={"mum.jpg": file_bytes},
              data = {"apikey": "K81767946788957"})

results = results.content.decode()
results = json.loads(results)

text_detected = results.get("ParsedResults")[0].get("ParsedText")


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

food_items = []
shortword = re.compile(r'\W*\b\w{1,3}\b')


for line in text_detected.splitlines():
    if not has_numbers(line) and not line.isupper():
        line = (shortword.sub('', line))
        food_items.append((re.sub(r'\d+', '', line)))

food_items = food_items[3:]

print(food_items)
food_key = "f1ca8a6a811c4cefbcde93892da32244"

food_api = url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={food_key}&ingredients={food_items}&number=5&limitLicense=true&ranking=2'
food_response = requests.get(url)

print(food_response)




