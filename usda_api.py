import requests

API_KEY = "MbvZGPVrj9P3eECrXnVpicA2xfS9Ky0LwaWrUjBR"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food/"

def search_usda_foods(query):
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 10
    }
    res = requests.get(SEARCH_URL, params=params)
    res.raise_for_status()
    return res.json().get("foods", [])

def get_usda_food_nutrition(fdc_id):
    res = requests.get(f"{FOOD_URL}{fdc_id}?api_key={API_KEY}")
    res.raise_for_status()
    food = res.json()

    # Gracefully handle missing nutrientName or value fields
    nutrients = {}
    for n in food.get("foodNutrients", []):
        name = n.get("nutrientName")
        value = n.get("value")
        if name and value is not None:
            nutrients[name] = value

    return {
        "Calories": nutrients.get("Energy", 0),
        "Protein (g)": nutrients.get("Protein", 0),
        "Fat (g)": nutrients.get("Total lipid (fat)", 0),
        "Carbs (g)": nutrients.get("Carbohydrate, by difference", 0),
        "Sugar (g)": nutrients.get("Sugars, total including NLEA", 0),
        "Fiber (g)": nutrients.get("Fiber, total dietary", 0)
    }
