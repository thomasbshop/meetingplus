import json
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context, loader
from django.views.decorators.cache import cache_page
from django.conf import settings
from .models import Agenda

@login_required(login_url="accounts/login/")
def dashboard(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

# @login_required()
# def agenda(request):
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#         new_item = request.POST['item']
#         item = Agenda(item = new_item)
#         item.save()
#         return HttpResponseRedirect(request.path_info)
#     items = Agenda.objects.all()
#     context = {'agenda': items}
#     return render(request, 'meeting/agenda.html', context)
    
# @login_required()
# def minutes(request):
#     meeting_id = 1
#     context = {'minutes': 'minutes page.'}
#     return render(request, 'meeting/minutes.html', context)

JS_SETTINGS_TEMPLATE = """
    window.settings = JSON.parse('{{ json_data|escapejs }}');
"""
@cache_page(60 * 15)
def js_settings(request):
    data = {
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        "DEBUG": settings.DEBUG,
        "LANGUAGES": settings.LANGUAGES,
        "DEFAULT_LANGUAGE_CODE": settings.LANGUAGE_CODE,
        "CURRENT_LANGUAGE_CODE": request.LANGUAGE_CODE,
        }
    json_data = json.dumps(data)
    template = Template(JS_SETTINGS_TEMPLATE)
    context = Context({"json_data": json_data})
    response = HttpResponse(
        content=template.render(context), 
        content_type="application/javascript; charset=UTF-8",
    )
    return response