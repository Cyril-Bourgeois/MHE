# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:10:42 2021

@author: bourgeoisc,neverren
"""
## Function for withdrawal cost
def cout_prelevement(flow, depth, water_type):
  flow_s= flow/duration # Convert monthly flow from m3/month to m3/sec
    S=  flow_s/((2/3)*K_n * 2* H_n )# Porchet Formula
    w_pompe = rho*g*flow_s*(depth+water_type* S)
    cout_prel=(w_pompe/rdt_pompe)*duration*price_elec/conversion_kwh_kgm3s2
    return cout_prel 

## Function for transport cost
def cout_transport(flux,D,L):
    flow_s= flow/duration
    deltaH=k*(1/(1+3*sqrt(D/2)))*(flow_s*flow_s)/(D*D)
    w_trans=rho*g*flow_s*deltaH
    output=w_trans*L*duration*price_elec/conversion_kwh_kgm3s2
    return output

## Function for linear  failure cost (not used)
def cout_defaillance(flux):   
    output= 9999*flux
    return output

### Function for quadratic failure cost
def cout_defaillance2(flux,demande):   
    output= flux* p_eau + flux*flux*(p_max_eau-p_eau)/(2*demande+1)
    return output

###Function for treatment cost
def cout_traitement(flux,cout):
    output= flux*cout
    return output

###Function for transaction cost
def cout_transaction(flux,param):
    output = flux*param
    return output
