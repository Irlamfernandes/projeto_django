import requests

API_KEY = "6f56ba9c0c8541e4d886842f2bd2b06d"  
BASE_URL = "https://api.themoviedb.org/3"

def buscar_filmes_tmdb(nome_filme: str):
    params = {
        "api_key": API_KEY,
        "query": nome_filme,
        "language": "pt-BR",
        "include_adult": False,
        "page": 1,
    }
    resp = requests.get(f"{BASE_URL}/search/movie", params=params, timeout=10)
    if resp.status_code == 200:
        return resp.json().get("results", [])
    else:
        return {"erro": f"Falha na requisição: {resp.status_code}"}