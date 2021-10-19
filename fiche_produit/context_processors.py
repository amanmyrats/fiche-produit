from .models import Project, Lot, Trade

def project_renderer(request):
    return {
        'projects': Project.objects.all()
    }

def lot_renderer(request):
    return {
        'lots': Lot.objects.all()
    }

def trade_renderer(request):
    return {
        'trades': Trade.objects.all()
    }