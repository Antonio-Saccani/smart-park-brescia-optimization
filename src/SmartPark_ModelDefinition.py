# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:50:01 2026

@author: Utente
"""

# 2. Model definition

import pyomo.environ as pyo

model = pyo.ConcreteModel(name="SmartPark_Brescia")

# SETS

model.I = pyo.Set(initialize=I)
model.J = pyo.Set(initialize=J)
model.K = pyo.Set(initialize=K)
model.T = pyo.Set(initialize=T)

# PARAMETERS

model.C = pyo.Param(model.I, initialize=C)
model.F = pyo.Param(model.I, initialize=F)
model.d = pyo.Param(model.I, model.J, initialize=d)
model.D = pyo.Param(model.J, model.K, model.T, initialize=D)
model.revenue = pyo.Param(model.K, model.T, initialize=revenue)
model.alpha = pyo.Param(model.K, initialize=alpha)
model.beta = pyo.Param(model.K, initialize=beta)


# VARIABLES

# x(i): binary variable - 1 for existing sites - 0 or 1 for new sites

model.x = pyo.Var(model.I, domain=pyo.Binary)
for i in I_exist:
    model.x[i].fix(1)
 
    
# y(i,j,k,t): fraction of the total parking demand to be assigned to parking i

model.y = pyo.Var(model.I, model.J, model.K, model.T,
                  bounds=(0, 1),
                  domain=pyo.NonNegativeReals)


# u(j,k,t): fraction of unsatisfied parking demand

model.u = pyo.Var(model.J, model.K, model.T,
                  bounds=(0, 1),
                  domain=pyo.NonNegativeReals)



# CONSTRAINTS

# Demand satisfaction

def demand_satisfaction(model, j, k, t):
    return (sum(model.y[i,j,k,t] for i in model.I)
            + model.u[j,k,t]
            == 1)
 
model.demand_sat = pyo.Constraint(
    model.J, model.K, model.T,
    rule=demand_satisfaction
)


# Parking capacity

def capacity_constraint(model, i, t):
    return (sum(model.D[j,k,t] * model.y[i,j,k,t]
                for j in model.J
                for k in model.K)
            <= model.C[i] * model.x[i])
 
model.capacity = pyo.Constraint(
    model.I, model.T,
    rule=capacity_constraint
)



# OBJECTIVE FUNCTIONS

# Minimizing costs

def obj_cost_min(model):
    fixed_costs = sum(
        model.F[i] * model.x[i]
        for i in model.I
    )
    distance_penalty = sum(
        model.alpha[k] * model.d[i,j]
        * model.D[j,k,t] * model.y[i,j,k,t]
        * 365
        for i in model.I
        for j in model.J
        for k in model.K
        for t in model.T
    )
    unmet_penalty = sum(
        model.beta[k] * model.D[j,k,t] * model.u[j,k,t]
        * 365
        for j in model.J
        for k in model.K
        for t in model.T
    )
    return fixed_costs + distance_penalty + unmet_penalty



# Maximizing social profit

def obj_social_profit(model):
    revenues = sum(
        model.revenue[k,t] * model.D[j,k,t] * model.y[i,j,k,t]
        * 365
        for i in model.I
        for j in model.J
        for k in model.K
        for t in model.T
    )
    fixed_costs = sum(
        model.F[i] * model.x[i]
        for i in model.I
    )
    distance_penalty = sum(
        model.alpha[k] * model.d[i,j]
        * model.D[j,k,t] * model.y[i,j,k,t]
        * 365
        for i in model.I
        for j in model.J
        for k in model.K
        for t in model.T
    )
    unmet_penalty = sum(
        model.beta[k] * model.D[j,k,t] * model.u[j,k,t]
        * 365
        for j in model.J
        for k in model.K
        for t in model.T
    )
    return revenues - fixed_costs - distance_penalty - unmet_penalty




