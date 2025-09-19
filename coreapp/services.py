import requests

API_KEY = "6f56ba9c0c8541e4d886842f2bd2b06d"
BASE_URL = "https://api.themoviedb.org/3"


class TMDbError(Exception):
    """Exceção personalizada para erros relacionados à API do TMDb."""
    pass


class TMDbClient:
    """
    Cliente para interagir com a API do TMDb.

    Parâmetros:
        api_key (str): Chave da API do TMDb.
        base_url (str): URL base da API.
        language (str): Idioma das respostas (ex: 'pt-BR').
    """

    def __init__(self, api_key=API_KEY, base_url=BASE_URL, language="pt-BR"):
        self.api_key = api_key
        self.base_url = base_url
        self.language = language
        self.session = requests.Session()  # Mantém conexões para múltiplas requisições

    def buscar_filmes(self, nome_filme: str, page: int = 1):
        """
        Busca filmes pelo nome usando a API do TMDb.

        Parâmetros:
            nome_filme (str): Nome do filme a buscar.
            page (int): Página de resultados (default: 1).

        Retorna:
            list: Lista de filmes encontrados (cada filme é um dicionário).

        Levanta:
            TMDbError: Se ocorrer algum problema de rede ou se a API retornar erro.
        """
        params = {
            "api_key": self.api_key,
            "query": nome_filme,
            "language": self.language,
            "include_adult": False,
            "page": page,
        }

        try:
            resp = self.session.get(f"{self.base_url}/search/movie", params=params, timeout=10)
            resp.raise_for_status()  # Lança HTTPError se status != 200
            data = resp.json()
            return data.get("results", [])
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro na requisição: {e}")
        except ValueError:
            raise TMDbError("Resposta inválida da API do TMDb.")


class StreamingClient:
    """
    Cliente para buscar provedores de streaming para filmes do TMDb.

    Parâmetros:
        api_key (str): Chave da API do TMDb.
        base_url (str): URL base da API.
    """

    def __init__(self, api_key=API_KEY, base_url=BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()  # Mantém conexões para múltiplas requisições

    def buscar_filmes_streaming(self, id_tmdb: int, country: str = "BR"):
        """
        Busca provedores de streaming para um filme específico.

        Parâmetros:
            id_tmdb (int): ID do filme no TMDb.
            country (str): Código do país (default: 'BR').

        Retorna:
            list: Lista de provedores de streaming disponíveis no país informado.
                Cada item é um dicionário com pelo menos as chaves:
                - 'provider_name': str, nome do serviço de streaming
                - 'logo_path': str, caminho do logo do serviço
                - 'provider_id': int, ID do serviço
                - outros campos podem estar presentes conforme a API do TMDb

        Levanta:
            TMDbError: Se ocorrer algum problema de rede ou se a API retornar erro.
        """
        url = f"{self.base_url}/movie/{id_tmdb}/watch/providers"
        params = {"api_key": self.api_key}

        try:
            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            country_data = data.get("results", {}).get(country, {})
            providers = country_data.get("flatrate", [])

            return providers
        except requests.exceptions.RequestException as e:
            raise TMDbError(f"Erro ao buscar provedores: {e}")
        except ValueError:
            raise TMDbError("Resposta inválida da API do TMDb.")
