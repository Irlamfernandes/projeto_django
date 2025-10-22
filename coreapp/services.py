import os
from dotenv import load_dotenv
import requests
from datetime import date

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
        """ Retorna filmes populares. """
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

    def top_rated_filmes(self, page: int = 1):
        """ Retorna filmes com melhor avaliação (Top Rated). """
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "page": page,
        }
        try:
            resp = self.session.get(f"{self.base_url}/movie/top_rated", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar filmes Top Rated: {e}")

    def filmes_lancamentos(self, page: int = 1):
        """ Retorna filmes que estão 'Próximos' de serem lançados (Upcoming). """
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "page": page,
        }
        try:
            resp = self.session.get(f"{self.base_url}/movie/upcoming", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar filmes de Lançamentos (Upcoming): {e}")

    def filmes_now_playing(self, page: int = 1):
        """ Retorna filmes que estão 'Nos Cinemas' (Now Playing). """
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "page": page,
            "region": "BR",
        }
        try:
            resp = self.session.get(f"{self.base_url}/movie/now_playing", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar filmes Nos Cinemas: {e}")

    def filmes_trending_week(self, page: int = 1):
        """ Retorna filmes em alta na semana (Mais Vistos). """
        params = {
            "api_key": self.api_key,
            "language": self.language,
            "page": page,
        }
        try:
            resp = self.session.get(f"{self.base_url}/trending/movie/week", params=params, timeout=10)
            resp.raise_for_status()
            return resp.json().get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar filmes em Alta (Semana): {e}")


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