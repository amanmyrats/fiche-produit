from .models import Annexe5, Project, Lot, Trade

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

def annexe5_renderer(request):
    return {
        'annexe5s': Annexe5.objects.all()
    }