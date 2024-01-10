# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:53:13 2021

@author: bourgeoisc, neverren
"""
###############################################################################
######################## Cost pararameters ###################################
###############################################################################
## PArameters for cost function (see function.py)

#### Month in days
duree= 3600*24*365/12
#### day in months
duree_jours_mois=365/12
#### electricity price (€/kwh)
prix_elec= 0.08
####  kiloWattheure  conversion in fundamental unit :kg.m3/s^3 (1W= 1 kg.m3/s^3 and 1Wh= 1000*3600W)
conversion_kwh_kgm3s2= 1000*3600
#### Water density (kg/m3)
rho=1000
#### Gravity constant (m/s2)
g= 9.81
#### pump efficiency (unitless)
rdt_pompe=0.8
#### permeability of the water table  (m/s)
K_n= 7e-5
#### thickness of water table (m)
H_n=60
####   Constant for pipe type
k = 0.003185

### water price for failure function
p_eau=3
p_max_eau=100

#### Loss between Dams and abstraction works
perte_lacher=0.6 #Loss for Brenillis (long canal between reservoir and withdrawal point)
perte_lacher_Kerrous=1 # Loss fos Kerrous (pump directly in Dams)

#### SMA Cost transaction
param_cout_SMA=0.2

#### opportunity cost(cost to prio river on Dams)
cout_lacher=0.1
