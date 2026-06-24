# -*- coding: utf-8 -*-
"""
Created on Sun May 24 14:17:55 2026

@author: Utente
"""
# SMART PARK OPTIMIAZTION - Brescia
# Optimization Methods in Business Analytics

 
import pyomo as pyo
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# 1. Data & Parameters

# SETS

# I: parking sites (existing and new candidates)
# (ID, name, latitude, longitude, capacity, annual cost, existing)

parking_data = {
    "I01": ("Camper Poliambulanza",       45.5215, 10.2368,   10,         0, True),
    "I02": ("Crystal Superficie",          45.5358, 10.2192,   50,         0, True),
    "I03": ("Apollonio",                   45.5292, 10.2182,  115,         0, True),
    "I04": ("Castellini",                  45.5248, 10.2292,  215,         0, True),
    "I05": ("Ospedale Nord (superficie)",  45.5568, 10.2315,  150,         0, True),
    "I06": ("Stadio Rigamonti",            45.5478, 10.2278,  496,         0, True),
    "I07": ("Poliambulanza",               45.5212, 10.2370,  350,         0, True),
    "I08": ("Prealpino",                   45.5718, 10.2048, 1005,         0, True),
    "I09": ("Autosilo Uno",                45.5372, 10.2168,  336,         0, True),
    "I10": ("S. Eufemia-Buffalora",        45.5252, 10.2648,  398,         0, True),
    "I11": ("Casazza",                     45.5592, 10.2118,  160,         0, True),
    "I12": ("Arnaldo Park",                45.5365, 10.2298,  300,         0, True),
    "I13": ("Crystal (autosilo)",          45.5358, 10.2192,  400,         0, True),
    "I14": ("Palagiustizia",               45.5398, 10.2118,  600,         0, True),
    "I15": ("Stazione",                    45.5328, 10.2128, 1000,         0, True),
    "I16": ("Benedetto Croce",             45.5382, 10.2238,   72,         0, True),
    "I17": ("San Domenico",                45.5412, 10.2208,   72,         0, True),
    "I18": ("Freccia Rossa",               45.5282, 10.2068, 2500,         0, True),
    "I19": ("Piazza Mercato",              45.5372, 10.2248,  190,         0, True),
    "I20": ("Randaccio",                   45.5448, 10.2130,  180,         0, True),
    "I21": ("Fossa Bagni",                 45.5398, 10.2208,  560,         0, True),
    "I22": ("D'Azeglio",                   45.5352, 10.2258,   35,         0, True),
    "I23": ("Ospedale Sud",                45.5532, 10.2378,  500,         0, True),
    "I24": ("Ospedale Nord (autosilo)",    45.5562, 10.2322, 1260,         0, True),
    "I25": ("Goito",                       45.5372, 10.2288,  215,         0, True),
    "I26": ("Piazza Vittoria",             45.5383, 10.2190,  520,         0, True),
    # ── New candidate sites─────────────────────────────────────────────────
    "I27": ("HUB Lamarmora Sud",           45.5198, 10.2252,  450, 225000, False),
    "I28": ("Parcheggio Sud Stazione",     45.5292, 10.2078,  350, 175000, False),
    "I29": ("Ospedale Nord-Ovest",         45.5582, 10.2282,  300, 60000, False),
    "I30": ("Parcheggio ex Pietra",        45.5422, 10.2058,  450, 225000, False),
    "I31": ("Mega Park&Ride Sud",          45.5052, 10.2398,  950, 237500, False),
}

I = list(parking_data.keys())           
I_exist = [i for i in I if parking_data[i][5]]  
I_new   = [i for i in I if not parking_data[i][5]] 



# J: demand nodes
# (ID, name, latitude, longitude)

node_data = {
    "J01": ("Piazza della Vittoria",        45.5381, 10.2192),
    "J02": ("Piazza Paolo VI / Duomo",      45.5387, 10.2213),
    "J03": ("Teatro Grande",                45.5370, 10.2175),
    "J04": ("Palazzo di Giustizia",         45.5395, 10.2118),
    "J05": ("Santa Giulia / Capitolium",    45.5392, 10.2291),
    "J06": ("Castello di Brescia",          45.5429, 10.2251),
    "J07": ("Piazzale Arnaldo",             45.5365, 10.2298),
    "J08": ("Stadio Rigamonti",             45.5478, 10.2278),
    "J09": ("Brixia Forum",                 45.5312, 10.1982),
    "J10": ("Università sede centrale",     45.5372, 10.2248),
    "J11": ("Università Ingegneria",        45.5645, 10.2315),
    "J12": ("Spedali Civili",               45.5565, 10.2318),
    "J13": ("Poliambulanza",                45.5212, 10.2370),
    "J14": ("Ist. Clinico Città BS",        45.5432, 10.2428),
    "J15": ("Quartiere Carmine",            45.5422, 10.2168),
    "J16": ("Zona Stazione / Fiumicello",   45.5328, 10.2128),
    "J17": ("Mompiano / Prealpino",         45.5698, 10.2098),
    "J18": ("Urago Mella / Sanpolino",      45.5252, 10.2598),
    "J19": ("Lamarmora / Brescia Due",      45.5195, 10.2205),
    "J20": ("San Polo / Vill. Sereno",      45.5130, 10.2478),
}

