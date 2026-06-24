# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:47:49 2026

@author: Utente
"""

# Solve & compare

model.obj_A = pyo.Objective(rule=obj_cost_min,      sense=pyo.minimize)
model.obj_B = pyo.Objective(rule=obj_social_profit,  sense=pyo.maximize)
model.obj_B.deactivate()

solver = pyo.SolverFactory('glpk')

results_A = {}
results_B = {}


# SCENARIO A: COST MINIMIZATION

print("\n" + "="*60)
print("SCENARIO A — Cost minimization")
print("="*60)

model.obj_A.activate()
model.obj_B.deactivate()
res = solver.solve(model)


if res.solver.termination_condition == pyo.TerminationCondition.optimal:
    print(f"State: OPTIMAL FOUND")
    print(f"Objective value: {pyo.value(model.obj_A):,.0f} €/anno")

    # New parkings opened
    print("\nNew parkings opened:")
    opened_A = []
    for i in I_new:
        if pyo.value(model.x[i]) > 0.5:
            opened_A.append(i)
            print(f"  ✓ {i} — {parking_data[i][0]}")
    if not opened_A:
        print("  No new parking opened")

    # Unmet demand per user type
    print("\nAverage unmet demand per user type:")
    for k in K:
        unmet = sum(pyo.value(model.u[j,k,t]) * D[j,k,t]
                    for j in J for t in T)
        total = sum(D[j,k,t] for j in J for t in T)
        print(f"  {k}: {unmet:,.0f} car/day ({unmet/total*100:.1f}% of the demand)")

    results_A = {
        'obj': pyo.value(model.obj_A),
        'opened': opened_A,
        'y': {(i,j,k,t): pyo.value(model.y[i,j,k,t])
              for i in I for j in J for k in K for t in T},
        'u': {(j,k,t): pyo.value(model.u[j,k,t])
              for j in J for k in K for t in T},
    }
else:
    print(f"State: {res.solver.termination_condition}")



# SCENARIO B: SOCIAL PROFIT MAXIMIZATION

print("\n" + "="*60)
print("SCENARIO B — Social profit maximization")
print("="*60)

model.obj_A.deactivate()
model.obj_B.activate()
res = solver.solve(model, tee=False)

if res.solver.termination_condition == pyo.TerminationCondition.optimal:
    print(f"State: Optimal found")
    print(f"Objective value: {pyo.value(model.obj_B):,.0f} €/anno")

    print("\nNew parkings opened:")
    opened_B = []
    for i in I_new:
        if pyo.value(model.x[i]) > 0.5:
            opened_B.append(i)
            print(f"  ✓ {i} — {parking_data[i][0]}")
    if not opened_B:
        print("  No new parking opened")

    print("\nAverage unmet demand per user type:")
    for k in K:
        unmet = sum(pyo.value(model.u[j,k,t]) * D[j,k,t]
                    for j in J for t in T)
        total = sum(D[j,k,t] for j in J for t in T)
        print(f"  {k}: {unmet:,.0f} car/day ({unmet/total*100:.1f}% of the demand)")

    results_B = {
        'obj': pyo.value(model.obj_B),
        'opened': opened_B,
        'y': {(i,j,k,t): pyo.value(model.y[i,j,k,t])
              for i in I for j in J for k in K for t in T},
        'u': {(j,k,t): pyo.value(model.u[j,k,t])
              for j in J for k in K for t in T},
    }
else:
    print(f"State: {res.solver.termination_condition}")



# Comparison: Scenario A vs Scenario B
if results_A and results_B:
    print("\n" + "="*60)
    print("SCENARIO COMPARISON A vs B")
    print("="*60)

    print(f"\n{'':30} {'Scenario A':>15} {'Scenario B':>15}")
    print("-"*60)

    # New opened sites
    n_A = len(results_A['opened'])
    n_B = len(results_B['opened'])
    print(f"{'New opened sites':30} {n_A:>15} {n_B:>15}")

    # Total unmet demand
    u_A = sum(results_A['u'][j,k,t] * D[j,k,t]
              for j in J for k in K for t in T)
    u_B = sum(results_B['u'][j,k,t] * D[j,k,t]
              for j in J for k in K for t in T)
    tot = sum(D[j,k,t] for j in J for k in K for t in T)
    print(f"{'Unmet demand':30} "
          f"{u_A:>12,.0f} ({u_A/tot*100:.1f}%)"
          f" {u_B:>12,.0f} ({u_B/tot*100:.1f}%)")

    # Average distance traveled
    def avg_dist(results):
        num = sum(results['y'][i,j,k,t] * D[j,k,t] * d[i,j]
                  for i in I for j in J for k in K for t in T)
        den = sum(results['y'][i,j,k,t] * D[j,k,t]
                  for i in I for j in J for k in K for t in T)
        return num/den if den > 0 else 0

    dA = avg_dist(results_A)
    dB = avg_dist(results_B)
    print(f"{'Average distance traveled':30} {dA:>14,.0f} m {dB:>14,.0f} m")

    print("-"*60)
    print("\nOpened sites:")
    only_A = set(results_A['opened']) - set(results_B['opened'])
    only_B = set(results_B['opened']) - set(results_A['opened'])
    both   = set(results_A['opened']) & set(results_B['opened'])
    if both:   print(f"  Opened in both cases: {list(both)}")
    if only_A: print(f"  Only in Scenario A: {list(only_A)}")
    if only_B: print(f"  Only in Scenario B: {list(only_B)}")







