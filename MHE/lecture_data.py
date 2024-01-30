# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 10:44:34 2021

@author: bourgeoisc, neverren
"""

###############################################################################
###########                      DATA                 #########################
###############################################################################

####### Water abstraction and resources structures data (=Supply )
Ouvrages = pd.read_csv(Donnees+'/BDD_OUV.csv',sep=',')
Ouvrages = Ouvrages.astype({"ID": str})
Ouvrages=Ouvrages.set_index('ID') 
List_OUV=list(Ouvrages.index) 
### SMA identification
Ouvrages_SMA=Ouvrages.loc[Ouvrages["Nom_COMCOM"]=="SMA"]
### Kerrous is only concerned by managment measures 
Ouvrages_Kerrous=Ouvrages.loc[Ouvrages["ID_TTP"]=='T6141']
Ouvrages_noSMA=Ouvrages.loc[(Ouvrages["Nom_COMCOM"]!="SMA") & (Ouvrages["ID_TTP"]!='T6141')]


####### Treatment Plants Data
Usines=pd.read_csv(Donnees+'/BDD_TTP.csv',sep=',')
Usines=Usines.set_index('ID_TTP')
List_usine=list(Usines.index)
### SMA treatment plant identification
Usines_SMA=Usines.loc[Usines["Nom_COMCOM"]=="SMA"]

####### Other intermediate nodes (Reservoirs or Others)
noeuds=pd.read_csv(Donnees+'/BDD_Noeuds.csv',sep=',')
noeuds=noeuds.set_index('ID')
List_reservoir=list(noeuds.index)
List_noeud= List_usine+List_reservoir

###### Distribution Unit 
Demande=pd.read_csv(Donnees+'/BDD_URD.csv',sep=';', decimal=",")
Demande = Demande.astype({"ID_URD": str})
Demande=Demande.set_index('ID_URD')
#### Yield
Demande.Rendement.fillna(100, inplace=True)
List_URD=list(Demande.index) 

### Water import (outside Area Study, not explicitly modeled) 
import_URD=pd.read_csv(Donnees+'/BDD_imports.csv',sep=',', decimal=".")
import_URD=import_URD[import_URD['ID_URD']=="HP3"]#FixME
import_URD= import_URD.astype({"ID_URD": str})
import_URD=import_URD.set_index('ID_URD')
List_import=list(import_URD.index)

####### Water Road ("Linked")
Liens=pd.read_csv(Donnees+'/BDD_Liens.csv',sep=',')
URD_Ouvrages=Liens[Liens.Type_depart =="OUV"][["ID_depart","ID_URD_depart"]]
URD_Ouvrages=URD_Ouvrages.set_index('ID_depart')

####### Failure possibility (if not existing, the model could be not solved)
Liens_def=pd.read_csv(Donnees+'/URD_defaillance.csv',sep=',')
Liens_def.columns=['ID_depart', 'ID_arrivee',"xx"]
Liens_def =Liens_def.astype({"ID_depart": str,"ID_arrivee": str})

### Diameter stress on a pipe (special case)
Liens.Diametre[Liens['ID_lien']=="201_204"]=225

######
Liens_def=Liens_def.merge(Demande, how='left', left_on='ID_arrivee', right_on='ID_URD')


########### Failure cost
Def_cost=pd.read_csv(Donnees+'/Cout_Defaillance.csv',sep=';', header=None)
Def_cost.columns =['ID_depart', 'Cost']
Def_cost=Def_cost.astype({"ID_depart": str})
Def_cost=Def_cost.set_index('ID_depart') 


######### Brenilis Data
#SM=pd.read_csv(Donnees+Stock_SM, sep=";")
SM=pd.read_csv(Stock_SM, sep=";")
Initial_Stock=SM["Vol_Lastday"]## NB pythyon commence à 0 donc mai = 5-1 et on prend le stock au 31 mai
Recharge=SM["Recharge_m3_Mois"]
Vol_soutien=-SM["Volume_Soutien_PMIN_Jour"]
Vol_prelevable=SM["Volume_Disponible_PMIN_Jour"]

######### Kerrous Data 
Kerrous=pd.read_csv(Stock_Kerrous, sep=";")
Initial_Stock_Kerrous=1200000## NB pythyon commence à 0 donc mai = 5-1 et on prend le stock au 31 mai
Vol_soutien_Kerrous=-Kerrous["Volume_Soutien_DOE"]
Vol_prelevable_Kerrous=Kerrous["Volume_Disponible_DOE"]
