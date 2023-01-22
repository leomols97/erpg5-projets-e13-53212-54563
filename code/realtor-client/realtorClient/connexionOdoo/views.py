from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from connexionOdoo.forms import odooForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import xmlrpc.client
from .models import connexionInformation



def index(request):
  """
ajout d'un formulaire et passage de celuici au gabarit

:param request;
"""  
  form = odooForm() 
  return render(request,
          'connexionOdoo/index.html',
          {'form': form}) 




def verif(request):
    """
vérifie les accès de l'utilisateur,
s'il existe on redirige vers l'url des appartements,
sinon vers celui de la connexion

:param request
"""
    form = odooForm(request.POST) 
    
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']        
    # Paramètres de connexion
    url = "http://localhost:8069"
    db = "dbProject"

    # Récupération de la version d’ODOO installée
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    # Connexion de l’utilisateur
    uid = common.authenticate(db, username, password, {})
    print(uid)
        # Référence à model.Models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    hasRight = False
    try:
        hasRight = models.execute_kw(db, uid, password, 'realtor.apartment', 'check_access_rights', ['read'], {'raise_exception': False})            
    except:
        hasRight = False
    if(hasRight):
        # Création d'une session et tout ce qui va être modifié existera durant la session
        # Session est un objet qui contient de la variable request
        # Niveau sécurité, ce n'est pas bon car 'session' a un lien avec les cookies. On ne s'en occupe simplement pas ici.
        request.session['username'] = username
        request.session['password'] = password
        request.session['uid'] = uid

        return redirect('/apartmentPurchase/')
    else:
        print('refresh') # Print dans la console
        return redirect('/connexionOdoo/')


