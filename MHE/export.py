# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 17:24:05 2021

@author: bourgeoisc, neverren

"""

###############################################################################
##############################  EXPORTS   #####################################
###############################################################################
# Writring transport cost results
output_transport = []
for (i,j) in Routes_reel :
        for t in time: 
            Cout_transfort_f={
                'index_mois':t,
                'Depart': i,
                'Arrivee': j,
                'Months': Months[t-1],
                'Volume': model.Q[(i,j,t)].value,
                'Diametre':Liens.Diametre[(i,j)],
                'Distance': 1000*Liens.distance[(i,j)],
                'Cout_transfort_f':cout_transport( model.Q[(i,j,t)].value,  Liens.Diametre[(i,j)],  1000*Liens.distance[(i,j)]) 
                }
            output_transport.append(Cout_transfort_f)
outputLiensReel_df = pd.DataFrame.from_records(output_transport).sort_values(['Depart','Arrivee','Months'])
# Writring transport cost results (failure cost)
output_transport_def = []
for (i,j) in Routes_def :
        for t in time: 
            Cout_transfort_f={
                'index_mois':t,
                'Depart': i,
                'Arrivee': j,
                'Months': Months[t-1],
                'Volume': model.Q[(i,j,t)].value,
                'Diametre':0,
                'Distance': 0,
                'Cout_transfort_f':0 
                }
            output_transport_def.append(Cout_transfort_f)
outputLiensDef_df= pd.DataFrame.from_records(output_transport_def).sort_values(['Depart','Arrivee','index_mois'])
outputLiens_df=pd.concat([outputLiensReel_df, outputLiensDef_df])
outputLiens_df.to_csv(name_Sorties+'Liens'+'.csv' )



### Writing URD results (Satisfying Demand, Failure, Export)

outputURD = []
for u in List_URD :
        for t in time:   
            Q_prod = sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if j == u])
            Q_def = sum([model.Q[((i,j),t)].value for (i,j) in Routes_def if j == u])
            Q_exp= sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if i == u])
            Q_sat= sum([model.Q[((ii,jj),t)].value  for (ii,jj) in Routes_reel if jj == u])*Demande.loc[u ,'Rendement']/100 - sum([model.Q[((i,j),t)].value   for (i,j) in Routes_reel if i == u])
            cout_def=sum([cout_defaillance(model.Q[((i,j),t)].value) for (i,j) in Routes_def if j == u])
            var_output = {
            'index_mois':t,
			'URD': u,
			'Months': Months[t-1]  ,
			'Volume_produit': Q_prod , 
            'Demande_satisfaite' : Q_sat, 
			'Defaillance': Q_def ,
			'Cout_defaillance':cout_def , 
			'Total_Q': Q_sat + Q_def ,
			'Demande' : Demande.loc[u, 'VCA2019']* Demande.loc[u, Months[t-1]]/100 ,
            'Volume_export': Q_exp,
			'Rdt' : Demande.loc[u ,'Rendement'] ,
			'Tx defaillance' : 100* Q_def / (Q_def + Q_sat +0.1),
            'X': Demande.X[u],
            'Y': Demande.Y[u]
		    }
            outputURD.append(var_output)
outputURD_df = pd.DataFrame.from_records(outputURD).sort_values(['URD','index_mois'])
outputURD_df
outputURD_df.to_csv(name_Sorties+'URD'+'.csv' )

### Wrtining Withdrawal result (Abstraction flux and cost, saturation rate )

outputOUV = []
for u in List_OUV :
    for t in time:  
        Q_prel = sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if i == u])
        K_prel = Ouvrages.K_aut_jr[u]*365/12* Ouvrages.loc[u, scenario_ouv_hydro[t-1]]
        K_DUP  = Ouvrages.K_aut_jr[u]*365/12
        cout_prel= cout_prelevement( Q_prel,  Ouvrages.loc[u,"Prof"],Ouvrages.loc[u,"Type_eau"]) 
         
        var_output = {
            'index_mois':t,
            'OUV': u,
			'Months': Months[t-1]  ,
            'COMCOM': Ouvrages.Nom_COMCOM[u],
            'URD':URD_Ouvrages.ID_URD_depart[u],
			'Preleve': Q_prel ,
			'Cout unitaire': cout_prel/Q_prel , 
			'Cout prelvt':  cout_prel ,
			'Capacité_DUP' :Ouvrages.K_aut_jr[u]*365/12 ,
            'Capacite_hydro': K_prel,
            'Tx_saturation_K' : 100 * Q_prel / (K_DUP+0.01),
			'Tx_saturation_K_hydro' : 100 * Q_prel / (K_prel+0.01),
            'X' : Ouvrages.X[u],
            'Y' : Ouvrages.Y[u]
		}
        outputOUV.append(var_output)
outputOUV_df = pd.DataFrame.from_records(outputOUV).sort_values(['OUV','index_mois'])
outputOUV_df
outputOUV_df.to_csv(name_Sorties+'OUV'+'.csv' )

### Wrtining Tratement plant result (Treated flux and cost, saturation rate )
outputTTP = []
for u in List_usine :
	for t in time:  
		Q_trait = sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if j == u])
		K_ttp = Usines.K[u]*365/12  # FIXME : il y aura probablement DUP et K hydro
        #cout_trait =  cout_traitement( Q_trait, Usines.loc[u, "Cout_moyen_m3"])# devrait marcher mais ne marche pas !
        
		var_output = {
            'index_mois':t,
			'TTP': u,
			'Months': Months[t-1]  ,
            'COMCOM': Usines.Nom_COMCOM[u],
            'URD': Usines.ID_URD[u],
			'Traite': Q_trait ,
			'Cout unitaire': Usines.Cout_moyen_m3[u] , # FIXME : ce ne sera plus un coût unitaire. On recalculera plutôt le cout moyen par m3 à partir du Cout total prélèvement.
			'Cout traitement': Q_trait*Usines.Cout_moyen_m3[u] , # FIXME : remplacer par le bon calcul du cout
			'Capacité' : K_ttp ,
			'Tx saturation K' : 100*Q_trait / K_ttp,
            'X' : Usines.X[u],
            'Y' : Usines.Y[u]
		}
		outputTTP.append(var_output)    
       

outputTTP_df = pd.DataFrame.from_records(outputTTP).sort_values(['TTP','index_mois'])
outputTTP_df
outputTTP_df.to_csv(name_Sorties+'TTP'+'.csv' )

### Writing Node flux (to easily verify that IN = OUT)
outputNodes = []
for u in List_noeud :
	for t in time:  
		Q_In = sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if j == u])
		Q_Out = sum([model.Q[((i,j),t)].value for (i,j) in Routes_reel if i == u])
		var_output = {
            'index_mois':t,
			'Noeud': u,
			'Months': Months[t-1] ,
			'Q_In' : Q_In ,
			'Q_Out' : Q_Out,
            "Error" : Q_Out-Q_In
		}
		outputNodes.append(var_output)
outputNodes_df = pd.DataFrame.from_records(outputNodes).sort_values(['Noeud','Months'])
outputNodes_df
outputNodes_df.to_csv(name_Sorties+'_'+'Noeuds'+'.csv' )

### Wrting MAjor Dam Results (Brennilis)
outputSM = []
for t in time: 
      Vol_preleve_Total = model.Q[(('29000151', 'T7001'),t)].value +  model.Q[(('29000152', 'T7002'),t)].value
      Vol_reservoir =  model.reservoir_SM[t].value
      Vol_reservoir_deb=model.reservoir_SM_01[t].value
      #Lacher_SM = max(0, (model.Q[(('29000151', 'T7001'),t)].value+model.Q[(('29000152', 'T7002'),t)].value - Vol_prelevable[t-1])/perte_lacher)
      Lacher_SM = model.lacher[t].value
      vol_preleve_Aulne=Vol_preleve_Total-0.6*Lacher_SM
    
      var_output = {
        'index_mois':t,
		'Months': Months[t-1] ,
        'Recharge': Recharge[t-1],
        'vol_reservoir_debut': Vol_reservoir_deb,
		'Vol_Reservoir_end' : Vol_reservoir ,
        'Vol_Prelevable_Aulne' : Vol_prelevable[t-1],
        'Lacher_Milieu' : Vol_soutien[t-1],
        'Lacher_AEP' : Lacher_SM,
        'Vol_preleve_Aulne': vol_preleve_Aulne,
        'Vol_prélevé_Total': Vol_preleve_Total,
       
	  }
      outputSM.append(var_output)
outputSM_df = pd.DataFrame.from_records(outputSM).sort_values(['index_mois'])
outputSM_df
outputSM_df.to_csv(name_Sorties+'_'+'SMA'+'.csv' )

### Wrting Secondary Dam Results (Kerrous)
outputKerrous = []
for t in time: 
      Vol_preleve_Total = model.Q[(('29000327', 'T6141'),t)].value
      Vol_reservoir_Kerrous =  model.reservoir_Kerrous[t].value
      Vol_reservoir_Kerrous_deb= model.reservoir_Kerrous_01[t].value
      #Lacher_SM = max(0, (model.Q[(('29000151', 'T7001'),t)].value+model.Q[(('29000152', 'T7002'),t)].value - Vol_prelevable[t-1])/perte_lacher)
      Lacher_Kerrous = model.lacher_Kerrous[t].value
      vol_preleve_Steir=Vol_preleve_Total-Lacher_Kerrous
    
      var_output = {
        'index_mois':t,
		'Months': Months[t-1] ,
        'vol_reservoir_debut': Vol_reservoir_Kerrous_deb,
		'Vol_Reservoir_end' :  Vol_reservoir_Kerrous ,
        'Vol_Prelevable_Steir' : Vol_prelevable_Kerrous[t-1],
        'Lacher_Milieu' : Vol_soutien_Kerrous[t-1],
        'Lacher_AEP' : Lacher_Kerrous,
        'Vol_preleve_Steir': vol_preleve_Steir,
        'Vol_prélevé_Total': Vol_preleve_Total,
       
	  }
      outputKerrous.append(var_output)
outputKerrous_df = pd.DataFrame.from_records(outputKerrous).sort_values(['index_mois'])
outputKerrous_df
outputKerrous_df.to_csv(name_Sorties+'_'+'Kerrous'+'.csv' )
