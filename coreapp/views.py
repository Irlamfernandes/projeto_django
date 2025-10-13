
from django.shortcuts import render
from django.views import View
from .services import TMDbClient, TMDbError, StreamingClient

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
                        servicos = [
                            {
                                "nome": p.get("provider_name"),
                                "logo_url": f"https://image.tmdb.org/t/p/w45{p.get('logo_path')}" if p.get("logo_path") else None
                            }
                            for p in provedores
                        ]
                    except TMDbError:
                        servicos = []

                    filme_formatado = {
                        "titulo": filme_api.get("title"),
                        "sinopse": filme_api.get("overview"),
                        "poster_url": f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get("poster_path") else None,
                        "servicos": servicos,
                    }
                    filmes_formatados.append(filme_formatado)
                
                context["filmes"] = filmes_formatados

            except TMDbError as e:
                context["erro"] = f"Ocorreu um erro ao buscar os filmes: {e}"

        return render(request, "coreapp/resultados.html", context) # 
    
class SobreView(View):
    template_name = 'coreapp/sobre.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)