import requests

food_items = ['Eggs', 'Kidney Beans', 'Pasta', 'Anchovies', 'Peppers', 'Ground Beef', 'Cream', 'Milk', 'Cheese', 'Mushrooms']
food_key = "f1ca8a6a811c4cefbcde93892da32244"

food_api = url = f'https://api.spoonacular.com/recipes/findByIngredients?apiKey={food_key}&ingredients={food_items}&number=5&limitLicense=true&ranking=2'
food_response = requests.get(url)

print(food_response.json()[0])

list = []
cols = []

print(len(food_response.json()[0]["missedIngredients"]))

for i in range(len(food_response.json())):
    print("Title: " + food_response.json()[i]["title"])
    list.append("Title: " + food_response.json()[i]["title"])
    if len(food_response.json()[i]["missedIngredients"]) == 0:
        print("no missing ingredients")
    else:
        print("Missing Ingredient: " + food_response.json()[i]["missedIngredients"][0]["name"])
        list.append("Missing Ingredient: " + food_response.json()[i]["missedIngredients"][0]["name"])
    for n in range(len(food_response.json()[i]["usedIngredients"])):
        print("Ingredients you have: " + food_response.json()[i]["usedIngredients"][n]["name"])
        list.append(("Ingredients you have: " + food_response.json()[i]["usedIngredients"][n]["name"]))
    cols.append(list)
    list = []
    print("\n")

print(cols)

