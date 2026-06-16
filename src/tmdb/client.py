import requests
from django.conf import settings

# Movie Discovery Resource

def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_API_KEY}",
    }


def search_movie(query:str, page:int=1, raw=False):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query":query,
        "language": "zh-CN",
        "include_adult":False,
        "page": page,
    }
    headers = get_headers()

    response = requests.get(url,headers=headers ,params=params)
    if raw:
        return response
    return response.json()


def movie_detail(movie_id: int, raw=False):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "language": "zh-CN",
        "include_adult": False,
    }
    headers = get_headers()

    response = requests.get(url, headers=headers, params=params)
    if raw:
        return response
    return response.json()