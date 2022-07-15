from django.shortcuts import render


def chantier_home(request):
    return render(request, 'site/site.html', {})
