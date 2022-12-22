from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from connexionOdoo.forms import odooForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import xmlrpc.client
from .models import connexionInformation



def index(request):
  print(request)

  form = odooForm()  # ajout d’un nouveau formulaire ici
  return render(request,
          'connexionOdoo/index.html',
          {'form': form})  # passe ce formulaire au gabarit




def verif(request):
    form = odooForm(request.POST) 
    username =""
    password =""
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']        
    # Paramètres de connexion
    url = "http://localhost:8069"
    db = "apa12"

    # Récupération de la version d’ODOO installée
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    # Connexion de l’utilisateur
    uid = common.authenticate(db, username, password, {})
    print(uid)
        # Référence à model.Models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    hasRight = False
    try:
        
        # print(username)
        # print(password)
        # print(url)
        # print(db)
        print('exec_kw')  
        print(hasRight)  
        hasRight = models.execute_kw(db, uid, password, 'realtor.apartment', 'check_access_rights', ['read'], {'raise_exception': False})
        print(hasRight)
            
    except:
        hasRight = False
        print("Vous n'avez pas accès au modèle ", models)
        
    print(hasRight)

    if(hasRight):
        # connexionInformation.objects.create( 
        #     username=form.cleaned_data['username'],
        #     password=form.cleaned_data['password'] 
        #     ) 
        print('verif')
        request.session['username'] = username
        request.session['password'] = password
        request.session['db'] = db
        request.session['uid'] = uid

        return redirect('/apartmentPurchase/')
    else:
        print('refresh')
        return redirect('/connexionOdoo/')
        #return index(request)


