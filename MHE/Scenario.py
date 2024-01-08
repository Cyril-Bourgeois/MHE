# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 10:39:23 2021

@author: bourgeoisc, neverren
"""

###############################################################################
###############          Parametre      Scenario           ###################
###############################################################################


################## Application des scénarios   ################################
            


#### Application des paramètres du scénario hydro sur les ouvrages:
     
#Ouvrages[Months_Kh]=Ouvrages[scenario_ouv_hydro]

#### Application des Scénarios Métabolites
if Scenario_Metabolite == "Abandon" or Scenario_Metabolite == "AbandonMax":
    for i in Usine_Meta:
        Usines.loc[i,'K']=Indice_Metabolite
if Scenario_Metabolite ==  "AbandonMaxK":
    for i in Usine_Meta:
        Usines.loc[i,'K']=Indice_Metabolite
    for i in For_meta:
        Ouvrages.loc[i,'K_aut_jr']=Indice_For
        

### Application de la hausse de la population
if Activation_Hausse_Population== "Oui":
    for com in Communes_hausse_pop:
        Demande_reference=np.mean(Demande.loc[com,[Months[0],Months[1],Months[3],Months[10],Months[11]]])
        delta_demande=Demande_reference*Coef_pop
        for t in time:
            Demande.loc[com,Months[t-1]] =Demande.loc[com,Months[t-1]]  + delta_demande          
      

### Application de l'étalement Saisonnier
if Activation_Etalement_Saisonnier== "Oui":
    for com in Communes_touristiques:
      Demande.loc[com,Months[8]] =Demande.loc[com,Months[5]] # o	Septembre : Application du niveau de consommation historique du mois de Juin
      Demande.loc[com,Months[9]] =Demande.loc[com,Months[4]] # o	Octobre : Application du niveau de consommation historique du mois de Mai 
      Demande.loc[com,Months[10]]=Demande.loc[com,Months[3]] # o	Novembre : Application du niveau de consommation historique du mois d’Avril 
      Demande.loc[com,Months[3]] =Demande.loc[com,Months[4]] # o	Avril : Application du niveau de consommation historique du mois de Mai 
      Demande.loc[com,Months[4]] =Demande.loc[com,Months[5]] # o	Mai : Application du niveau de consommation historique du mois de Juin 
      Demande.loc[com,Months[5]] =9 # o	Juin : Augmentation de la consommation, pour atteindre 9% de la consommation annuelle historique.

### Application de la hausse estivale de touristique
if Activation_Hausse_tourisme== "Oui":
    for com2 in Com_hausse_toursime:
        delta=(Demande.loc[com2,Months[7]] -Demande.loc[com2,Months[6]])/Demande.loc[com2,Months[6]]
        Demande.loc[com,Months[6]] =Demande.loc[com,Months[7]]            # o	La fréquentation actuelle du mois d’aout est appliquée au mois de juillet (soit +7,5% de demande en juillet)
        Demande.loc[com,Months[7]] =Demande.loc[com,Months[7]]*(1+delta)  # o	Le delta de fréquentation entre juillet et aout est ajouté à la fréquentation du mois d’aout (soit +7% de demande en aout). 

### Application du scénario de crise
if Activation_Crise== "Oui":
    coef_crise=0
    df_crise.loc[df_crise['Months']==Mois_crise,'crise'] =coef_crise ### A activiter sur les USines SMA.!!
    
### Actication Scénario Goyen
if Activation_Goyen== "Non": # Pour rappel par défault on apprivionne 15j, et quand on active on apprivisionne le mois entier
    Demande.loc[Demande['Nom_URD']=="Goyen",'VCA2019']=Demande.loc[Demande['Nom_URD']=="Goyen",'VCA2019']/2
    
if Activation_CapSizun== "Non" :#(on approviosonne pas le sizunpar défault)    
    Demande.loc[Demande['Nom_URD']=="Nord-Cap-Sizun",'VCA2019']=0
