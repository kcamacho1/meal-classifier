import requests

API_KEY = "MbvZGPVrj9P3eECrXnVpicA2xfS9Ky0LwaWrUjBR"
SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
FOOD_URL = "https://api.nal.usda.gov/fdc/v1/food/"

# ✅ Required nutrients we care about
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

    # 🔍 Filter to only those with all required nutrients
    valid_results = []
    for food in all_results:
        nutrients = {n.get("nutrientName"): n.get("value") for n in food.get("foodNutrients", []) if n.get("nutrientName")}

        if all(k in nutrients and nutrients[k] is not None for k in REQUIRED_NUTRIENTS):
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

    # ✅ Fail early if required nutrients are missing
    if not all(k in nutrients for k in REQUIRED_NUTRIENTS):
        raise ValueError("This USDA food entry lacks complete nutritional information.")

    return {
        "Calories": nutrients["Energy"],
        "Protein (g)": nutrients["Protein"],
        "Fat (g)": nutrients["Total lipid (fat)"],
        "Carbs (g)": nutrients["Carbohydrate, by difference"],
        "Sugar (g)": nutrients["Sugars, total including NLEA"],
        "Fiber (g)": nutrients["Fiber, total dietary"]
    }
