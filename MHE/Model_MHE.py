# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:29:36 2021

@author: bourgeoisc, neverren
"""

###############################################################################
###########                    Model                 ##########################
###############################################################################


###############################################################################
###########         Water Flux          #########################
###############################################################################


####### Route creation - NB: a route = a section between 2 nodes
Routes_reel = [(Liens.loc[i, "ID_depart"], Liens.loc[i, "ID_arrivee"]) for i in range(len(Liens))] # Real water road
Routes_def= [(Liens_def.loc[i, "ID_depart"], Liens_def.loc[i, "ID_arrivee"]) for i in range(len(Liens_def))] # Failure road
Routes = Routes_reel + Routes_def
## Subset of roads leading from water extraction points
liens_ouvrages=Liens.loc[Liens["Type_depart"] == 'OUV']
liens_ouvrages.reset_index(inplace = True,drop=True)
Routes_prel= [(liens_ouvrages.loc[j, "ID_depart"], liens_ouvrages.loc[j, "ID_arrivee"]) for j in range(len(liens_ouvrages))]
## Subset of routes from SMA sampling points
liens_ouvrages_SMA=Liens.loc[(Liens["Type_depart"] == 'OUV') & (Liens["ID_CC_depart"] == '7' )]
liens_ouvrages_SMA.reset_index(inplace = True,drop=True)
Routes_SMA= [(liens_ouvrages_SMA.loc[j, "ID_depart"], liens_ouvrages_SMA.loc[j, "ID_arrivee"]) for j in range(len(liens_ouvrages_SMA))]

liens_ouvrages_Kerrous=Liens.loc[(Liens["Type_depart"] == 'OUV') & (Liens["ID_arrivee_txt"] == 'T6141' )]
liens_ouvrages_Kerrous.reset_index(inplace = True,drop=True)
## Subset of routes from Kerrous (secondary dam)
Routes_Kerrous= [(liens_ouvrages_Kerrous.loc[j, "ID_depart"], liens_ouvrages_Kerrous.loc[j, "ID_arrivee"])for j in range(len(liens_ouvrages_Kerrous))]

## SSubset of roads leading from treatment plants
liens_usines=Liens.loc[Liens["Type_depart"] == 'TTP']
liens_usines.reset_index(inplace = True,drop=True)
Routes_usines= [(liens_usines.loc[j, "ID_depart"], liens_usines.loc[j, "ID_arrivee"]) for j in range(len(liens_usines))]

##Subset of roads leading from SMA treatment plants
liens_usines_SMA=liens_usines.loc[ liens_usines["ID_CC_depart"] == '7' ]
liens_usines_SMA.reset_index(inplace = True,drop=True)
Routes_usines_SMA= [(liens_usines.loc[j, "ID_depart"], liens_usines.loc[j, "ID_arrivee"]) for j in range(len(liens_usines))]

Liens=Liens.set_index(['ID_depart',"ID_arrivee"]) 
Liens_def=Liens_def.set_index(['ID_depart',"ID_arrivee"]) 

###############################################################################
###########      Model definition                  ############################
###############################################################################

####### Name and class of model 
 
model=ConcreteModel(name="Global Problem")
#######
time=range(1,13,1)    
model.months = Set(initialize=(i for i in time),
doc="Index of variables")
####### Decision variables
model.Q =Var(Routes, time, within=NonNegativeReals, initialize=0) #Water flux
model.lacher= Var(model.months,doc="Optimized stocks") #Use of Brennilis Dam
model.lacher_Kerrous= Var(model.months,domain=NonNegativeReals, doc="Optimized stocks") #Use of Kerrous Dam

# Declaration of stock variable ( Brenilis)
model.reservoir_SM= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")
model.reservoir_SM_01= Var(model.months,
domain=NonNegativeReals,
doc="Optimized stocks")

# Declaration of stock variable (Kerrous)    
model.reservoir_Kerrous= Var(model.months,domain=NonNegativeReals,doc="Optimized stocks")
model.reservoir_Kerrous_01= Var(model.months,domain=NonNegativeReals,doc="Optimized stocks")
                                               
####### Objective function
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
            
            
                      
###Pipe capacity stress (when stakeholder has supported restrictive information)
## Crozon-Intermedite Node
model.C_Nodes_Crozon=ConstraintList()   
for t in time:
    model.C_Nodes_Crozon.add( 24*Coef_Crozon_EO*duree_jours_mois >= 
     model.Q[(('R1021', '101'),t)]  )
      
##  Kerlaeron --> Landulec
model.C_Nodes_CCHPB1=ConstraintList()   
for t in time:
    model.C_Nodes_CCHPB1.add( 950*duree_jours_mois >= 
     model.Q[(('R3031', 'R3021'),t)]  )
 
##  Kerandouaré -->Landulec
model.C_Nodes_CCHPB2=ConstraintList()   
for t in time:
    model.C_Nodes.add( 24*Coef_Kerandouare_landulec*duree_jours_mois >= 
     model.Q[(('R3031', 'R3021'),t)]  )
        
### Plant capacity constraints 
model.C_TTP=ConstraintList()
for t in time:   
    for u in Usines.index:
        model.C_TTP.add( (Usines.K[u]*duree_jours_mois  >=
              sum([model.Q[((i,j),t)]   for (i,j) in Routes_prel if j == u])))
        
### Application crisis scenerio 
model.C_TTP_SMA=ConstraintList()
for t in time:   
    for u in Usines_SMA.index:
        model.C_TTP_SMA.add( (Usines.K[u]*duree_jours_mois* df_crise.crise[t]  >=
              sum([model.Q[((i,j),t)]   for (i,j) in Routes_prel if j == u])))        
        
### Capacity constraints Resources ( Capacity /Administrative authorization (m3] *d hydrogeological capacity (%) )
model.C_OUV=ConstraintList()
for t in time:   
    for u in Ouvrages_noSMA.index:
        model.C_OUV.add( Ouvrages.K_aut_jr[u]*duree_jours_mois* Ouvrages.loc[u,  scenario_ouv_hydro[t-1]]
       >= sum([model.Q[((i,j),t)] for (i,j) in Routes_prel if i == u]) )

###Constraint on Withdrawal linked to a river and a dam
###The model cannot take more than can be taken from the river + what is available in the dam modulo the release.
### Capacity constraints SMA Resources 
model.C_OUV_SMA1=ConstraintList()
for t in time:   
    for u in Ouvrages_SMA.index:
           model.C_OUV_SMA1.add( Ouvrages.K_aut_jr[u]*duree_jours_mois                    
                            >= sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA if i == u]) )
           model.C_OUV_SMA1.add( sum([model.Q[((i,j),t)] for (i,j) in Routes_SMA ])                    
                           <= Vol_prelevable[t-1]+perte_lacher*model.lacher[t] )
 
### Capacity constraints Kerrous Resources
model.C_OUV_Kerrous1=ConstraintList()
for t in time:   
    for u in Ouvrages_Kerrous.index:
            model.C_OUV_Kerrous1.add( Ouvrages.K_aut_jr[u]*duree_jours_mois                    
                            >= sum([model.Q[((i,j),t)] for (i,j) in Routes_Kerrous if i == u]) )
            model.C_OUV_Kerrous1.add( sum([model.Q[((i,j),t)] for (i,j) in Routes_Kerrous ])                    
                            <= Vol_prelevable_Kerrous[t-1]+perte_lacher_Kerrous*model.lacher_Kerrous[t] )
                            
### Contrainte satisfaction Demande    
model.C_Dmd=ConstraintList()
for t in time:   
    for u in Demande.index:
        model.C_Dmd.add(Demande.loc[u, 'VCA2019']* Demande.loc[u, Months[t-1]]/100  <= sum([model.Q[((i,j),t)] * (Demande.loc[u ,'Rendement']/100)   for (i,j) in Routes_reel if j == u]) -
                                                                                       sum([model.Q[((i,j),t)]   for (i,j) in Routes_reel if i == u])+
                                                                                       sum([model.Q[((i,j),t)]   for (i,j) in Routes_def if j == u])) 
  
##  Contrainte importatinn demande   
model.C_import=ConstraintList() 
for u in import_URD.index:
    model.C_Dmd.add(import_URD.loc[u, "Export_2019"] >= # changer export en import 
             sum([model.Q[((i,j),t)]  for (i,j) in Routes if i == u  for t in time])) 
    
##################################################################################################################################
############# Brenillis ( MAjor dam) ############################################################################################  
##################################################################################################################################  
### Stock constraints
### 1. stock modeling 
### 1a. Before June, no possibility of taking from the Saint-Michel reserve --->Stock at Zero
### 1b. June, the stock value is given by the climate data scenario. We take the value on the last day of June (this allows us to integrate the June refill, which is available for the month of June).
### 1c. From June onwards, Stock evolution is equal to previous stock + current month's recharge - current month's release.
### 1d. The release is equal to the difference between what has been withdrawn by the (model - what can be withdrawn from the river)/ loss coef.

model.constraint_Saint_Michel= ConstraintList( )
model.constraint_Saint_Michel2= ConstraintList( )
model.constraint_lacher1= ConstraintList( )

#### Constraint on the release of
### Release before June = 0
### Release in June and after lower than actual available stock

for t in time:
    if t<6 : # January-May constraint
        model.constraint_lacher1.add(
        model.lacher[t] == 0
           )
    else: # June constraint
        # Constraints June. Note that Recharge Month =[t-1] and not t. ( because the index of Recharge and Vol_prélevable corresponds to the python index and not to the month number).
        model.constraint_lacher1.add(
        model.lacher[t] >= 0.00)
        
        model.constraint_lacher1.add(
             model.lacher[t]<=
             model.reservoir_SM[t-1 ] + Recharge[t-1]-Vol_soutien[t-1]
             )    
#### Damevolution equation
### Exogenous stock before June
### Stock in t = stock t-1 + Recharge in T(desynchro pyhton)-Support in T - AEP releases

for t in model.months:
    if t<=5 : # January-May constraint
        model.constraint_Saint_Michel.add(         
            model.reservoir_SM[t] ==Initial_Stock[t-1]+Stock_carriere
            )
               
    else : # >June constraint
            model.constraint_Saint_Michel.add(       
        model.reservoir_SM[t] ==  model.reservoir_SM[t-1] + Recharge[t-1]-Vol_soutien[t-1]- model.lacher[t]
            )
               
    
#### Not essential
### Allows you to know the volume at the beginning of each month       
            
for t in time:
    if t==1 : # January constraint
        model.constraint_Saint_Michel2.add(
            model.reservoir_SM_01[t]==0 )
    else :
        model.constraint_Saint_Michel2.add(    
            model.reservoir_SM_01[t]==model.reservoir_SM[t-1]
    )


##################################################################################################################################
############# Kerrous Dam (Secondary Dam)   ######################################################################################  
##################################################################################################################################    

model.constraint_Kerrous= ConstraintList( )
model.constraint_lacher_Kerrous= ConstraintList( )
model.constraint_lacher_Kerrous2= ConstraintList( )


#### Kerrous reservoir release constraint
### Release before June O
### Release in June and after lower than actual available stock             

for t in time:
    if t<6 : # January-May constraint
        model.constraint_lacher_Kerrous.add(
        model.lacher_Kerrous[t] == 0
           )
    else: # >June constraint
        model.constraint_lacher_Kerrous.add(
        model.lacher_Kerrous[t] >= 0.00)
        
        model.constraint_lacher_Kerrous.add(
             model.lacher_Kerrous[t]<=
             model.reservoir_Kerrous[t-1 ] -Vol_soutien_Kerrous[t-1]
             )    
for t in model.months:
    if t<=5 : # January-May constraint
        model.constraint_Kerrous.add(         
            model.reservoir_Kerrous[t] ==Initial_Stock_Kerrous
            )
   
             
    else : # June constraint
        model.constraint_Kerrous.add(       
        model.reservoir_Kerrous[t] == model.reservoir_Kerrous[t-1] -Vol_soutien_Kerrous[t-1]- model.lacher_Kerrous[t]
            )
               
    
#### Not essential
### Allows you to know the volume at the beginning of each month      
                  
for t in time:
    if t==1 : # January constraint
        model.constraint_lacher_Kerrous2.add(
            model.reservoir_Kerrous_01[t]==0 )
    else :
        model.constraint_lacher_Kerrous2.add(    
            model.reservoir_Kerrous_01[t]==model.reservoir_Kerrous[t-1]
    ) 