J = list(node_data.keys())


# K: user type
K = ["res", "wor", "vis"]



# T: Time slots
T = ["morning", "afternoon", "night"]



# PARAMETERS

# C(i): capacity of prking i
C = {i: parking_data[i][3] for i in I}

print(f"Total capacity: {sum(C.values())}")


# F(i): annual cost to open a new site (20 years)
F = {i: parking_data[i][4] for i in I}


# d(i,j): distance matrix (from i to j)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000    # average radius of the earth in meters
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a  = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.asin(math.sqrt(a))
 
urban_factor = 1.3
 
d = {}
for i in I:
    _, plat, plon, *_ = parking_data[i]
    for j in J:
        _, jlat, jlon = node_data[j]
        d[i, j] = round(haversine(plat, plon, jlat, jlon) * urban_factor)
        


# D(j,k,t): estimated parking demand for node j, user k and time slot t

# Residents, workers, visitors
demand_raw = {
    "J01": (1500,  4500, 2000),  
    "J02": ( 800,  2500, 2500),  
    "J03": ( 600,  2000, 1000), 
    "J04": ( 300,  3500,  500), 
    "J05": ( 200,   600, 1500),  
    "J06": ( 150,   200, 1200),  
    "J07": (3000,  2500, 1800),  
    "J08": (4000,   600,  500),  
    "J09": (1000,  2000, 1000),  
    "J10": (1500,  3500,  800),  
    "J11": (2000,  2500,  600),  
    "J12": ( 500,  6500, 3500),  
    "J13": (1500,  3000, 2000),  
    "J14": (2000,  1800,  800),  
    "J15": (8000,  2500,  200),  
    "J16": (6000,  4500, 2000),  
    "J17": (10000, 1500,  200),  
    "J18": (12000, 2000,  150), 
    "J19": (12000, 4500,  400), 
    "J20": (9000,  1200,  200),  
}        
        
tax_mot  = 0.62   # cars per inhabitant - Brescia motorization rate
use_rate = 0.32   # share of residents who use the car and look for parking
work_car = 0.55   # share of workers arriving by car
vis_car = 0.45   # share of visitors arriving by car


time_dist = {
    "res": [0.10, 0.30, 0.60],
    "wor": [0.70, 0.25, 0.05],
    "vis": [0.35, 0.60, 0.05],
}

# Percentage of parking demand by user type for every time slot


D = {}
for j in J:
    res, wor, vis = demand_raw[j]
    d_res = round(res * tax_mot * use_rate)
    d_wor = round(wor * work_car)
    d_vis = round(vis * vis_car)
    base  = {"res": d_res, "wor": d_wor, "vis": d_vis}
    for k in K:
        for ti, t in enumerate(T):
            D[j, k, t] = round(base[k] * time_dist[k][ti])

print(f"Total demand: {sum(D.values())}")



# P(k,t): tariff payed by user k in time slot t (€/h)

P = {
    ("res", "morning"): 0.85,  
    ("res", "afternoon"): 0.85,
    ("res", "night"): 0.18,   
    ("wor", "morning"): 1.30,  
    ("wor", "afternoon"): 1.30,
    ("wor", "night"): 0.50,  
    ("vis", "morning"): 1.70,   
    ("vis", "afternoon"): 2.00,  
    ("vis", "night"): 1.00,  
}


duration = {
    ("res", "morning"): 5.0,
    ("res", "afternoon"): 5.0,
    ("res", "night"): 10.0,
    ("wor", "morning"): 7.0,
    ("wor", "afternoon"): 7.0,
    ("wor", "night"): 7.0,
    ("vis", "morning"): 2.5,
    ("vis", "afternoon"): 2.5,
    ("vis", "night"): 2.5,
}

# medium parking duration for user type k in time slot t


revenue = {(k, t): P[k, t] * duration[k, t] for k in K for t in T}



# α(k): distance penalty (€/m)

alpha = {
    "res": 0.0040,   
    "wor": 0.0025,   
    "vis": 0.0015,   
}



# β(k): unmet demand penalty (€/auto)

beta = {
    "res": 3.50,     
    "wor": 2.50,     
    "vis": 1.20,     
}


