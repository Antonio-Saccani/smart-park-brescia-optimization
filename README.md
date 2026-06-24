# SmartPark Brescia: Optimization-Based Decision Support System for Urban Parking Planning

## Project Overview

SmartPark Brescia is an optimization-based decision support system developed to support urban parking planning in the city of Brescia, Italy.

The project aims to identify the optimal locations for new parking facilities in order to maximize demand coverage while considering investment constraints and operational feasibility.

A Mixed Integer Linear Programming (MILP) model was developed and tested under different planning scenarios to evaluate alternative parking expansion strategies and support evidence-based decision making.

---

## Research Question

**Which parking facilities should be opened to maximize parking demand coverage in Brescia under different investment scenarios?**

---

## Methodology

The project combines operations research techniques and data-driven decision making through:

* Facility Location Optimization
* Mixed Integer Linear Programming (MILP)
* Scenario Analysis
* Sensitivity Analysis
* Demand Coverage Evaluation

The optimization model determines which candidate parking sites should be activated while assigning demand nodes to parking facilities based on capacity and distance constraints.

---

## Data

The analysis is based on:

* Parking demand estimates for demand nodes across Brescia
* Distance matrix between demand nodes and parking facilities
* Existing parking infrastructure
* Candidate locations for new parking facilities

The complete datasets are available in the `data/` folder.

---

## Repository Structure

```text
smart-park-brescia-optimization/
│
├── README.md
├── report/
├── data/
├── src/
├── images/
└── results/
```

### Main Components

| Folder     | Description                                   |
| ---------- | --------------------------------------------- |
| `src/`     | Python source code and optimization model     |
| `data/`    | Input datasets used by the model              |
| `images/`  | Maps, figures and project visualizations      |
| `report/`  | Final report, presentation and project poster |
| `results/` | Optimization outputs and scenario results     |

---

## Technologies

* Python
* Pyomo
* Pandas
* Excel
* Mathematical Optimization
* Operations Research

---

## Key Outputs

The project provides:

* Optimal parking location recommendations
* Demand allocation strategies
* Comparison of alternative investment scenarios
* Sensitivity analysis on model parameters
* Decision support for urban planning

---

## Project Documents

The complete project documentation is available in the `report/` folder:

* Final Project Report
* Project Presentation
* Project Poster

---

## Authors

Saccani Antonio, Ripari Matteo, Porru Mattia.
Project developed as part of the Optimization Methods in Business Analytics course within the MSc in Analytics and Data Science for Economics and Management.

