# -*- coding: utf-8 -*-
"""
Created on Mon May 16 10:21:00 2022

@author: bourgeoisc
"""

###############################################################################
###############          Parametre  Mesure de destion          ################
###############################################################################


################## Application des scénarios   ################################
#### 0. Liens le Juck-Kernevez
if  (scenario_Juch_Kernevez=="Non"):#Double sésurité
     # Fonctionne à l'envers si aucun scénario il faut retirer les lines
    indexNames = Liens[Liens.ID_lien.isin(Juch_Kernevez)].index 
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)

  
#### 1. Interco globable          
if  (scenario_interco_globale=="Oui") :
    if  (activation_Douarnenez_Lejuch==1) & (activation_Cuzon==0):#Double sésurité
        Interco_globale=Interco_globale2 # Fonctionne à l'envers si Douardannez est activité, il faut retirer le lien de Cuzon
        indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
        Liens.drop(indexNames , inplace=True)

    if (activation_Cuzon==1) & (activation_Douarnenez_Lejuch==0):#Double sésurité
        Interco_globale=Interco_globale1 # Fonctionne à l'envers si Cuzon est activité, il faut retirer le lien de Douardennez
        indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
        Liens.drop(indexNames , inplace=True)    
    Liens.reset_index(drop=True, inplace=True)
if  (scenario_interco_globale=="Non"):#Double sésurité
    Interco_globale=Interco_globale1+Interco_globale2 # Fonctionne à l'envers si aucun scénario il faut retirer les lines
    indexNames = Liens[Liens.ID_lien.isin(Interco_globale)].index 
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)


if scenario_Kerstrat=="Oui":
    Usines.K[Kerstrat]=1000

#### 2. Interco locale
if scenario_interco_locale=="Non":
    indexNames = Liens[Liens.ID_lien.isin(Interco_locale)].index
    Liens.drop(indexNames , inplace=True)
    Liens.reset_index(drop=True, inplace=True)
 

if scenario_interco_locale=="Oui" :
    Coef_Kerandouare_landulec= 90
    Coef_Crozon_EO=180
else:
    Coef_Kerandouare_landulec=45
    Coef_Crozon_EO=180
    
#### 3. Brenillis
if scenario_brennilis=="Max":
    Initial_Stock[0:6]=10000000
if scenario_brennilis=="Medium":
    Initial_Stock[0:6]=7500000
    
#### 4. Nouvelles Carrières



if scenario_nouvelles_carriere=="Oui":
    Stock_carriere=  (Carriere_plessis*Stock_Plessis *Coef_Plessis + Carriere_loquefret*Stock_Loquefret*Coef_Loquefret+ Carriere_MenezMolve*Stock_MenezMolve*Coef_MenezMolve)/perte_lacher
elif scenario_nouvelles_carriere=="Non":
    Stock_carriere=  0
if (scenario_nouvelles_carriere=="Oui"):
    if (Carriere_SaintEvarzec==1):
        Ouvrages.loc[SaintEvarzec, scenario_ouv_hydro]= scenario_surf
#### 5. Résilience Forages

if scenario_Resilience_forage=="Oui":
    for cap in Securisation_forage:
        Ouvrages.loc[cap, scenario_ouv_hydro]=Ouvrages.loc[Captage_ref, scenario_ouv_hydro]
#### 6. Résilience Stockage
if scenario_Resilience_Stockage=="Oui":
    if  (Activation_Poraon==1) & (Activation_Keryannes==1):
        Securisation_stockage=SPoraon+SKeryannes
    if (Activation_Poraon==1) & (Activation_Keryannes==0):  
        Securisation_stockage=SPoraon
    if  (Activation_Poraon==0) & (Activation_Keryannes==1):      
        Securisation_stockage=SKeryannes
    
    
if scenario_Resilience_Stockage=="Oui":
    for esu in Securisation_stockage:
        Ouvrages.loc[esu, scenario_ouv_hydro]= scenario_surf
        
#### Nouvelle Ressources
if scenario_nouvelles_Ressources=="Oui":
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
        
####8. Baisse de la demande en eau
if Scenario_baisse_demande=="Max":
    coef_baisse_demande=1-param_baisse_demande 
    Demande.VCA2019=Demande.VCA2019*coef_baisse_demande
if Scenario_baisse_demande=="Medium":      
    coef_baisse_demande=1-param_baisse_demande2 
    Demande.VCA2019=Demande.VCA2019*coef_baisse_demande
    
        
####9. Rendement
if Scenario_Rendement=="Oui":    
    Demande['Rendement']=pd.to_numeric(Demande.Objectif_rendement_gestion)
 