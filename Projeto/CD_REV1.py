# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 11:23:12 2023

@author: pedro.solha / gabriel.franca
"""
import pandas as pd
import math
import numpy as np

def area_secao(tipo_secao, dimensoes_secao):
    if tipo_secao == "circular":
        altura = dimensoes_secao["diametro"]
        raio = altura / 2
        area = math.pi * raio**2
    elif tipo_secao == "trapezoidal":
        z = dimensoes_secao["inclinacao_talude"]
        base_menor = dimensoes_secao["base_menor"] 
        altura = dimensoes_secao["altura"]
        base_maior = z * altura * 2 + base_menor
        area = (base_maior + base_menor) / 2 * altura
    elif tipo_secao == "retangular":
        base = dimensoes_secao["base"]
        altura = dimensoes_secao["altura"]
        area = base * altura
    else:
        raise ValueError("Tipo de seção não suportado.")
    
    return area

def vazao_emboque(area,altura):
    q_emboque = 2/3 * 0.9 * area * math.sqrt(2/3  * 9.81 * altura)
    return q_emboque

def vazao_pequeno_orificio(area,H2, H1):
    q = 0.61 * area * math.sqrt(2  * 9.81 * (H1-H2))
    return q

def vazao_grande_orificio(area,H2, H1):
    q = 2/3 * 0.61 * area * math.sqrt(2 * 9.81 )*((H1**1.5 - (H2)**1.5)/(H1 - H2))
    return q

def vazao_soleira(tipo, Comprimento, altura, Cd, N_pilar, Kp, Ka, z):
    if tipo == "trapezoidal":
        L_efetiva = (Comprimento-2*(N_pilar*Kp+Ka)*(altura))
        q = Cd*L_efetiva*altura**(3/2) + Cd *  z * altura ** (5/2) 
    
    elif tipo == "side_flow":
        L_efetiva = (Comprimento-2*(N_pilar*Kp+Ka)*(altura))
        q = Cd * L_efetiva ** 0.83 * altura ** (5/3)
    
    elif tipo == "retangular":
        L_efetiva = (Comprimento-2*(N_pilar*Kp+Ka)*(altura))
        q = Cd * L_efetiva * altura ** (3/2)  
    
    elif tipo == "triangular":
        #L_efetiva = ((Comprimento+2*altura*z)-2*(N_pilar*Kp+Ka)*(altura))
        q = Cd * z * altura ** (5/2) 
    return q

### Calculando a área para cada intervalo determinado
def area_discretizada(tipo_secao, Delta_H, dimensoes_secao):
    area = np.zeros_like(Delta_H)
    if tipo_secao == "circular":
        raio = dimensoes_secao["diametro"]  / 2
        for i, altura in enumerate(Delta_H):
            altura = Delta_H[i]
            angulo = 2 * math.acos(1 - altura / raio)
            area[i] = 1/2 * raio**2 * (angulo-math.sin(angulo))
    elif tipo_secao == "trapezoidal":
        z = dimensoes_secao["inclinacao_talude"]
        base_menor = dimensoes_secao["base_menor"] 
        for i, altura in enumerate(Delta_H):
            base_maior = z * altura * 2 + base_menor
            area[i] = (base_maior + base_menor) / 2 * altura
    elif tipo_secao == "retangular":
        base = dimensoes_secao["base"]
        for i, altura in enumerate(Delta_H):
            area[i] = base * altura
    else:
        for i, altura in enumerate(Delta_H):
            area[i] = 0
    return area

def calcular_vazao(Areas, Delta_Cota, dimensoes_secao, tipo_secao, tipo):
    vazoes = np.zeros_like(Delta_Cota)
    max_area_index = len(Areas) - 1
        
        
    for i, delta_cota in enumerate(Delta_Cota):
        delta_h = delta_cota - Delta_Cota[0]
        
        if i <= max_area_index:
            area = Areas[i]
        else:
            area = Areas[max_area_index]
            
        if tipo_secao == "soleira":
            vazoes [i] = vazao_soleira(tipo, dimensoes_secao["Comprimento"], delta_h, dimensoes_secao["Cd"], dimensoes_secao["N_pilar"], dimensoes_secao["Kp"], dimensoes_secao["Ka"],dimensoes_secao["z"])
        else:
                if delta_h <= dimensoes_secao["H2"]:
                    vazoes[i] = vazao_emboque(area, delta_h)
                else:
                    if dimensoes_secao["H2"] > (Delta_Cota[i] - Delta_Cota[1]) / 3:
                        vazoes[i] = vazao_grande_orificio(area, delta_h-dimensoes_secao["H2"], delta_h)
                    else:
                        vazoes[i] = vazao_pequeno_orificio(area, dimensoes_secao["H2"], delta_h)
                    
                if tipo_secao == "circular":
                    fator_correcao = 1 - 0.05 * (dimensoes_secao["linhas"]-1)
                    vazoes[i] =  dimensoes_secao["linhas"]*vazoes[i]* fator_correcao
                else:
                    vazoes = vazoes
    return vazoes

def calcula_curva_descarga(tipo_secao, dimensoes_secao, El_Soleira, El_Max, Discretizacao, tipo=None):
    ### Definindo alturas a ser utilizadas para calculo da CD
    Delta_Cota = np.arange(El_Soleira, El_Max + Discretizacao, Discretizacao)
    Delta_H = np.arange(0,dimensoes_secao['H2']+Discretizacao, Discretizacao)

    # Garantindo que o maior valor das listas seja El_Max e diferenca entre El_Max e El_soleira
    Delta_Cota[-1] = El_Max
    Delta_H[-1] = dimensoes_secao['H2']

    Areas = area_discretizada(tipo_secao, Delta_H, dimensoes_secao)
    #print(Areas)

    Vazao_final = calcular_vazao(Areas, Delta_Cota, dimensoes_secao, tipo_secao, tipo)

    CD = pd.DataFrame({"Cota (m)":Delta_Cota, "Vazão (m³/s)":Vazao_final})

    print("A curva de descarga é:")
    print(CD)
    
    return CD
