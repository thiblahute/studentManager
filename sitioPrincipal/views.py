from django.http import HttpResponse

# Create your views here.
def HolaMundo (request):
    html = "<html><body>Hola Mundo</body></html>"
    return HttpResponse(html)
