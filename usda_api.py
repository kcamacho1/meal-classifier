import requests

API_KEY = "MbvZGPVrj9P3eECrXnVpicA2xfS9Ky0LwaWrUjBR"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food/"

REQUIRED_NUTRIENTS = [
    "Energy",
    "Protein",
    "Total lipid (fat)",
    "Carbohydrate, by difference",
    "Sugars, total including NLEA",
    "Fiber, total dietary"
]

def search_usda_foods(query):
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 10
    }
    res = requests.get(SEARCH_URL, params=params)
    res.raise_for_status()
    all_results = res.json().get("foods", [])

    # Keep only foods that have at least 4 of the 6 nutrients
    valid_results = []
    for food in all_results:
        nutrients = {n.get("nutrientName"): n.get("value") for n in food.get("foodNutrients", []) if n.get("nutrientName")}
        nutrient_match_count = sum(1 for key in REQUIRED_NUTRIENTS if key in nutrients and nutrients[key] is not None)

        if nutrient_match_count >= 2:
            valid_results.append(food)

    return valid_results

def get_usda_food_nutrition(fdc_id):
    res = requests.get(f"{FOOD_URL}{fdc_id}?api_key={API_KEY}")
    res.raise_for_status()
    food = res.json()

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
