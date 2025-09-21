
from django.shortcuts import render
from django.views import View
from .services import TMDbClient, TMDbError # Corrigido para .services

class BuscarFilmeView(View):
    def get(self, request):
        query = request.GET.get("filme", "").strip()
        context = {
            "query": query,
            "filmes": [], # MUDANÇA 1: Nome da variável agora é "filmes"
            "erro": None
        }

        if query:
            try:
                client = TMDbClient()
                resultados_api = client.buscar_filmes(query)
                
                # --- INÍCIO DA LÓGICA DE FORMATAÇÃO ---
                filmes_formatados = []
                for filme_api in resultados_api:
                    # MUDANÇA 2: Cria um dicionário com os nomes que o template espera
                    filme_formatado = {
                        'titulo': filme_api.get('title'),
                        'sinopse': filme_api.get('overview'),
                        # MUDANÇA 3: Monta a URL completa do pôster
                        'poster_url': f"https://image.tmdb.org/t/p/w500{filme_api.get('poster_path')}" if filme_api.get('poster_path') else None,
                        # MUDANÇA 4: Adiciona uma lista vazia para não quebrar o template
                        'servicos': [] 
                    }
                    filmes_formatados.append(filme_formatado)
                # --- FIM DA LÓGICA DE FORMATAÇÃO ---
                
                context["filmes"] = filmes_formatados

            except TMDbError as e:
                context["erro"] = f"Ocorreu um erro ao buscar os filmes: {e}"

        return render(request, "resultados.html", context) # 