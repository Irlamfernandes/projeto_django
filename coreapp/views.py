
from django.shortcuts import render
from django.views import View
from .services import TMDbClient, TMDbError

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
                resultados_api = client.buscar_filmes(query)
                
                filmes_formatados = []
                for filme_api in resultados_api:
                    filme_formatado = {
                        'titulo': filme_api.get('title'),
                        'sinopse': filme_api.get('overview'),
                        'poster_url': f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get('poster_path') else None,
                        'servicos': [] 
                    }
                    filmes_formatados.append(filme_formatado)
             
                
                context["filmes"] = filmes_formatados

            except TMDbError as e:
                context["erro"] = f"Ocorreu um erro ao buscar os filmes: {e}"

        return render(request, "resultados.html", context) # 