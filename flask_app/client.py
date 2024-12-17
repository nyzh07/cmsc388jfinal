import requests
import math
class Recipe(object):
    def __init__(self, json, detailed=False):
        self.recipe_id = json["id"]
        self.ingredients = [item["original"] for item in json["extendedIngredients"]]
        self.title = json["title"]
        self.readyInMinutes = json["readyInMinutes"]
        self.servings = json["servings"]
        self.image = json["image"]
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

    def search(self, search_string):
        # breakpoint()
        search_url = self.base_url + search_string + f"&titleMatch={search_string}&number=30"
        try:
            resp = self.sess.get(search_url, timeout=10)  # Add a timeout
            resp.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.Timeout:
            print("Request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

        return resp.json()
    
    def get_recipe(self, recipe_id):
        """
        Use to obtain a Recipe object representing the recipe identified by
        the supplied recipe_id
        """
        recipe_url = self.base_id_url + f"{recipe_id}/information?apiKey={self.api_key}"

        resp = self.sess.get(recipe_url)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        try:
            resp = self.sess.get(recipe_url, timeout=10)  # Add a timeout
            resp.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.Timeout:
            print("Request timed out.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

        recipe = Recipe(data)
        return recipe

if __name__ == "__main__":
    import os

    client = RecipeClient(os.environ.get("API_KEY"))
    recipes = client.search("pasta")
    # find = client.get_recipe(716429)


