import streamlit as st
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from network_graph import build_supply_chain_graph

# 1. Page Setup
st.set_page_config(page_title="Agri Supply Chain Twin", layout="wide")
st.title("🌾 Agribusiness Digital Twin: Supply Chain Resilience")
st.markdown("Watch the AI agent dynamically reroute shipments during a crisis and manage perishable (FEFO) inventory.")

# 2. Interactive Sidebar Controls
st.sidebar.header("⚙️ Agent Parameters")
reorder_point = st.sidebar.slider("Safety Stock Threshold", 100, 500, 350, step=10)
order_quantity = st.sidebar.slider("Order Quantity", 100, 500, 200, step=10)
days_to_simulate = st.sidebar.slider("Days to Simulate", 10, 30, 20, step=1)

# Run Simulation Button
if st.sidebar.button("▶️ Run Digital Twin Simulation"):
    
    # 3. Background Setup (Same logic you built!)
    G = build_supply_chain_graph()
    start_date = datetime(2026, 11, 9)
    disruption_start = start_date + timedelta(days=6)
    disruption_end = start_date + timedelta(days=11)
    
    inventory_batches = [{'quantity': 500, 'production_date': start_date - timedelta(days=2), 
                          'arrival_date': start_date, 'expiry_date': start_date + timedelta(days=5)}]
    
    in_transit_orders = {}
    days_tracker, total_stock_tracker, spoiled_tracker = [], [], []
    
    # 4. The Simulation Loop
    for day_offset in range(days_to_simulate):
        current_date = start_date + timedelta(days=day_offset)
        spoiled_today = 0
        
        # Arrivals
        if current_date in in_transit_orders:
            arr = in_transit_orders[current_date]
            p_date = current_date - timedelta(days=arr['lead_time'])
            inventory_batches.append({
                'quantity': arr['quantity'], 'production_date': p_date, 
                'arrival_date': current_date, 'expiry_date': p_date + timedelta(days=9)
            })
            del in_transit_orders[current_date]
            
        # Spoilage
        for batch in inventory_batches:
            if batch['quantity'] > 0 and current_date >= batch['expiry_date']:
                spoiled_today += batch['quantity']
                batch['quantity'] = 0 
        inventory_batches = [b for b in inventory_batches if b['quantity'] > 0]
        
        # Retail Demand (FEFO)
        demand_left = random.randint(40, 70)
        inventory_batches.sort(key=lambda x: x['expiry_date'])
        for batch in inventory_batches:
            if demand_left > 0 and batch['quantity'] > 0:
                take = min(batch['quantity'], demand_left)
                batch['quantity'] -= take
                demand_left -= take
                
        # Agent Reorder Logic with Crisis Detection
        total_stock = sum(b['quantity'] for b in inventory_batches)
        is_crisis = disruption_start <= current_date <= disruption_end
        
        if total_stock <= reorder_point:
            total_in_transit = sum(o['quantity'] for o in in_transit_orders.values())
            if total_stock + total_in_transit <= reorder_point:
                
                # Dynamic Rerouting
                best_supplier, lowest_cost, optimal_lead = None, float('inf'), 0
                for sup in G.predecessors('Cold_Storage_2'):
                    if is_crisis and sup == 'Processing_Plant_B': continue
                    cost = G.edges[sup, 'Cold_Storage_2']['transit_cost']
                    if cost < lowest_cost:
                        lowest_cost, best_supplier = cost, sup
                        optimal_lead = G.edges[sup, 'Cold_Storage_2']['lead_time']
                
                arr_date = current_date + timedelta(days=optimal_lead)
                in_transit_orders[arr_date] = {'quantity': order_quantity, 'supplier': best_supplier, 'lead_time': optimal_lead}
                
        days_tracker.append(day_offset + 1)
        total_stock_tracker.append(total_stock)
        spoiled_tracker.append(spoiled_today)

    # 5. Draw the Web Chart
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(days_tracker, total_stock_tracker, marker='o', color='#1f77b4', label='Usable Stock')
    ax1.axvspan((disruption_start - start_date).days + 1, (disruption_end - start_date).days + 1, color='red', alpha=0.1, label='Plant B Blocked (Flood)')
    ax1.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Threshold')
    ax1.set_xlabel('Simulation Days')
    ax1.set_ylabel('Pallets in Stock', color='#1f77b4')
    
    ax2 = ax1.twinx()
    ax2.bar(days_tracker, spoiled_tracker, color='orange', alpha=0.5, label='Spoiled Pallets')
    ax2.set_ylabel('Spoiled', color='orange')
    
    plt.title("Live Digital Twin Simulation", fontweight='bold')
    
    # Output to Streamlit instead of saving a file!
    st.pyplot(fig)
    st.success("Simulation Complete! Adjust the sliders on the left to run a new scenario.")