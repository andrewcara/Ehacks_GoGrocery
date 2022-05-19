import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import string
import cv2
import numpy as np
import io
import json
import regex as re

__author__ = 'ibininja'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return redirect(url_for('picture'))


@app.route("/picture")
def picture():
    path = r'C:\Users\andre\Documents\School Work\OtherCourses\OpenCVProject\final.jpg'
    img = cv2.imread(path)

    url_api = "https://api.ocr.space/parse/image"
    _, compressedimage = cv2.imencode(".jpg", img)
    file_bytes = io.BytesIO(compressedimage)

    results = requests.post(url_api,
                            files={"final.jpg": file_bytes},
                            data={"apikey": "K81767946788957"})

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
    food_items = food_response

    food_key = "f1ca8a6a811c4cefbcde93892da32244"

    print(food_response.json()[0])

    list = []
    cols = []

    print(len(food_response.json()[0]["missedIngredients"]))

    for i in range(len(food_response.json())):
        list.append("Title: " + food_response.json()[i]["title"])
        if len(food_response.json()[i]["missedIngredients"]) == 0:
            print("no missing ingredients")
        else:
            list.append("Missing Ingredient: " + food_response.json()[i]["missedIngredients"][0]["name"])
        for n in range(len(food_response.json()[i]["usedIngredients"])):
            list.append(("Ingredients you have: " + food_response.json()[i]["usedIngredients"][n]["name"]))
        cols.append(list)
        list = []

    return jsonify(cols)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
