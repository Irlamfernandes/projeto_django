from django.http import HttpResponse

def ola (request):
    return HttpResponse("Olá, Tudo Bem?")