# Agri-Food Supply Chain Digital Twin & Agentic AI Replenishment

## Overview
This project is a lightweight Digital Twin and Agentic AI simulation built in Python, designed to model and autonomously manage a multi-echelon agricultural supply chain. It transitions inventory management from reactive dashboarding to proactive, autonomous execution.

## The Business Problem
In agricultural and FMCG supply chains, volatile downstream demand and strict transit lead times frequently lead to stockouts or excessive holding costs (the Bullwhip Effect). Traditional ERP alerts require human intervention to calculate lead times and dispatch shipments, which introduces delays.

## The Solution
This project simulates a regional supply chain network (Processing Plants $\rightarrow$ Cold Storage $\rightarrow$ Retail Hubs) and introduces an **Autonomous Replenishment Agent**. 

### Key Features:
* **Network Mapping:** Utilizes `NetworkX` to define supply chain nodes, transit routes, and lead times.
* **Stochastic Demand Simulation:** Models randomized daily pallet pulls from downstream retail hubs.
* **Agentic Orchestration:** An algorithmic agent monitors safety stock thresholds (350 pallets). When breached, it autonomously calculates in-transit inventory to prevent over-ordering, places a replenishment order, and tracks the 2-day lead time to delivery.
* **Visualization:** Uses `Matplotlib` to dynamically generate a "Sawtooth" inventory curve, proving the agent successfully prevents stockouts while minimizing excess holding capacity.

## Tech Stack
* **Python 3**
* `NetworkX` (Graph logic and digital twin mapping)
* `Pandas` / `SciPy` (Data handling and optimization)
* `Matplotlib` (Visualization)

## Example Output
The agent successfully maintains inventory stability, reacting to demand drops and perfectly timing the 2-day transit lead time to replenish stock just before a stockout occurs.