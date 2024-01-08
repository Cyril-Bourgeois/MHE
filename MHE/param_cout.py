# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:53:13 2021

@author: bourgeoisc, neverren
"""
###############################################################################
######################## Paramètre de couts ###################################
###############################################################################


#### Passages des mois en jours
duree= 3600*24*365/12
#### Passage des jours en mois
duree_jours_mois=365/12
#### Prix electricité (€/kwh)
prix_elec= 0.08
#### conversion kiloWattheure en unite fondamentale kg.m3/s^3 (1W= 1 kg.m3/s^3 et 1Wh= 1000*3600W)
conversion_kwh_kgm3s2= 1000*3600
#### Masse volumique de l'eau (kg/m3)
rho=1000
#### Constante de gravité (m/s2)
g= 9.81
#### rendement de la pompoe (sans unité)
rdt_pompe=0.8
#### Perméabilité de la nappe (m/s)
K_n= 7e-5
#### Epaisseur de la nappe (m)
H_n=60
####  Constante pour la nature de la canalisation
k = 0.003185

### prix de l'eau pour la défaillance
p_eau=3
p_max_eau=100

#### Perte entre le lacher Saint-Michel et les Ouvrages
perte_lacher=0.6
perte_lacher_Kerrous=1

#### Couttransaction USines SMA
param_cout_SMA=0.2

#### cout pr prio Aulne Vs SM
cout_lacher=0.1