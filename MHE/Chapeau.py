# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:18:49 2021

@author: bourgeoisc, neverren

A lancer à partir de "D:\Documents\bourgeoisc\BRGM\REN_INTERREG_W4T - General\03 - Réalisation SMA\MHE"

But de ce script: 
1. Créer une version python scénarisable
2. On peut facilement lancer une boucle sur les scénarios 
"""

# Import modules
import pyomo
from pyomo.environ import *
from pyomo.opt import SolverFactory

""" Vérif solveurs dispos :
pyomo_solvers_list = SolverFactory.__dict__['_cls'].keys()
SolverFactory('ipopt').available() == True
"""

import pandas as pd
import numpy as np
import csv
import os


####### Définitions des répertoires 
Donnees="./Input"
Dossiers_sorties="./Sorties"
####### Défintions des mois
Months=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
#Months=["January","February","March","April","May","June","July","August","September","October","November","December"]
####### Défintion des pas de temps
time=range(1,13,1)

####### Scénario ## 

## Choix scénarios :

## 1. Le climat
Scenario_hydro = "Sec"  # Choix: Ref,DOE,Sec,SecEtendue
print("Scenario hydro :" , Scenario_hydro) 

## 2. Les métabolites
Scenario_Metabolite = "Ref"  # Choix: Ref,Abandon,AbandonMax,AbandonMaxK
print("Scenario_Metabolite :" , Scenario_Metabolite) 

## 3. La demande
### Pour rappel :
    #Référence= Etalement saisonnier
    #Domestique+: Ref + hausse population 10% sur comnmunes littoral
    #Toursitique: Ref+Augmentation Toruisme estival Crozon
    #Capsizun+: Ref+ CapSiZun +Goyen!!!
    
Activation_Etalement_Saisonnier= "Oui"  # Choix Oui/Non #par défault oui
print("Activation_Etalement_Saisonnier :" , Activation_Etalement_Saisonnier) 

Activation_Hausse_Population= "Oui"  # Choix Oui/Non # PAr défault non
print("Activation_Hausse_Population :" , Activation_Hausse_Population) 

Activation_Hausse_tourisme= "Oui"  # Choix Oui/Non # PAr défault non
print("Activation_Hausse_tourisme :" , Activation_Hausse_tourisme) 

Activation_CapSizun= "Oui"  # Choix Oui/Non # PAr défault non
Activation_Goyen= "Oui"  # Choix Oui/Non # PAr défault non
print("Activation_CapSizun_Goyen :" , Activation_CapSizun +'_'+ Activation_Goyen) 

## 4. La crise
Activation_Crise= "Oui"  # Choix Oui/Non # Par ddfault non
if Activation_Crise=="Oui":
    Mois_crise="Janvier" # Choix = Août, Septembre, Janvier
print("Activation_Crise :" , Activation_Crise) 


### Option: Activation lien LeJuch-Kernevez (par default non)
scenario_Juch_Kernevez="Non"
print("scenario_Juch_Kernevez :" , scenario_Juch_Kernevez) 


## 5. Mesure de Gestion
#Mesure_gestion= "Non" # Choix Oui/Non
#if Mesure_gestion=="Oui"
# Rendement
Scenario_Rendement="Non" # Choix Oui, Non
print("Scenario_Rendement :" , Scenario_Rendement) 
if Scenario_Rendement=="Non":
    mesure1="0"
else:
    mesure1="1"
# Economie d'eau
Scenario_baisse_demande="Non" # Choix Max, Medium, Non
print("Scenario_baisse_demande :" , Scenario_baisse_demande) 
if Scenario_baisse_demande=="Non":
    mesure2="0"
elif Scenario_baisse_demande=="Medium":
    mesure2="1"
elif Scenario_baisse_demande=="Max":
    mesure2="2"
    
#Brennilis
scenario_brennilis="Non" # Choix Max, Medium, Non
print("scenario_brennilis :" , scenario_brennilis) 
if scenario_brennilis=="Non":
    mesure3="0"
elif scenario_brennilis=="Medium":
    mesure3="1"
elif scenario_brennilis=="Max":
    mesure3="2"
# Interco globale
scenario_interco_globale="Non"   #Choix Oui/Non # Par ddfault non
if scenario_interco_globale=="Oui":
    activation_Douarnenez_Lejuch=1
    activation_Cuzon=1
    mesure4="DLJ"+str(activation_Douarnenez_Lejuch)+"RC"+str(activation_Cuzon)
else:
    mesure4="DLJ0RC0"
print("scenario_interco_globale :" ,  mesure4) 
# Kerstrat

scenario_Kerstrat="Non"  # Choix Oui/Non
if scenario_Kerstrat=="Non":
    mesure4b="0"
else:
    mesure4b="1"
# Interco locale
scenario_interco_locale="Non"   #Choix Oui/Non # Par ddfault non
print("scenario_interco_locale :" , scenario_interco_globale+scenario_interco_locale) 
if scenario_interco_locale=="Non":
    mesure5="0"
else:
    mesure5="1"
# Nouvelle carrière 

scenario_nouvelles_carriere="Non"  #Choix Oui/Non # Par ddfault non
if scenario_nouvelles_carriere=="Oui":
    Carriere_plessis=0 #Choix0/1
    Carriere_loquefret=0 #Choix0/1
    Carriere_MenezMolve=0 #Choix0/1
    Carriere_SaintEvarzec=1  # Choix 0/1. fonctionne différement. Concerne PenALen et n'est pas modélisé explicitement
    mesure6="p"+str(Carriere_plessis)+"l"+str(Carriere_loquefret)+"m"+ str(Carriere_MenezMolve)+"E"+str(Carriere_SaintEvarzec)
if scenario_nouvelles_carriere=="Non":
    mesure6="p0l0m0"
  
print("scenario_nouvelles_carriere :" , scenario_nouvelles_carriere+mesure6) 

# Nouvelle Ressource *CCPF
scenario_nouvelles_Ressources="Non" 
if scenario_nouvelles_Ressources=="Oui":
    Secteur_Benodet=1 #Choix0/1
    Secteur_RoudGwen=1 #Choix0/1
    Secteur_Lanveron=1 #Choix0/1
    Secteur_PenALen=1 #Choix0/1
    Secteur_Brehoulou=1 #Choix0/1
    mesure7="NR"+str(Secteur_Benodet)+str(Secteur_RoudGwen)+str(Secteur_Lanveron)+str(Secteur_PenALen)+str(Secteur_Brehoulou)
if scenario_nouvelles_Ressources=="Non":
    mesure7="NR00000"
# Securisation Reservoir
scenario_Resilience_Stockage="Non" #Choix Oui/Non # Par ddfault non
if scenario_Resilience_Stockage=="Oui":
    Activation_Poraon=1  #Choix 0/1
    Activation_Keryannes= 1  # Choix 0/1
    mesure8="P"+str(Activation_Poraon)+"K"+str(Activation_Keryannes)
else:
    mesure8="P0K0"
print("scenario_Resilience_Stockage :" , scenario_Resilience_Stockage) 

# Secursiation Forage
scenario_Resilience_forage='Non' #Choix Oui/Non # Par ddfault non
print("scenario_Resilience_forage :" , scenario_Resilience_forage) 
if scenario_Resilience_forage=="Non":
    mesure9="0"
else:
    mesure9="1"
#print(Scenario_autres)
## Choix de la fonction de défaillance (#Utiliser CoutLinéaire pour les tests, CoutQuadratique sinon)
#Scenario_cout_def="CoutLineaire"

####### Définitions du scnéario
if Activation_Crise== "Non" :
    name_simulation='H'+Scenario_hydro+'-M'+Scenario_Metabolite +'-ES_'+Activation_Etalement_Saisonnier +'-HP_'+Activation_Hausse_Population +'-HT_'+ Activation_Hausse_tourisme + 'CS-Go_'+  Activation_CapSizun +'_'+ Activation_Goyen+'-Crise_'+Activation_Crise+ '-LJK'+scenario_Juch_Kernevez+ '-Gestion'+mesure1+mesure2+mesure3+mesure4+mesure4b+mesure5+mesure6+mesure7+mesure8+mesure9
else :
     name_simulation='H'+Scenario_hydro+'-M'+Scenario_Metabolite +'-ES_'+Activation_Etalement_Saisonnier +'-HP_'+Activation_Hausse_Population +'-HT_'+ Activation_Hausse_tourisme + 'CS-Go_'+  Activation_CapSizun +'_'+ Activation_Goyen+'-Crise_'+Activation_Crise+Mois_crise+ '-LJK'+scenario_Juch_Kernevez+'-Gestion'+mesure1+mesure2+mesure3+mesure4+mesure4b+mesure5+mesure6+mesure7+mesure8+mesure9

#name_simulation="AtelierNew"+'_'+name_simulation
name_simulation="test_kerrous"+'_'+name_simulation




print(name_simulation)
Sorties=Dossiers_sorties+'/'+name_simulation
os.makedirs(Sorties, exist_ok=True)
name_Sorties=Sorties+'/results_'


#### Eplacement des fichiers hyfro
dossier_Hydro='./../HYDROLOGIE/A - DEBITS PRELEVABLES AULNE ET ST MICHEL - Modif 28_04_22/'
dossier_Hydro_kerrous='./../HYDROLOGIE/A - Steir Guengat_V2/'
###### Appels des sous parties
### Partie 1 Def param et senario
print(" Partie 1 :Definition paramétres et Scénarios")
###1.1 Lecture des Scénarios
print("Lecture paramétre Scénarios")
exec(open("param_scenario.py").read())
###1.2 Lecture des Paramtres des fonctions de couts
print("Lecture paramétre Couts")
exec(open("param_cout.py").read())

###1.3 Lecture des Fonctions  de couts
print("Lecture Fonctions Couts")
exec(open("fonctions.py").read())

print("Partie 1 Ok")

### PArtie 2  Data
print(" Partie 2 : Lecture des Datas")
#2.1 lectures des csv d'entrés 
exec(open("lecture_data.py").read())

print("Data OK")

### PArtie 3  Scénario
#3.1 Scénrio 2050
print(" PArtie 3 : Application Scenarios 2050")
exec(open("Scenario.py").read())
#3.2 Scénario de gestion
print(" PArtie 3 : Application Mesure Gestion")
exec(open("Mesure_gestion.py").read())
### PArtie 4 Probleme
print(" PArtie 4 : Defintion Objective et Contraintes")
#exec(open("Model_MHE.py").read())
exec(open("Model_MHE.py").read())
print(" Model Ok")
### PArtie 5 Solce
print("Debut optimisation")
opt=SolverFactory("ipopt")      
#opt=SolverFactory('mindtpy')  
#opt.options['max_iter']= 5000       
result=opt.solve(model,tee=True)      



print("Solve Ok")
### Partie 5 : Ecriture Resultats
print("Partie 5: Ecriture Résultats")
exec(open("export.py").read())
print("Export OK")
print("^-^ Simulation fini ^-^")
