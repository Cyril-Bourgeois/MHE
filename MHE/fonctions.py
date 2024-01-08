# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 17:10:42 2021

@author: bourgeoisc,neverren
"""

def cout_prelevement(flux,profondeur,type_eau):
    debit= flux/duree # Conversio flux mensuel de m3/mois à m3/sec
    S= debit/((2/3)*K_n * 2* H_n )# Formule de Porchet
    w_pompe = rho*g*debit*(profondeur+type_eau* S)
    cout_prel=(w_pompe/rdt_pompe)*duree*prix_elec/conversion_kwh_kgm3s2
    return cout_prel 


def cout_transport(flux,D,L):
    debit=flux/duree
    deltaH=k*(1/(1+3*sqrt(D/2)))*(debit*debit)/(D*D)
    w_trans=rho*g*debit*deltaH
    output=w_trans*L*duree*prix_elec/conversion_kwh_kgm3s2
    return output


def cout_defaillance(flux):   
    output= 9999*flux
    return output

### mettre 100 (p_eau_max en paream!)
def cout_defaillance2(flux,demande):   
    output= flux* p_eau + flux*flux*(p_max_eau-p_eau)/(2*demande+1)
    return output

def cout_traitement(flux,cout):
    output= flux*cout
    return output


def cout_transaction(flux,param):
    output = flux*param
    return output