from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from connexionOdoo.forms import odooForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import xmlrpc.client



def index(request):
  form = odooForm()  # ajout d’un nouveau formulaire ici
  return render(request,
          'connexionOdoo/index.html',
          {'form': form})  # passe ce formulaire au gabarit




def verif(request):
    form = odooForm(request.POST) 
    username =''
    password =''
    if form.is_valid():
        username = form.cleaned_data['username']
        print(username)
        password = form.cleaned_data['password']        
        print(password)
    # Paramètres de connexion
    url = "http://localhost:8069"
    db = "apa12"

    # Récupération de la version d’ODOO installée
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    # Connexion de l’utilisateur
    uid = common.authenticate(db, username, password, {})

        # Référence à model.Models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    try:
        if models.execute_kw(db, uid, password, models, 'check_access_rights', ['read'], {'raise_exception': False}):
            
            print('ddddddddddddddddddddddddddd')
    except:
        print("Vous n'avez pas accès au modèle ", models)

    return render(request,'connexionOdoo/verif.html')





    # if request.method == 'POST':
    #     form = odooForm(request.POST)
    #     if form.is_valid():
    #             return HttpResponseRedirect('/thanks/')




    # form = odooForm(request.POST)
    # if form.is_valid(): 
    #         odooForm.objects.create( 
    #         first_name=form.cleaned_data['username'],
    #         last_name=form.cleaned_data['password'] 
    #         ) 

# last_name=form.cleaned_data['password'] 
