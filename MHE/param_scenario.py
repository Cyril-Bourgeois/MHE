# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 19:08:47 2021

@author: bourgeoisc,neverren
"""

###############################################################################
###############           Parametre      Scenario           ###################
######################à#########################################################

#### Paramètre  du Scénario Hydro
if Scenario_hydro == "Ref" :
         scenario_ouv_hydro=["K_hydro_moy_1", "K_hydro_moy_2", "K_hydro_moy_3", "K_hydro_moy_4", "K_hydro_moy_5","K_hydro_moy_6",
                 "K_hydro_moy_7", "K_hydro_moy_8", "K_hydro_moy_9", "K_hydro_moy_10", "K_hydro_moy_11", "K_hydro_moy_12"]
         scenario_surf=[1,1,1,1,1,1,1,1,1,1,1,1] #New Carrer monthly productivity constraint with respect to climate
         Stock_SM=dossier_Hydro+'AAA_Monthly-2015-DOE-1.8 correction-1.csv'
         Stock_Kerrous=dossier_Hydro_kerrous+'AAA_Monthly-2015-DOE-0.38 correction-1.csv'
     
if Scenario_hydro=="LWTF":
         scenario_ouv_hydro=["K_hydro_moy_1", "K_hydro_moy_2", "K_hydro_moy_3", "K_hydro_moy_4", "K_hydro_moy_5","K_hydro_moy_6",
                 "K_hydro_moy_7", "K_hydro_moy_8", "K_hydro_moy_9", "K_hydro_moy_10", "K_hydro_moy_11", "K_hydro_moy_12"] 
         Stock_SM=dossier_Hydro+'AAA_Monthly-2015-DOE-2.15 correction-1.csv'
         Stock_Kerrous=dossier_Hydro_kerrous+'AAA_Monthly-2015-DOE-0.38 correction-1.csv'
         scenario_surf=[1,1,1,1,1,1,1,1,1,1,1,1]
if Scenario_hydro == "Dry":
         scenario_ouv_hydro=["K_hydro_sec_1", "K_hydro_sec_2", "K_hydro_sec_3", "K_hydro_sec_4", "K_hydro_sec_5","K_hydro_sec_6",
                  "K_hydro_sec_7", "K_hydro_sec_8", "K_hydro_sec_9", "K_hydro_sec_10", "K_hydro_sec_11", "K_hydro_sec_12"] 
         Stock_SM=dossier_Hydro+'AAA_Monthly-2011-DOE-1.8 correction-1.csv'
         Stock_Kerrous=dossier_Hydro_kerrous+'AAA_Monthly-2011-DOE-0.38 correction-1.csv'
         scenario_surf=[1,1,1,1,1,1,1,1,1,1,1,1]
if Scenario_hydro == "ExtendedDry":
         scenario_ouv_hydro=["K_hydro_Etendue_1", "K_hydro_Etendue_2", "K_hydro_Etendue_3", "K_hydro_Etendue_4", "K_hydro_Etendue_5","K_hydro_Etendue_6",
                  "K_hydro_Etendue_7", "K_hydro_Etendue_8", "K_hydro_Etendue_9", "K_hydro_Etendue_10", "K_hydro_Etendue_11", "K_hydro_Etendue_12"] 
         Stock_SM=dossier_Hydro+'AAA_Monthly-2011-DOE-1.8 correction-0.85.csv' 
         Stock_Kerrous=dossier_Hydro_kerrous+'AAA_Monthly-2011-DOE-0.38 correction-0.85.csv' 
         scenario_surf=[1,1,1,1,1,1, 0.75,0.75,0.75,0.75,0.85,1]


#### Scenario parameter Metabolite
if  Scenario_Metabolite == "Abandon":
    Indice_Metabolite=0
    Usine_Meta=["T1052","T2011","T2031","T6051","T3031"]  # CCPCAM: Pouldu, DzCO:"Nankou" et "Kerstrat", QBO:"Kernevez", CCHPB:"Saint-Ronan"
elif Scenario_Metabolite == "AbandonMax":
    Indice_Metabolite=0
    Usine_Meta=["T1052","T2011","T2031","T6051","T3031", "T1021","T2041","T3011","T3021","T4021","T4022","T5031","T5032","T5151","T5162","T6011","T6061","T6071","T6121","T6131"] 
    ## CCPCAM:"Kernagoff" et "Pouldu" DZCO:"Nankou", "Kerstrat" et Lezaff, CCPF: "Keraven" et "Cheffontaines",
    ## CCPCP: "Kergaoc", "Kernevez" "Runigo Vihan" et "Moulin Neuf", QBO: "Kernevez", "Kergoat", "Boissavarn","Kervoellic" "Kermaria/landulal", "Kerzouaelen"
    ## CCHPB: "Saint-Ronan, Kergamet, Saint-avé
elif Scenario_Metabolite == "AbandonMaxK":
    Indice_Metabolite=0
    Usine_Meta=["T1052","T2011","T2031","T3031", "T1021","T2041","T3011","T3021","T4021","T4022","T5031","T5032","T5151","T5162","T6011","T6061","T6071","T6121","T6131"] 
    Indice_For=0
    For_meta=['29000247','29001504','29000997']

#### PArameter of demand scenario
### Definition of tourist communities :
# CCPCAM: The 2 URDs of the Crozon peninsula
# CCPCP: Saint-Nic, Plomordien, Ploëven, Plonevez-Porzay,
# DzCo : Douarnenez, Kerlaz, Pouldergat
# QBO : Plomelin
# CCPF : Bénodet, Fouesnant, la Forêt-Fouesnant
# CCHPB: Plozévet, Pouldreuzic, Plovan, Tréogat

### Population_Increase
Coef_pop=0.1
Communes_hausse_pop=['101','102','201','202','204','303','401','402','403','502','504','505','506','606']

### Seasonal spread ## Addition of Quimper 
Communes_touristiques=Communes_hausse_pop+['614']
#voir scenario.py
### Tourisme Increase 
Com_hausse_toursime=['101','102']
#voir Scénario.py


### Crisis Scenario:
index_time=time
df_crise = pd.DataFrame({'index_time':index_time,'Months':Months})
df_crise=df_crise.assign(crise=1)
df_crise=df_crise.set_index('index_time') 
    
### Adaptation Scenario
# Lower water demand
param_baisse_demande=0.10
param_baisse_demande2=0.05
# New Career
Stock_Plessis=500000
Stock_Loquefret=8000000
Stock_MenezMolve=800000
SaintEvarzec= '29000197'  #Alimente PenAlen

Coef_Plessis=1-0.25
Coef_Loquefret=1-0.4
Coef_MenezMolve=1-0.4
  
#Secure drilling
#Sites concerned :
#- CCPCAM: Goastallan, Le pouldu, Pen Ar Vern
#- CCPCP: Runigou Vihan, Plomodiern (Dour bihan), Châteaulin (the 2 wells), Moulin neuf, Kerbalaen (3sites)
#- CCPF: Cheffontaines, Roud gwen, Trouarn
#- QBO: Reuniat, Goutliquer, Kernevez (reinforcement of existing well)
Securisation_forage=['29000275','29000274','29000194',
                     '29000232','29000258','29001540','29001522', '29000203','29000251','29000999','29000998',
                     '29000157','29002110','29001319',
                     '29000247','29001504','29000255','29000172']   
Captage_ref='29001501'

# Resilience Storage
## Concerns Poraon and Kergaouelen/keryannes
SPoraon=['29000279']
SKeryannes=['29000190','29000190']

### Interco_globale
### Moulin <--> Douarnenez
Interco_globale1=[('201_R2031'),
                 ('R2031_201')]
### ### Troheïr plant --> Cuzon  
Interco_globale2=[('T6141_R6141')]

#Augmentation Kerstrat 100 000-->300 000
Kerstrat="T2031"

#### 2. Interco locale
Interco_locale=[('201_202')]


### Liens Le Juck - Kernevez
Juch_Kernevez=[('R2031_T6051')]
