from mongoengine import Document, StringField, DictField, IntField, QuerySet


class CachedSearch(Document):
    query = StringField(unique=True, required=True)
    response = DictField(required=True)


class CachedRecipe(Document):
    recipe_id = IntField(unique=True, required=True)
    response = DictField(required=True)


def memoize(func):
    """
    The database is used to cache search results and recipes to reduce the
    number of API calls. Every time a cached object is accessed in the
    database, it is also stored in a local cache to reduce the number
    of reads to the database.
    """
    local_cache = {}

    def wrapper(*args):
        if args in local_cache:
            print("Accessed Local Cache")
            return local_cache[args]
        result = func(*args)
        if result:
            local_cache[args] = result
        return result

    return wrapper


@memoize
def read_search_cache(query: str = "") -> CachedSearch:
    qs: QuerySet = CachedSearch.objects(query=query)
    return qs.first()


@memoize
def read_recipe_cache(recipe_id: int) -> CachedRecipe:
    qs: QuerySet = CachedRecipe.objects(recipe_id=recipe_id)
    return qs.first()


def write_search_cache(query: str, response: dict):
    cs = CachedSearch(query=query, response=response)
    cs.save()


def write_recipe_cache(recipe_id: str, response: dict):
    cs = CachedRecipe(recipe_id=recipe_id, response=response)
    cs.save()
