import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from network_graph import build_supply_chain_graph

def run_erp_date_simulation(days_to_simulate):
    G = build_supply_chain_graph()
    target_warehouse = 'Cold_Storage_2'
    
    print("=" * 70)
    print(" AGRIBUSINESS ERP: DATE-BASED BATCH TRACKING & FEFO DISPATCH ")
    print("=" * 70)
    
    # 1. SET UP REAL CALENDAR DATES
    start_date = datetime(2026, 11, 9) # Starting the simulation today
    total_shelf_life_days = 9          # Total days a product is good for after production
    
    # The starting inventory now tracks specific real-world dates
    inventory_batches = [
        {
            'quantity': 500,
            'production_date': start_date - timedelta(days=2),
            'arrival_date': start_date,
            'expiry_date': start_date + timedelta(days=5) # Expires on Nov 14
        }
    ]
    
    reorder_point = 350
    order_quantity = 200
    
    # Map optimization logic
    inbound_suppliers = list(G.predecessors(target_warehouse))
    best_supplier = inbound_suppliers[0]
    lowest_cost = float('inf')
    for sup in inbound_suppliers:
        cost = G.edges[sup, target_warehouse]['transit_cost']
        if cost < lowest_cost:
            lowest_cost = cost
            best_supplier = sup
    optimal_lead_time = G.edges[best_supplier, target_warehouse]['lead_time']
    
    in_transit_orders = {}
    
    days_tracker = []
    total_stock_tracker = []
    spoiled_tracker = []
    
    # 2. RUN THE LOOP USING ACTUAL CALENDAR DATES
    for day_offset in range(days_to_simulate):
        # Calculate the exact calendar date for "today" in the loop
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')
        
        print(f"\n--- DATE: {date_str} ---")
        spoiled_today = 0
        
        # Morning 1: Receive New Shipments
        if current_date in in_transit_orders:
            arriving_qty = in_transit_orders[current_date]
            
            # Automatically generate the ERP dates for the new arrival
            prod_date = current_date - timedelta(days=optimal_lead_time)
            exp_date = prod_date + timedelta(days=total_shelf_life_days)
            
            inventory_batches.append({
                'quantity': arriving_qty,
                'production_date': prod_date,
                'arrival_date': current_date,
                'expiry_date': exp_date
            })
            print(f"[ARRIVAL] {arriving_qty} pallets received.")
            print(f"   -> Mfg Date: {prod_date.strftime('%Y-%m-%d')} | Exp Date: {exp_date.strftime('%Y-%m-%d')}")
            del in_transit_orders[current_date]
            
        # Morning 2: Date-Based Spoilage Check
        for batch in inventory_batches:
            if batch['quantity'] > 0:
                # If today's date matches or passes the expiry date, it rots
                if current_date >= batch['expiry_date']:
                    print(f"   --> [SPOILAGE ALERT] {batch['quantity']} pallets expired on {batch['expiry_date'].strftime('%Y-%m-%d')} and were scrapped!")
                    spoiled_today += batch['quantity']
                    batch['quantity'] = 0 
        
        inventory_batches = [b for b in inventory_batches if b['quantity'] > 0]
        
        # Afternoon: Retail Demand using FEFO (Sorting by Expiry Date!)
        daily_demand = random.randint(40, 70)
        demand_left = daily_demand
        
        # SORT BY CALENDAR EXPIRY DATE
        inventory_batches.sort(key=lambda x: x['expiry_date'])
        
        for batch in inventory_batches:
            if demand_left > 0 and batch['quantity'] > 0:
                take = min(batch['quantity'], demand_left)
                batch['quantity'] -= take
                demand_left -= take
                
        actual_shipped = daily_demand - demand_left
        print(f"Demand: {daily_demand} pallets. Shipped: {actual_shipped} pallets (FEFO).")
        
        # Evening: AI Agent Check
        total_stock = sum(batch['quantity'] for batch in inventory_batches)
        print(f"End-of-Day Total Usable Stock: {total_stock} pallets.")
        
        if total_stock <= reorder_point:
            total_in_transit = sum(in_transit_orders.values())
            if total_stock + total_in_transit <= reorder_point:
                arrival_date = current_date + timedelta(days=optimal_lead_time)
                in_transit_orders[arrival_date] = order_quantity
                print(f"--> [AGENT ACTION] Ordered {order_quantity} pallets from {best_supplier}. Expected arrival: {arrival_date.strftime('%Y-%m-%d')}.")
                
        days_tracker.append(day_offset + 1)
        total_stock_tracker.append(total_stock)
        spoiled_tracker.append(spoiled_today)

    # Chart Generation
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(days_tracker, total_stock_tracker, marker='o', color='#1f77b4', label='Total Usable Stock', linewidth=2)
    ax1.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Threshold')
    ax1.set_xlabel(f'Simulation Days (Starting {start_date.strftime("%Y-%m-%d")})')
    ax1.set_ylabel('Pallets in Stock', color='#1f77b4')
    ax1.tick_params(axis='y', labelcolor='#1f77b4')
    
    ax2 = ax1.twinx()
    ax2.bar(days_tracker, spoiled_tracker, color='orange', alpha=0.5, label='Spoiled Pallets')
    ax2.set_ylabel('Spoiled Pallets Thrown Away', color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    
    plt.title(f"ERP-Integrated Agribusiness FEFO Simulation ({target_warehouse})", fontweight='bold')
    fig.tight_layout()
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! ERP Date-Based FEFO chart saved.")

if __name__ == "__main__":
    run_erp_date_simulation(15)