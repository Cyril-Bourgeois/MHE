# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:21:00 2022

@author: bourgeoisc
"""

###############################################################################
###############          Paramater Adaptation measures          ################
###############################################################################


################## Appy scénario   ################################
#### 0. Interco Le Juch-Kernever (locale interconnection, not studeid in article)
if  (scenario_Juch_Kernevez=="No"):#Double sésurité
    #Works in reverse if no scenario, links must be removed
    indexNames = Liens[Liens.ID_lien.isin(Juch_Kernevez)].index 
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)

  
#### 1. Global interconnection    
if  (scenario_interco_globale=="Yes") :
     # DzCO interco
    if  (activation_Douarnenez_Lejuch==1) & (activation_Cuzon==0):#Double security
        Interco_globale=Interco_globale2 # # Works in reverse if Douardannez is active, Cuzon link must be removed
        indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
        Liens.drop(indexNames , inplace=True)
     # Cuzon interco
    if (activation_Cuzon==1) & (activation_Douarnenez_Lejuch==0):##Double security
        Interco_globale=Interco_globale1  # Works in reverse if Cuzon is active, the Douardennez link must be removed
        indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
        Liens.drop(indexNames , inplace=True)    
    Liens.reset_index(drop=True, inplace=True)
if  (scenario_interco_globale=="No"):#Double sésurité
    Interco_globale=Interco_globale1+Interco_globale2 #Works in reverse if no scenario, links must be removed
    indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)

# KErstrat Interco
if scenario_Kerstrat=="Yes":
    Usines.K[Kerstrat]=1000

#### 2. local Interco (not used in article)
if scenario_interco_locale=="No":
    indexNames = Liens[Liens.ID_lien.isin(Interco_locale)].index
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)
 

if scenario_interco_locale=="Yes" :
    Coef_Kerandouare_landulec= 90
    Coef_Crozon_EO=180
else:
    Coef_Kerandouare_landulec=45
    Coef_Crozon_EO=180
    
#### 3. Filling capacity at Brennilis
if scenario_brennilis=="Max":
    Initial_Stock[0:6]=10000000
if scenario_brennilis=="Medium":
    Initial_Stock[0:6]=7500000
    
#### 4. New Career

if scenario_nouvelles_carriere=="Yes":
    Stock_carriere=  (Carriere_plessis*Stock_Plessis *Coef_Plessis + Carriere_loquefret*Stock_Loquefret*Coef_Loquefret+ Carriere_MenezMolve*Stock_MenezMolve*Coef_MenezMolve)/perte_lacher
elif scenario_nouvelles_carriere=="No":
    Stock_carriere=  0
if (scenario_nouvelles_carriere=="Yes"):
    if (Carriere_SaintEvarzec==1):
        Ouvrages.loc[SaintEvarzec, scenario_ouv_hydro]= scenario_surf
         
#### 5. Boreholes resilience (Résilience Forages)

if scenario_Resilience_forage=="Yes":
    for cap in Securisation_forage:
        Ouvrages.loc[cap, scenario_ouv_hydro]=Ouvrages.loc[Captage_ref, scenario_ouv_hydro]
         
#### 6.  Stoackage Resilience (Résilience Stockage)
if scenario_Resilience_Stockage=="Yes":
    if  (Activation_Poraon==1) & (Activation_Keryannes==1):
        Securisation_stockage=SPoraon+SKeryannes
    if (Activation_Poraon==1) & (Activation_Keryannes==0):  
        Securisation_stockage=SPoraon
    if  (Activation_Poraon==0) & (Activation_Keryannes==1):      
        Securisation_stockage=SKeryannes
    
if scenario_Resilience_Stockage=="Yes":
    for esu in Securisation_stockage:
        Ouvrages.loc[esu, scenario_ouv_hydro]= scenario_surf
        
#### New Resources
if scenario_nouvelles_Ressources=="Yes":
    if Secteur_Benodet==1:
        Ouvrages.K_aut_jr['290020552']=710# Guenoudou
        Ouvrages.K_aut_jr['290020551']=390# Keraven
        Ouvrages.K_aut_jr['290001571']=1200# Cheffontaines
        Usines.K['T4021']=3200
        Usines.K['T4022']=1450
        
    if Secteur_RoudGwen==1:
        Ouvrages.K_aut_jr['290021101']=720# Forage RoudGwen
        Usines.K['T4031']=1520
    if Secteur_Lanveron ==1:
        Ouvrages.K_aut_jr['290013191']=290# BoisdeMur
        Ouvrages.K_aut_jr['290013192']=600# Lanveron
        Usines.K['T4051']=1500
    if Secteur_PenALen ==1:
        Ouvrages.K_aut_jr['290001971']=1200# Kervrancel/rosnabat
        Usines.K['T4041']=5200
    if Secteur_Brehoulou ==1:
        Ouvrages.K_aut_jr['29002240']=840# Brehoulou F2
        Ouvrages.K_aut_jr['2900224']=840# Brehoulou F3
        
        Usines.K['T4012']=2500
        
####8. Lower water demand
if Scenario_baisse_demande=="Max":
    coef_baisse_demande=1-param_baisse_demande 
    Demande.VCA2019=Demande.VCA2019*coef_baisse_demande
if Scenario_baisse_demande=="Medium":      
    coef_baisse_demande=1-param_baisse_demande2 
    Demande.VCA2019=Demande.VCA2019*coef_baisse_demande
    
        
####9. Yield
if Scenario_Rendement=="Yes":    
    Demande['Rendement']=pd.to_numeric(Demande.Objectif_rendement_gestion)
 
