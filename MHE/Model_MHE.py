# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:29:36 2021

@author: bourgeoisc, neverren
"""

###############################################################################
###########                    Model                 ##########################
###############################################################################


###############################################################################
###########         Définition des routes             #########################
###############################################################################


####### Création des routes - NB : une route = un tronçon entre 2 noeuds
Routes_reel = [(Liens.loc[i, "ID_depart"], Liens.loc[i, "ID_arrivee"]) for i in range(len(Liens))]
Routes_def= [(Liens_def.loc[i, "ID_depart"], Liens_def.loc[i, "ID_arrivee"]) for i in range(len(Liens_def))]
Routes = Routes_reel + Routes_def
## Subset routes prelevment
liens_ouvrages=Liens.loc[Liens["Type_depart"] == 'OUV']
liens_ouvrages.reset_index(inplace = True,drop=True)
Routes_prel= [(liens_ouvrages.loc[j, "ID_depart"], liens_ouvrages.loc[j, "ID_arrivee"]) for j in range(len(liens_ouvrages))]
## Subset routes SMA
liens_ouvrages_SMA=Liens.loc[(Liens["Type_depart"] == 'OUV') & (Liens["ID_CC_depart"] == '7' )]
liens_ouvrages_SMA.reset_index(inplace = True,drop=True)
Routes_SMA= [(liens_ouvrages_SMA.loc[j, "ID_depart"], liens_ouvrages_SMA.loc[j, "ID_arrivee"]) for j in range(len(liens_ouvrages_SMA))]

liens_ouvrages_Kerrous=Liens.loc[(Liens["Type_depart"] == 'OUV') & (Liens["ID_arrivee_txt"] == 'T6141' )]
liens_ouvrages_Kerrous.reset_index(inplace = True,drop=True)

Routes_Kerrous= [(liens_ouvrages_Kerrous.loc[j, "ID_depart"], liens_ouvrages_Kerrous.loc[j, "ID_arrivee"])for j in range(len(liens_ouvrages_Kerrous))]

## Subset routes usines
liens_usines=Liens.loc[Liens["Type_depart"] == 'TTP']
liens_usines.reset_index(inplace = True,drop=True)
Routes_usines= [(liens_usines.loc[j, "ID_depart"], liens_usines.loc[j, "ID_arrivee"]) for j in range(len(liens_usines))]

liens_usines_SMA=liens_usines.loc[ liens_usines["ID_CC_depart"] == '7' ]
liens_usines_SMA.reset_index(inplace = True,drop=True)
Routes_usines_SMA= [(liens_usines.loc[j, "ID_depart"], liens_usines.loc[j, "ID_arrivee"]) for j in range(len(liens_usines))]


Liens=Liens.set_index(['ID_depart',"ID_arrivee"]) 
Liens_def=Liens_def.set_index(['ID_depart',"ID_arrivee"]) 

###############################################################################
###########      Definition du   Model             ############################
###############################################################################

####### Name and class of model 
 
model=ConcreteModel(name="Global Problem")

####### Decision variables
model.Q =Var(Routes, time, within=NonNegativeReals, initialize=0)
model.months = Set(initialize=(i for i in time),
doc="Index of variables")

model.lacher= Var(model.months,
doc="Optimized stocks")                                     
# Déclaration de la variable du stock de la réservoir SM
model.reservoir_SM= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")
model.reservoir_SM_01= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")


# Déclaration de la variable du stock de la réservoir Kerrous
model.lacher_Kerrous= Var(model.months,
domain=NonNegativeReals,                          
doc="Optimized stocks")     
model.reservoir_Kerrous= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")
model.reservoir_Kerrous_01= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")
                          
time=range(1,13,1)                             
####### Objective function
# FIXME : introduire les couts de transactions
# FIXME : déterminer comment traiter le coût de l'eau du SMA : mêmes fonctions de coût que les autres ressources, ou prix d'achat.
model.obj= Objective(
        expr= sum([ cout_transport( model.Q[((i1,j1),t)],  Liens.Diametre[(i1,j1)],  1000*Liens.distance[(i1,j1)])  for (i1,j1) in Routes_reel for t in time])+ 
              sum([ cout_prelevement( model.Q[((i2,j2),t)],  Ouvrages.loc[i2,"Prof"],Ouvrages.loc[i2,"Type_eau"])  for (i2,j2) in Routes_prel for t in time])+
              sum([ cout_traitement( model.Q[((i3,j3),t)], Usines.loc[i3, "Cout_moyen_m3"])  for (i3,j3) in Routes_usines for t in time])+
              sum( [ cout_transaction( model.Q[((i5,j5),t)], param_cout_SMA)  for (i5,j5) in Routes_usines_SMA for t in time] )+
              #sum([ cout_defaillance( model.Q[((i4,j4),t)])  for (i4,j4) in Routes_def for t in time]) +
              sum([ cout_defaillance2( model.Q[((i4,j4),t)],Liens_def.loc[((i4,j4),Months[t-1])]*Liens_def.VCA2019[(i4,j4)]/100)  for (i4,j4) in Routes_def for t in time])+
              sum([cout_lacher*model.lacher[t] for t in time])+
              sum([cout_lacher*model.lacher_Kerrous[t] for t in time])
        ,sense=minimize)


 
####### Constraints 

### C1= Flow conservation constraint - this ensures the amount going into each node is at least equal to the amount leaving
model.C_Nodes=ConstraintList()   
for t in time:
    for n in List_noeud:
            model.C_Nodes.add( sum([model.Q[((i,j),t)] for (i,j) in Routes if j == n]) >= 
                              sum([model.Q[((i,j),t)] for (i,j) in Routes if i == n]) )
            
            
            
            
### Contrainte de Conduite :"mode tout caca pas beau"model.C_Nodes=ConstraintList()
## Conduite Crozon entre le Réservoir de la Montagne et le Réservoir de Crozon
#135000
model.C_Nodes_Crozon=ConstraintList()   
for t in time:
    model.C_Nodes_Crozon.add( 24*Coef_Crozon_EO*duree_jours_mois >= 
     model.Q[(('R1021', '101'),t)]  )
      
## Conduite CCHPB 1 entre Kerlaeron et Landulec
model.C_Nodes_CCHPB1=ConstraintList()   
for t in time:
    model.C_Nodes_CCHPB1.add( 950*duree_jours_mois >= 
     model.Q[(('R3031', 'R3021'),t)]  )
## Conduite CCHPB 2 entre Kerandouaré et Landulec
model.C_Nodes_CCHPB2=ConstraintList()   
for t in time:
    model.C_Nodes.add( 24*Coef_Kerandouare_landulec*duree_jours_mois >= 
     model.Q[(('R3031', 'R3021'),t)]  )
      

    
   
### Contrainte Capacité usine 
model.C_TTP=ConstraintList()
for t in time:   
    for u in Usines.index:
        model.C_TTP.add( (Usines.K[u]*duree_jours_mois  >=
              sum([model.Q[((i,j),t)]   for (i,j) in Routes_prel if j == u])))
        
### Application crise 
model.C_TTP_SMA=ConstraintList()
for t in time:   
    for u in Usines_SMA.index:
        model.C_TTP_SMA.add( (Usines.K[u]*duree_jours_mois* df_crise.crise[t]  >=
              sum([model.Q[((i,j),t)]   for (i,j) in Routes_prel if j == u])))        
        
### Contraite capacités Ressources (FIXME : DUP + installation + hydro)
### Rappel K_model=min(K_aut_jr, K_autres)
model.C_OUV=ConstraintList()
for t in time:   
    for u in Ouvrages_noSMA.index:
        #model.C_OUV.add( Ouvrages.loc[u, Months[t-1]]  >=## Old crozon test
        #model.C_OUV.add( Ouvrages.K_aut_jr[u]*365/12  ## Old w/o contrainte hydro
        #model.C_OUV.add( 1>= sum([model.Q[((i,j),t)] for (i,j) in Routes if i == u]) )## verif fonctionnement defaillance
        model.C_OUV.add( Ouvrages.K_aut_jr[u]*duree_jours_mois* Ouvrages.loc[u,  scenario_ouv_hydro[t-1]]
       >= sum([model.Q[((i,j),t)] for (i,j) in Routes_prel if i == u]) )



### contrainte Prélevment ouvrage SMA DUP
model.C_OUV_SMA1=ConstraintList()
for t in time:   
    for u in Ouvrages_SMA.index:
           model.C_OUV_SMA1.add( Ouvrages.K_aut_jr[u]*duree_jours_mois                    
                            >= sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA if i == u]) )
           model.C_OUV_SMA1.add( sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ])                    
                           <= Vol_prelevable[t-1]+perte_lacher*model.lacher[t] )
 

### contrainte Prélevment ouvrage Kerrous
model.C_OUV_Kerrous1=ConstraintList()
for t in time:   
    for u in Ouvrages_Kerrous.index:
            model.C_OUV_Kerrous1.add( Ouvrages.K_aut_jr[u]*duree_jours_mois                    
                            >= sum([model.Q[((i,j),t)] for (i,j) in Routes_Kerrous if i == u]) )
            model.C_OUV_Kerrous1.add( sum([model.Q[((i,j),t)] for (i,j) in Routes_Kerrous ])                    
                            <= Vol_prelevable_Kerrous[t-1]+perte_lacher_Kerrous*model.lacher_Kerrous[t] )
                            
### contrainte Prélevment  SMA (Sur les ressources hydro pour l'enesemble des ressources)   
### Le modéle ne peut pas prélever plus que qui est prelevable dans l'aulne + Ce qui est disponible dans la réserve SM modulo le lacher
# model.C_OUV_SMA2=ConstraintList()
# for t in time:       
#           model.C_OUV_SMA2.add( sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ])                    
#                            <= Vol_prelevable[t-1]+perte_lacher*model.lacher[t] )


### Contrainte satisfaction Demande    
# FIXME : vérifier comment prendre en compte le rendement de façon appropriée (Cf. définition Rdt dans RPQS)
model.C_Dmd=ConstraintList()
for t in time:   
    for u in Demande.index:
        model.C_Dmd.add(Demande.loc[u, 'VCA2019']* Demande.loc[u, Months[t-1]]/100  <= sum([model.Q[((i,j),t)] * (Demande.loc[u ,'Rendement']/100)   for (i,j) in Routes_reel if j == u]) -
                                                                                       sum([model.Q[((i,j),t)]   for (i,j) in Routes_reel if i == u])+
                                                                                       sum([model.Q[((i,j),t)]   for (i,j) in Routes_def if j == u])) 
  
## Contrainte importatinn demande   
# FIXME : Rajouter les ventes URD
# FIXME : vérifier comment prendre en compte le rendement de façon appropriée (Cf. définition Rdt dans RPQS)
model.C_import=ConstraintList() 
for u in import_URD.index:
    model.C_Dmd.add(import_URD.loc[u, "Export_2019"] >= # changer export en import 
             sum([model.Q[((i,j),t)]  for (i,j) in Routes if i == u  for t in time])) 
    
##################################################################################################################################
############# Réservoir Saint-Michel  ############################################################################################  
##################################################################################################################################  
### Contrainte_Stock Saint-Michel    
### 1. Modélisation du stock saint michel
### 1a. Avant Juin, pas de possibilité de prendre dans la réserve Saint-michel --->Stock à Zéro
### 1b. Juin, La valeur du stock est donnée par les fichier d'AB (dépend du climat). On prend la valeur au Dernier jour de juin (permet dintégrer la recharge de juin qui est bien disponible pour le mois de juin)
### 1c. A partir de Juin, l'évolution du Stock est égal au stock précédent + la recharge du mois en cours - le lacher du mois en cours
### 1d. Le lacher est égal à la différence entre ce qui a été prélevé par le (modèle - ce qui est prélevable dans l'aulne)/ coef de perte



model.constraint_Saint_Michel= ConstraintList( )
model.constraint_Saint_Michel2= ConstraintList( )
model.constraint_lacher1= ConstraintList( )


#### Contrainte sur le lacher du reservoir Saint-Michel
###Lacher avant juin O
### Lacher en juin et apres inférieur au stock réeel disponible


for t in time:
    if t<6 : # January constraint
        model.constraint_lacher1.add(
        model.lacher[t] == 0
           )
    else: # June constraint
        # Constraints Juin. Attention, Recharge Mois =[t-1] et pas t. ( car l'index de Recharge et Vol_prélevable correspond à l'index python et pas au numéro du  mois)
        #model.constraint_lacher1.add(
        #model.lacher[t] == 0.001+0.5*(
        #     (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #   )
        # model.constraint_lacher1.add(
        # model.lacher[t] == 0.5*(
        #       (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #     )
        # model.constraint_lacher1.add(
        # model.lacher[t] <= 0.5*(
        #       (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #     )
        model.constraint_lacher1.add(
        model.lacher[t] >= 0.00)
        
        model.constraint_lacher1.add(
             model.lacher[t]<=
             model.reservoir_SM[t-1 ] + Recharge[t-1]-Vol_soutien[t-1]
             )    


#### Contrainte de Stock reservoir Saint-Michel
###  Stock exogène avant juin
### Stock en t = stock t-1 + Recharge en T(desynchro pyhton)-Soutien en T - les lachers AEP


for t in model.months:
    if t<=5 : # January constraint
        model.constraint_Saint_Michel.add(         
            model.reservoir_SM[t] ==Initial_Stock[t-1]+Stock_carriere
            )
   
             
    else : # June constraint
        # Constraints Juin. Attention, Recharge Mois =[t-1] et pas t. ( car l'index de Recharge et Vol_prélevable correspond à l'index python et pas au numéro du  mois)
        model.constraint_Saint_Michel.add(       
        model.reservoir_SM[t] ==  model.reservoir_SM[t-1] + Recharge[t-1]-Vol_soutien[t-1]- model.lacher[t]
            )
               
    
#### Non essentiel
###  Permet de connaitre le volume en debut de chaque  mois
    
            
for t in time:
    if t==1 : # January constraint
        model.constraint_Saint_Michel2.add(
            model.reservoir_SM_01[t]==0 )
    else :
        model.constraint_Saint_Michel2.add(    
            model.reservoir_SM_01[t]==model.reservoir_SM[t-1]
    )


##################################################################################################################################
############# Réservoir de Kerrous   ############################################################################################  
##################################################################################################################################    


model.constraint_Kerrous= ConstraintList( )
model.constraint_lacher_Kerrous= ConstraintList( )
model.constraint_lacher_Kerrous2= ConstraintList( )


#### Contrainte sur le lacher du reservoir de Kerrous
### Lacher avant juin O
### Lacher en juin et apres inférieur au stock réeel disponible


for t in time:
    if t<6 : # January constraint
        model.constraint_lacher_Kerrous.add(
        model.lacher_Kerrous[t] == 0
           )
    else: # June constraint
        # Constraints Juin. Attention, Recharge Mois =[t-1] et pas t. ( car l'index de Recharge et Vol_prélevable correspond à l'index python et pas au numéro du  mois)
        #model.constraint_lacher1.add(
        #model.lacher[t] == 0.001+0.5*(
        #     (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #   )
        # model.constraint_lacher1.add(
        # model.lacher[t] == 0.5*(
        #       (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #     )
        # model.constraint_lacher1.add(
        # model.lacher[t] <= 0.5*(
        #       (sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher +abs((sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ]) -Vol_prelevable[t-1] )/perte_lacher))
        #     )
        model.constraint_lacher_Kerrous.add(
        model.lacher_Kerrous[t] >= 0.00)
        
        model.constraint_lacher_Kerrous.add(
             model.lacher_Kerrous[t]<=
             model.reservoir_Kerrous[t-1 ] -Vol_soutien_Kerrous[t-1]
             )    
for t in model.months:
    if t<=5 : # January constraint
        model.constraint_Kerrous.add(         
            model.reservoir_Kerrous[t] ==Initial_Stock_Kerrous
            )
   
             
    else : # June constraint
        # Constraints Juin. Attention, Recharge Mois =[t-1] et pas t. ( car l'index de Recharge et Vol_prélevable correspond à l'index python et pas au numéro du  mois)
          model.constraint_Kerrous.add(       
        model.reservoir_Kerrous[t] == model.reservoir_Kerrous[t-1] -Vol_soutien_Kerrous[t-1]- model.lacher_Kerrous[t]
            )
               
    
#### Non essentiel
###  Permet de connaitre le volume en debut de chaque  mois
                
for t in time:
    if t==1 : # January constraint
        model.constraint_lacher_Kerrous2.add(
            model.reservoir_Kerrous_01[t]==0 )
    else :
        model.constraint_lacher_Kerrous2.add(    
            model.reservoir_Kerrous_01[t]==model.reservoir_Kerrous[t-1]
    ) 