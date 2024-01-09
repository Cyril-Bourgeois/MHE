# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:18:49 2021

@author: bourgeoisc, neverren

Master Script:
Activation Scenario 
sub-model call
Writring Result
"""

# Import modules
import pyomo
from pyomo.environ import *
from pyomo.opt import SolverFactory

# Import library

import pandas as pd
import numpy as np
import csv
import os


####### Repertory Definition 
Data="./Input"
Output_file="./Output"
####### Month Defintion
Months=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre"]
#Months=["January","February","March","April","May","June","July","August","September","October","November","December"]
####### Défintion des pas de temps
time=range(1,13,1)

####### Scenario ## 

## Choice Scenario (manually):
##See Param_scenario for the signigication of scenario

## 1. Climate
Scenario_hydro = "Dry"  # Choce: Ref, LWTF, Dry, ExtendedDry (Ref,DOE,Sec,SecEtendue)
print("Scenario hydro :" , Scenario_hydro) 

## 2. MEtabolite
Scenario_Metabolite = "Ref"  # Choice: Ref,Abandon,AbandonMax,AbandonMaxK
print("Scenario_Metabolite :" , Scenario_Metabolite) 

## 3. Demand
### For reminder :
    #Seasonal spread=  more tourism in mid-seasonr
    #Population increase:  10% pop growth on littoral municipality
    #Tourism: Increase summer tourism in Crozon
    #Syndicat connection outside SMA : CapSizun Syndicate, Goyen sindicate


# Seasonal spread 
Activation_Etalement_Saisonnier= "Yes"  # Choice Yes/No  
print("Activation_Etalement_Saisonnier :" , Activation_Etalement_Saisonnier) 
#Population increase
Activation_Hausse_Population= "Yes"  # Choice Yes/No
print("Activation_Hausse_Population :" , Activation_Hausse_Population) 
#Tourism
Activation_Hausse_tourisme= "Yes"  #  Choice Yes/No
print("Activation_Hausse_tourisme :" , Activation_Hausse_tourisme) 
#Syndicat connection outside SMA
Activation_CapSizun= "Yes"  ## Choice Yes/No
Activation_Goyen= "Yes"  # # Choice Yes/No 
print("Activation_CapSizun_Goyen :" , Activation_CapSizun +'_'+ Activation_Goyen) 

## 4. Crisis Scenario
Activation_Crise= "Yes"  # Choice Yes/No
if Activation_Crise=="Yes":
    Mois_crise="Janvier" #  Month Choice = Août, Septembre, Janvier (August, September, January)
print("Activation_Crise :" , Activation_Crise) 


### Option: Activation node LeJuch-Kernevez (# Choice Yes/No)
scenario_Juch_Kernevez="No"
print("scenario_Juch_Kernevez :" , scenario_Juch_Kernevez) 


## 5. Adaptation measure (mesure_gestion)

#Mesure_gestion= "No" #  Choice Yes/No
#if Mesure_gestion=="Yes"
# Rendement (Yield of drinking water supply system))
Scenario_Rendement="No" #Choice Yes/No
print("Scenario_Rendement :" , Scenario_Rendement) 
if Scenario_Rendement=="No":
    mesure1="0"
else:
    mesure1="1"
# Economie d'eau (Water Restriction)
Scenario_baisse_demande="No" #  Choice No/Medium(5%), Max(10%)
print("Scenario_baisse_demande :" , Scenario_baisse_demande) 
if Scenario_baisse_demande=="No":
    mesure2="0"
elif Scenario_baisse_demande=="Medium":
    mesure2="1"
elif Scenario_baisse_demande=="Max":
    mesure2="2"
    
#Brennilis (filling of major Dam)
scenario_brennilis="No" # Choix Max (9Mm3), Medium(7.5 Mm3), Non(5.5 Mm3)
print("scenario_brennilis :" , scenario_brennilis) 
if scenario_brennilis=="No":
    mesure3="0"
elif scenario_brennilis=="Medium":
    mesure3="1"
elif scenario_brennilis=="Max":
    mesure3="2"
# Interco globale
scenario_interco_globale="No"   #Choice Yes/no
if scenario_interco_globale=="Yes":
    activation_Douarnenez_Lejuch=1 #(1 Node activated, 0 no node)
    activation_Cuzon=1
    mesure4="DLJ"+str(activation_Douarnenez_Lejuch)+"RC"+str(activation_Cuzon)
else:
    mesure4="DLJ0RC0"
print("scenario_interco_globale :" ,  mesure4) 

# Kerstrat (increased local production)
scenario_Kerstrat="No"   #Choice Yes/no
if scenario_Kerstrat=="No":
    mesure4b="0"
else:
    mesure4b="1"
    
# Local interco
scenario_interco_locale="No"   #Choice Yes/No
print("scenario_interco_locale :" , scenario_interco_globale+scenario_interco_locale) 
if scenario_interco_locale=="No":
    mesure5="0"
else:
    mesure5="1"
# New career 
scenario_nouvelles_carriere="No"   #Choice Yes/No
if scenario_nouvelles_carriere=="Yes":
    Carriere_plessis=0 ##(1 carreer activated, 0 no carrer)
    Carriere_loquefret=0 ##(1 carreer activated, 0 no carrer)
    Carriere_MenezMolve=0 ##(1 carreer activated, 0 no carrer)
    Carriere_SaintEvarzec=1  ##(1 carreer activated, 0 no carrer)
    mesure6="p"+str(Carriere_plessis)+"l"+str(Carriere_loquefret)+"m"+ str(Carriere_MenezMolve)+"E"+str(Carriere_SaintEvarzec)
if scenario_nouvelles_carriere=="No":
    mesure6="p0l0m0"
  
print("scenario_nouvelles_carriere :" , scenario_nouvelles_carriere+mesure6) 

# New Ressorces CCPF
scenario_nouvelles_Ressources="No" 
if scenario_nouvelles_Ressources=="Yes":
    Secteur_Benodet=1 #Choix0/1 ##(1 New ressource activated, 0 nonex ressource)
    Secteur_RoudGwen=1 #Choix0/1 ##(1 New ressource activated, 0 nonex ressource)
    Secteur_Lanveron=1 #Choix0/1 ##(1 New ressource activated, 0 nonex ressource)
    Secteur_PenALen=1 #Choix0/1 ##(1 New ressource activated, 0 nonex ressource)
    Secteur_Brehoulou=1 #Choix0/1 ##(1 New ressource activated, 0 nonex ressource)
    mesure7="NR"+str(Secteur_Benodet)+str(Secteur_RoudGwen)+str(Secteur_Lanveron)+str(Secteur_PenALen)+str(Secteur_Brehoulou)
if scenario_nouvelles_Ressources=="No":
    mesure7="NR00000"
    
# Resilience through local Storage
scenario_Resilience_Stockage="No" #Choice Yes/No
if scenario_Resilience_Stockage=="Yes":
    Activation_Poraon=1  #Choice 0/1
    Activation_Keryannes= 1  # Choice 0/1
    mesure8="P"+str(Activation_Poraon)+"K"+str(Activation_Keryannes)
else:
    mesure8="P0K0"
print("scenario_Resilience_Stockage :" , scenario_Resilience_Stockage) 

# # Resilience through Boreholes
scenario_Resilience_forage='No' #Choix Yes/No
print("scenario_Resilience_forage :" , scenario_Resilience_forage) 
if scenario_Resilience_forage=="No":
    mesure9="0"
else:
    mesure9="1"
#print(Scenario_autres)

####### Name Scenario
if Activation_Crise== "Non" :
    name_simulation='H'+Scenario_hydro+'-M'+Scenario_Metabolite +'-ES_'+Activation_Etalement_Saisonnier +'-HP_'+Activation_Hausse_Population +'-HT_'+ Activation_Hausse_tourisme + 'CS-Go_'+  Activation_CapSizun +'_'+ Activation_Goyen+'-Crise_'+Activation_Crise+ '-LJK'+scenario_Juch_Kernevez+ '-Gestion'+mesure1+mesure2+mesure3+mesure4+mesure4b+mesure5+mesure6+mesure7+mesure8+mesure9
else :
     name_simulation='H'+Scenario_hydro+'-M'+Scenario_Metabolite +'-ES_'+Activation_Etalement_Saisonnier +'-HP_'+Activation_Hausse_Population +'-HT_'+ Activation_Hausse_tourisme + 'CS-Go_'+  Activation_CapSizun +'_'+ Activation_Goyen+'-Crise_'+Activation_Crise+Mois_crise+ '-LJK'+scenario_Juch_Kernevez+'-Gestion'+mesure1+mesure2+mesure3+mesure4+mesure4b+mesure5+mesure6+mesure7+mesure8+mesure9

#name_simulation="AtelierNew"+'_'+name_simulation
name_simulation="test_kerrous"+'_'+name_simulation




print(name_simulation)
Output=Output_file+'/'+name_simulation
os.makedirs(Output, exist_ok=True)
name_output=Output+'/results_'


#### Hydrologie Data repository
dossier_Hydro='./Input/A - DEBITS PRELEVABLES AULNE ET ST MICHEL - Modif 28_04_22/'
dossier_Hydro_kerrous='./Input/A - Steir Guengat_V2/'

###### Subpart call
### Part 1:  Paramater and scenario definiton
print(" Part 1 :Paramater and scenario definiton")
###1.1 Scenario parameter  read
print("Scenario parameter  read")
exec(open("param_scenario.py").read())
###1.2 Cost fucntion paramater read
print("Cost fucntion parmater read")
exec(open("param_cout.py").read())

###1.3 Cost function load
print("Cost function load")
exec(open("fonctions.py").read())

print("Part1 Ok")

### Part 2: Data
print(" Partie 2 : Data read")
#2.1  read data  csv
exec(open("lecture_data.py").read())

print("Data OK")

### Part 3:  Scenario
#3.1 Scenario definiton
print(" Part 3 : Scenario Definition")
exec(open("Scenario.py").read())
#3.2 Adaptation scenario definition
print(" PArtie 3 : Adaptation scenario definitation")
exec(open("Mesure_gestion.py").read())

### Part 4: Model Defintion (Objective and constraints)
print("Part 4: Model Defintion (Objective and constraints)")
#exec(open("Model_MHE.py").read())
exec(open("Model_MHE.py").read())
print(" Model Ok")

### PArt5: Solve
print("Start optimization")
opt=SolverFactory("ipopt")      
#opt=SolverFactory('mindtpy')  
#opt.options['max_iter']= 5000       
result=opt.solve(model,tee=True)      
print("Solve Ok")

### Part 5 : Write Results
print("Part 5 : Write Results")
exec(open("export.py").read())
print("Export OK")
print("^-^ End Simulation ^-^")
