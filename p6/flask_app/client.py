import requests


class Recipe:
    def __init__(self, recipe_json, detailed=False):
        if detailed:
            self.ingredients = [ingredient["name"] for ingredient in recipe_json.get("extendedIngredients", [])]
            self.instructions = recipe_json.get("instructions", "No instructions provided")
            self.ready_in_minutes = recipe_json.get("readyInMinutes", "Unknown")
            self.servings = recipe_json.get("servings", "Unknown")

        self.title = recipe_json["title"]
        self.recipe_id = recipe_json["id"]
        self.image_url = recipe_json.get("image", "")

    def __repr__(self):
        return self.title


class RecipeClient:
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.base_url = "https://api.spoonacular.com/recipes"
        self.api_key = api_key

    def search(self, search_string, number=10):
        """
        Searches Spoonacular's API for the supplied search_string and returns
        a list of Recipe objects.
        """
        search_url = f"{self.base_url}/complexSearch"
        params = {
            "query": search_string,
            "number": number,
            "apiKey": self.api_key
        }

        resp = self.sess.get(search_url, params=params)

        if resp.status_code != 200:
            raise ValueError("Search request failed; check your API key and permissions")

        data = resp.json()

        if not data.get("results"):
            raise ValueError(f"No results found for '{search_string}'")

        return [Recipe(item) for item in data["results"]]

    def retrieve_recipe_by_id(self, recipe_id):
        """
        Retrieves detailed information about a recipe by its ID.
        """
        recipe_url = f"{self.base_url}/{recipe_id}/information"
        params = {
            "apiKey": self.api_key
        }

        resp = self.sess.get(recipe_url, params=params)

        if resp.status_code != 200:
            raise ValueError("Request failed; check your API key and permissions")

        data = resp.json()

        if not data:
            raise ValueError(f"No recipe found for ID '{recipe_id}'")

        return Recipe(data, detailed=True)


## -- Example usage -- ##
if __name__ == "__main__":
    import os

    # Replace with your actual API key
    RECIPE_API_KEY = os.environ.get("RECIPE_API_KEY")
    client = RecipeClient(RECIPE_API_KEY)

    # Search for recipes
    search_results = client.search("pasta", number=5)
    for recipe in search_results:
        print(recipe)

    # Retrieve detailed information about the first recipe
    if search_results:
        detailed_recipe = client.retrieve_recipe_by_id(search_results[0].recipe_id)
        print(f"\nDetailed Recipe: {detailed_recipe.title}")
        print(f"Ingredients: {detailed_recipe.ingredients}")
        print(f"Instructions: {detailed_recipe.instructions}")