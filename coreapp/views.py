from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .services import TMDbClient, TMDbError, StreamingClient
from .rotas_streaming import STREAMING_LINKS_BY_NAME


class BuscarFilmeView(View):
    def get(self, request):
        query = request.GET.get("filme", "").strip()
        context = {
            "query": query,
            "filmes": [],
            "erro": None
        }

        if query:
            try:
                client = TMDbClient()
                streaming_client = StreamingClient()

                resultados_api = client.buscar_filmes(query)

                resultados_ordenados = sorted(resultados_api, key=lambda f: f.get("popularity", 0), reverse=True)

                filmes_formatados = []
                for filme_api in resultados_ordenados:
                    id_tmdb = filme_api.get("id")

                    servicos = []
                    try:
                        provedores = streaming_client.buscar_filmes_streaming(id_tmdb)
                        for p in provedores:
                            provider_name = p.get("provider_name")
                            link = STREAMING_LINKS_BY_NAME.get(provider_name, "  # ")
                            servicos.append({
                                "nome": provider_name,
                                "logo_url": f"https://image.tmdb.org/t/p/w45{p.get('logo_path')}" if p.get(
                                    "logo_path") else None,
                                "link": link,
                            })
                    except TMDbError:
                        servicos = []

                    filme_formatado = {
                        "id": id_tmdb,
                        "titulo": filme_api.get("title"),
                        "sinopse": filme_api.get("overview"),
                        "poster_url": f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get(
                            "poster_path") else None,
                        "servicos": servicos,
                    }
                    filmes_formatados.append(filme_formatado)

                context["filmes"] = filmes_formatados

            except TMDbError as e:
                context["erro"] = f"Ocorreu um erro ao buscar os filmes: {e}"

        return render(request, "coreapp/resultados.html", context)


class DetalheFilmeView(View):
    def get(self, request, filme_id):
        context = {"filme": None, "erro": None}
        try:
            tmdb_client = TMDbClient()
            streaming_client = StreamingClient()

            filme_api = tmdb_client.get_filme_detalhes(filme_id)

            videos = filme_api.get("videos", {}).get("results", [])
            trailer = next((v for v in videos if v["type"] == "Trailer" and v["site"] == "YouTube"), None)

            try:
                provedores = streaming_client.buscar_filmes_streaming(filme_id)
                servicos = [
                    {
                        "nome": p.get("provider_name"),
                        "logo_url": f"https://image.tmdb.org/t/p/w45{p.get('logo_path')}" if p.get(
                            "logo_path") else None,
                        "link": STREAMING_LINKS_BY_NAME.get(p.get("provider_name"), "  # ")
                    }
                    for p in provedores
                ]
            except TMDbError:
                servicos = []

            filme_formatado = {
                "id": filme_api.get("id"),
                "titulo": filme_api.get("title"),
                "sinopse": filme_api.get("overview"),
                "poster_url": f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get(
                    "poster_path") else None,
                "data_lancamento": filme_api.get("release_date"),
                "avaliacao": filme_api.get("vote_average"),
                "generos": [genero["name"] for genero in filme_api.get("genres", [])],
                "duracao": filme_api.get("runtime"),
                "elenco": [
                    {
                        "nome": pessoa.get("name"),
                        "personagem": pessoa.get("character"),
                        "foto_url": f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get(
                            "profile_path") else None,
                    }
                    for pessoa in filme_api.get("credits", {}).get("cast", [])
                ],
                "trailer_key": trailer["key"] if trailer else None,
                "imagens": {
                    "backdrops": [
                        f"https://image.tmdb.org/t/p/w1280{img['file_path']}"
                        for img in filme_api.get("images", {}).get("backdrops", [])
                    ],
                },
                "avaliacoes": [
                    {
                        "autor": avaliacao.get("author"),
                        "conteudo": avaliacao.get("content"),
                        "nota": avaliacao.get("author_details", {}).get("rating"),
                        "avatar_url": f"https://image.tmdb.org/t/p/w45{avaliacao.get('author_details', {}).get('avatar_path')}" if avaliacao.get(
                            'author_details', {}).get('avatar_path') else None,
                        "url": avaliacao.get("url"),
                        "data_criacao": avaliacao.get("created_at"),
                    }
                    for avaliacao in filme_api.get("reviews", {}).get("results", [])
                ],
                "servicos": servicos,
                "recomendacoes": [
                    {
                        "id": filme.get("id"),
                        "titulo": filme.get("title"),
                        "poster_url": f"https://image.tmdb.org/t/p/w185{filme.get('poster_path')}" if filme.get(
                            "poster_path") else None,
                    }
                    for filme in filme_api.get("recommendations", {}).get("results", [])
                ],
            }
            context["filme"] = filme_formatado

        except TMDbError as e:
            context["erro"] = f"Ocorreu um erro ao buscar os detalhes do filme: {e}"

        return render(request, 'coreapp/detalhe_filme.html', context)


class SobreView(View):
    template_name = 'coreapp/sobre.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class FilmesPopularesView(View):
    template_name = 'coreapp/filmes_populares.html'

    def get(self, request, *args, **kwargs):
        """
        Se a requisição for AJAX, retorna JSON com os próximos filmes.
        Caso contrário, renderiza a página normal com os primeiros filmes.
        """
        page = int(request.GET.get("page", 1))
        client = TMDbClient()
        streaming_client = StreamingClient()

        context = {
            "filmes": [],
            "erro": None,
            "page": page
        }

        try:
            resultados_api = client.filmes_populares(page=page)
            filmes_formatados = []

            for filme_api in resultados_api:
                id_tmdb = filme_api.get("id")
                servicos = []
                try:
                    provedores = streaming_client.buscar_filmes_streaming(id_tmdb)
                    for p in provedores:
                        provider_name = p.get("provider_name")
                        link = STREAMING_LINKS_BY_NAME.get(provider_name, "  # ")
                        servicos.append({
                            "nome": provider_name,
                            "logo_url": f"https://image.tmdb.org/t/p/w45{p.get('logo_path')}" if p.get(
                                "logo_path") else None,
                            "link": link,
                        })
                except TMDbError:
                    servicos = []

                filmes_formatados.append({
                    "id": id_tmdb,
                    "titulo": filme_api.get("title"),
                    "sinopse": filme_api.get("overview"),
                    "poster_url": f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get(
                        "poster_path") else None,
                    "servicos": servicos,
                })

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # Retorna apenas JSON para AJAX
                return JsonResponse({
                    "filmes": filmes_formatados,
                    "page": page,
                    "tem_mais": len(resultados_api) > 0
                })
            else:
                context["filmes"] = filmes_formatados
                return render(request, self.template_name, context)

        except TMDbError as e:
            context["erro"] = f"Ocorreu um erro ao buscar filmes populares: {e}"
            return render(request, self.template_name, context)
