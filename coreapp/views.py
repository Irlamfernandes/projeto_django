from django.shortcuts import render
from django.views import View

class BuscarFilmeView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        resultados = []
        context = {
            "query": query,
            "resultados": resultados
        }
        return render(request, "buscar.html", context)
