# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 10:39:23 2021

@author: bourgeoisc, neverren
"""

###############################################################################
###############          Parameter Scenario         ###################
###############################################################################


################## Apply scénario   ################################
            


#### Application of hydro scenario parameters to structures:


#### Application of Metabolite Scenarios (not studied in article)
if Scenario_Metabolite == "Abandon" or Scenario_Metabolite == "AbandonMax":
    for i in Usine_Meta:
        Usines.loc[i,'K']=Indice_Metabolite
if Scenario_Metabolite ==  "AbandonMaxK":
    for i in Usine_Meta:
        Usines.loc[i,'K']=Indice_Metabolite
    for i in For_meta:
        Ouvrages.loc[i,'K_aut_jr']=Indice_For
        

### Application of the population increase
if Activation_Hausse_Population== "Yes":
    for com in Communes_hausse_pop:
        Demande_reference=np.mean(Demande.loc[com,[Months[0],Months[1],Months[3],Months[10],Months[11]]])
        delta_demande=Demande_reference*Coef_pop
        for t in time:
            Demande.loc[com,Months[t-1]] =Demande.loc[com,Months[t-1]]  + delta_demande          
      

### Application of Seasonal Spread
if Activation_Etalement_Saisonnier== "Yes":
    for com in Communes_touristiques:
      Demande.loc[com,Months[8]] =Demande.loc[com,Months[5]] # o	September: Application of June's historical consumption level
      Demande.loc[com,Months[9]] =Demande.loc[com,Months[4]] # o	October: Application of May's historical consumption level 
      Demande.loc[com,Months[10]]=Demande.loc[com,Months[3]] # o	November: Application of April's historical consumption level 
      Demande.loc[com,Months[3]] =Demande.loc[com,Months[4]] # o	April: Application of May's historical consumption level
      Demande.loc[com,Months[4]] =Demande.loc[com,Months[5]] # o	May: Application of June's historical consumption level
      Demande.loc[com,Months[5]] =9                          # 	June: Consumption rises to 9% of historical annual consumption.

### Application of the summer tourist increase
if Activation_Hausse_tourisme== "Yes":
    for com2 in Com_hausse_toursime:
        delta=(Demande.loc[com2,Months[7]] -Demande.loc[com2,Months[6]])/Demande.loc[com2,Months[6]]
        Demande.loc[com,Months[6]] =Demande.loc[com,Months[7]]            # o	Current August demand applied to July (i.e. +7.5% demand in July)
        Demande.loc[com,Months[7]] =Demande.loc[com,Months[7]]*(1+delta)  # o	The delta in demand between July and August is added to the August demand (i.e. +7% demand in August). 

###Application of the crisis scenario
if Activation_Crise== "Yes":
    coef_crise=0
    df_crise.loc[df_crise['Months']==Mois_crise,'crise'] =coef_crise 
    
### Activation Goyen scenario
if Activation_Goyen== "No":  # As a reminder, the default setting is 15 days, and when activated, the entire month is billed.
    Demande.loc[Demande['Nom_URD']=="Goyen",'VCA2019']=Demande.loc[Demande['Nom_URD']=="Goyen",'VCA2019']/2
    
if Activation_CapSizun== "No" :#(sizun is not the default setting)     
    Demande.loc[Demande['Nom_URD']=="Nord-Cap-Sizun",'VCA2019']=0
