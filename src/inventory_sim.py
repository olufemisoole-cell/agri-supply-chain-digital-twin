import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from network_graph import build_supply_chain_graph

def run_disruption_simulation(days_to_simulate):
    G = build_supply_chain_graph()
    target_warehouse = 'Cold_Storage_2'
    
    print("=" * 70)
    print(" DIGITAL TWIN: CRISIS DISRUPTION & DYNAMIC REROUTING ")
    print("=" * 70)
    
    start_date = datetime(2026, 11, 9) 
    total_shelf_life_days = 9          
    
    # 1. DEFINE THE CRISIS WINDOW
    disruption_start = start_date + timedelta(days=6)  # Nov 15
    disruption_end = start_date + timedelta(days=11)   # Nov 20
    
    inventory_batches = [
        {
            'quantity': 500,
            'production_date': start_date - timedelta(days=2),
            'arrival_date': start_date,
            'expiry_date': start_date + timedelta(days=5) 
        }
    ]
    
    reorder_point = 350
    order_quantity = 200
    in_transit_orders = {} # Now stores dictionaries of supplier data
    
    days_tracker = []
    total_stock_tracker = []
    spoiled_tracker = []
    
    for day_offset in range(days_to_simulate):
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')
        
        print(f"\n--- DATE: {date_str} ---")
        spoiled_today = 0
        
        # Morning 1: Receive New Shipments
        if current_date in in_transit_orders:
            arriving_qty = in_transit_orders[current_date]['quantity']
            supplier = in_transit_orders[current_date]['supplier']
            lead_time = in_transit_orders[current_date]['lead_time']
            
            prod_date = current_date - timedelta(days=lead_time)
            exp_date = prod_date + timedelta(days=total_shelf_life_days)
            
            inventory_batches.append({
                'quantity': arriving_qty,
                'production_date': prod_date,
                'arrival_date': current_date,
                'expiry_date': exp_date
            })
            print(f"[ARRIVAL] {arriving_qty} pallets received from {supplier}!")
            del in_transit_orders[current_date]
            
        # Morning 2: Date-Based Spoilage Check
        for batch in inventory_batches:
            if batch['quantity'] > 0 and current_date >= batch['expiry_date']:
                print(f"   --> [SPOILAGE ALERT] {batch['quantity']} pallets expired and were scrapped!")
                spoiled_today += batch['quantity']
                batch['quantity'] = 0 
        
        inventory_batches = [b for b in inventory_batches if b['quantity'] > 0]
        
        # Afternoon: Retail Demand
        daily_demand = random.randint(40, 70)
        demand_left = daily_demand
        inventory_batches.sort(key=lambda x: x['expiry_date'])
        
        for batch in inventory_batches:
            if demand_left > 0 and batch['quantity'] > 0:
                take = min(batch['quantity'], demand_left)
                batch['quantity'] -= take
                demand_left -= take
                
        # Evening: DYNAMIC AI DISRUPTION CHECK
        total_stock = sum(batch['quantity'] for batch in inventory_batches)
        print(f"Demand: {daily_demand} pallets. Usable Stock Left: {total_stock}")
        
        # Is the road washed out today?
        is_crisis = disruption_start <= current_date <= disruption_end
        if is_crisis:
            print(f"   [CRISIS ALERT] Severe flooding! Route from Processing_Plant_B is BLOCKED.")
        
        if total_stock <= reorder_point:
            total_in_transit = sum(order['quantity'] for order in in_transit_orders.values())
            if total_stock + total_in_transit <= reorder_point:
                
                # 2. THE AI EVALUATES ROUTES DYNAMICALLY TODAY
                inbound_suppliers = list(G.predecessors(target_warehouse))
                best_supplier = None
                lowest_cost = float('inf')
                optimal_lead_time = 0
                
                for sup in inbound_suppliers:
                    # If Route B is blocked during the crisis, the AI completely ignores it!
                    if is_crisis and sup == 'Processing_Plant_B':
                        continue
                        
                    cost = G.edges[sup, target_warehouse]['transit_cost']
                    if cost < lowest_cost:
                        lowest_cost = cost
                        best_supplier = sup
                        optimal_lead_time = G.edges[sup, target_warehouse]['lead_time']
                
                arrival_date = current_date + timedelta(days=optimal_lead_time)
                
                # Save the order details so the warehouse knows where it came from
                in_transit_orders[arrival_date] = {
                    'quantity': order_quantity,
                    'supplier': best_supplier,
                    'lead_time': optimal_lead_time
                }
                
                print(f"--> [AGENT ACTION] Ordered {order_quantity} pallets from {best_supplier}.")
                print(f"    Cost: ${lowest_cost} | Lead Time: {optimal_lead_time} days | Arrival: {arrival_date.strftime('%Y-%m-%d')}")
                
        days_tracker.append(day_offset + 1)
        total_stock_tracker.append(total_stock)
        spoiled_tracker.append(spoiled_today)

    # 3. Chart Generation with Crisis Highlighting
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(days_tracker, total_stock_tracker, marker='o', color='#1f77b4', label='Total Usable Stock', linewidth=2)
    
    # Draw a shaded red box over the crisis dates on the chart!
    disruption_start_day = (disruption_start - start_date).days + 1
    disruption_end_day = (disruption_end - start_date).days + 1
    ax1.axvspan(disruption_start_day, disruption_end_day, color='red', alpha=0.1, label='Plant B Road Blocked')
    
    ax1.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Threshold')
    ax1.set_xlabel(f'Simulation Days')
    ax1.set_ylabel('Pallets in Stock', color='#1f77b4')
    
    ax2 = ax1.twinx()
    ax2.bar(days_tracker, spoiled_tracker, color='orange', alpha=0.5, label='Spoiled Pallets')
    ax2.set_ylabel('Spoiled Pallets', color='orange')
    
    plt.title(f"Dynamic Rerouting & Supply Chain Crisis Simulation ({target_warehouse})", fontweight='bold')
    fig.tight_layout()
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! Disruption chart saved as inventory_chart.png")

if __name__ == "__main__":
    run_disruption_simulation(20) # We extended this to 20 days to see the full crisis!