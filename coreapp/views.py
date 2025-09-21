from django.shortcuts import render
from django.views import View
from .services import TMDbClient, TMDbError

class BuscarFilmeView(View):
    def get(self, request):
        """
        Esta view captura o nome de um filme enviado por um formulário GET,
        utiliza o TMDbClient para buscar os resultados e os envia para o template.
        """
        # Linha que captura o nome do filme do formulário (que usa name="filme")
        query = request.GET.get("filme", "").strip()
        
        # Dicionário de contexto que será enviado para o template
        context = {
            "query": query,
            "resultados": [],
            "erro": None
        }

        # Executa a busca apenas se um termo foi digitado
        if query:
            try:
                # Instancia e utiliza o cliente da API que você criou
                client = TMDbClient()
                resultados_api = client.buscar_filmes(query)
                context["resultados"] = resultados_api

            except TMDbError as e:
                # Em caso de erro, preenche a mensagem para ser exibida no template
                context["erro"] = f"Ocorreu um erro ao buscar os filmes: {e}"

        # Renderiza a resposta. O nome 'buscar.html' foi mantido do seu código original.
        # A URL 'resultados' deve estar configurada para apontar para esta view.
        return render(request, "buscar.html", context)