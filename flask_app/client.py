import requests
import math

from flask_app.cache import read_recipe_cache, read_search_cache, write_recipe_cache, write_search_cache
class Recipe(object):
    def __init__(self, json, detailed=False):
        self.recipe_id = json["id"]
        self.ingredients = [item["original"] for item in json["extendedIngredients"]]
        self.title = json["title"]
        self.readyInMinutes = json["readyInMinutes"]
        self.servings = json["servings"]
        self.image = json["image"] if "image" in json else None
        self.summary = json["summary"]
        self.instructions = {}
        instructions = json["analyzedInstructions"]
        if instructions:
            steps = instructions[0]["steps"]
            for dict in steps:
                number = dict["number"]
                step = dict["step"]
                self.instructions[number] = step
        self.score = math.floor(json["spoonacularScore"])
 
    def __repr__(self):
        return self.ingredients

class RecipeClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.api_key = api_key
        self.base_url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&addRecipeInstructions=True&query="
        self.base_id_url = f"https://api.spoonacular.com/recipes/"

    def search(self, search_string, page=1):
        offset = (page - 1) * 30
        search_url = self.base_url + search_string + f"&titleMatch={search_string}&number=30&offset={offset}"
        try:
            resp = self.sess.get(search_url, timeout=10)
            resp.raise_for_status()
        except requests.HTTPError:
            if resp.status_code == 404:
                print(f"API Request: HTTP {resp.status_code} - Not Found")
                return None
            if resp.status_code == 402:
                print(f"API Request: HTTP {resp.status_code} - Limit Reached")
                raise Exception("Recipe Request Failed")
            print(f"API Request: HTTP {resp.status_code} - Check API Key")
            raise Exception("Recipe Request Failed")
        except requests.exceptions.Timeout:
            print(f"API Request: HTTP {resp.status_code} - Timed Out")
            raise
        except requests.exceptions.RequestException as e:
            print(f"API Request: HTTP {resp.status_code} - See Below")
            print(e)
            raise
        return resp.json()
    
    def get_recipe(self, recipe_id):
        recipe_url = self.base_id_url + f"{recipe_id}/information?apiKey={self.api_key}"
        try:
            resp = self.sess.get(recipe_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.HTTPError:
            if resp.status_code == 404:
                print(f"API Request: HTTP {resp.status_code} - Not Found")
                return None
            if resp.status_code == 402:
                print(f"API Request: HTTP {resp.status_code} - Limit Reached")
                raise Exception("Recipe Request Failed")
            print(f"API Request: HTTP {resp.status_code} - Check API Key")
            raise Exception("Recipe Request Failed")
        except requests.exceptions.Timeout:
            print(f"API Request: HTTP {resp.status_code} - Timed Out")
            print(f"Timed Out")
            raise Exception("Recipe Retrieval Failed")
        except requests.exceptions.RequestException as e:
            print(f"API Request: HTTP {resp.status_code} - See Below")
            print(e)
            raise Exception("Recipe Retrieval Failed")

        recipe = Recipe(data)
        return recipe
    
    def get_random_recipes(self):
        recipe_url = self.base_id_url + f"random?number=12&apiKey={self.api_key}"

        try:
            resp = self.sess.get(recipe_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.HTTPError:
            if resp.status_code == 404:
                print(f"API Request: HTTP {resp.status_code} - Not Found")
                return None
            if resp.status_code == 402:
                print(f"API Request: HTTP {resp.status_code} - Limit Reached")
                raise Exception("Recipe Request Failed")
            print(f"API Request: HTTP {resp.status_code} - Check API Key")
            raise Exception("Recipe Request Failed")
        except requests.exceptions.Timeout:
            print("API Request Timed Out")
            raise Exception("Random Recipe Retrieval Failed")
        except requests.exceptions.RequestException as e:
            print("API Request Error:", e)
            raise Exception("Random Recipe Retrieval Failed")
        
        recipes = [Recipe(recipe) for recipe in data["recipes"]]
        return recipes

if __name__ == "__main__":
    import os

    client = RecipeClient(os.environ.get("API_KEY"))
    recipes = client.search("pasta")
    find = client.get_recipe(716429)


