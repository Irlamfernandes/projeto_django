import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


class TMDbError(Exception):
    pass


class TMDbClient:
    def __init__(self, api_key=API_KEY, base_url=BASE_URL, language="pt-BR"):
        self.api_key = api_key
        self.base_url = base_url
        self.language = language
        self.session = requests.Session()

    def buscar_filmes(self, nome_filme: str, page: int = 1):
        params = {
            "api_key": self.api_key,
            "query": nome_filme,
            "language": self.language,
            "include_adult": False,
            "page": page,
        }
        try:
            resp = self.session.get(f"{self.base_url}/search/movie", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro na requisição: {e}")

    def get_filme_detalhes(self, filme_id: int):
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "append_to_response": "credits,videos,images,reviews,recommendations",
        }
        try:
            resp = self.session.get(f"{self.base_url}/movie/{filme_id}", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro na requisição: {e}")

    def filmes_populares(self, page: int = 1):
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "page": page,
        }
        try:
            resp = self.session.get(f"{self.base_url}/movie/popular", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar filmes populares: {e}")


class StreamingClient:
    def __init__(self, api_key=API_KEY, base_url=BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

    def buscar_filmes_streaming(self, id_tmdb: int, country: str = "BR"):
        url = f"{self.base_url}/movie/{id_tmdb}/watch/providers"
        params = {"api_key": self.api_key}
        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            country_data = data.get("results", {}).get(country, {})
            return country_data.get("flatrate", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar provedores: {e}")
