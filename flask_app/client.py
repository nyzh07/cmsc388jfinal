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
        self.base_url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query="
        self.base_id_url = f"https://api.spoonacular.com/recipes/"

    def search(self, search_string):
        # breakpoint()
        cached_search = read_search_cache(search_string)
        if cached_search:
            return cached_search.response
        
        search_url = self.base_url + search_string + f"&number=10"
        try:
            resp = self.sess.get(search_url, timeout=10)  # Add a timeout
            resp.raise_for_status()  # Raise an exception for HTTP errors
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
        write_search_cache(search_string, resp.json())
        return resp.json()
    
    def get_recipe(self, recipe_id):
        """
        Use to obtain a Recipe object representing the recipe identified by
        the supplied recipe_id
        """
        recipe_url = self.base_id_url + f"{recipe_id}/information?apiKey={self.api_key}"

        cached_recipe = read_recipe_cache(int(recipe_id))
        if cached_recipe:
            return Recipe(cached_recipe.response)

        try:
            resp = self.sess.get(recipe_url, timeout=10)  # Add a timeout
            resp.raise_for_status()  # Raise an exception for HTTP errors
            data = resp.json()
            write_recipe_cache(int(recipe_id), resp.json())
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

if __name__ == "__main__":
    import os

    client = RecipeClient(os.environ.get("API_KEY"))
    recipes = client.search("pasta")
    find = client.get_recipe(716429)


