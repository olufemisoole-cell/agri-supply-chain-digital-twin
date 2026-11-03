import random
import matplotlib.pyplot as plt

# 1. IMPORT THE MAP: Bring in our network builder function from the other file!
from network_graph import build_supply_chain_graph

def run_network_aware_simulation(days):
    # 2. LOAD THE DIGITAL TWIN: Build the graph map inside this simulation
    G = build_supply_chain_graph()
    
    # 3. DYNAMICALLY READ THE MAP: Look up the exact lead time and cost between Plant A and Cold Storage 1!
    lead_time = G.edges['Processing_Plant_A', 'Cold_Storage_1']['lead_time']
    transit_cost = G.edges['Processing_Plant_A', 'Cold_Storage_1']['transit_cost']
    
    print(f"Connected to Digital Twin Map!")
    print(f"-> Route Loaded: Processing_Plant_A -> Cold_Storage_1")
    print(f"-> Dynamically Read Lead Time: {lead_time} days")
    print(f"-> Dynamically Read Transit Cost: ${transit_cost}\n")
    
    inventory = {'Cold_Storage_1': 500}
    reorder_point = 350
    order_quantity = 200
    
    in_transit_orders = {}
    days_tracker = []
    stock_tracker = []
    
    print(f"Starting {days}-Day Network-Aware Simulation...\n")
    print("-" * 50)
    
    for day in range(1, days + 1):
        print(f"--- DAY {day} ---")
        
        # Morning: Receive incoming shipments
        if day in in_transit_orders:
            arriving_stock = in_transit_orders[day]
            inventory['Cold_Storage_1'] += arriving_stock
            print(f"[ARRIVAL] {arriving_stock} pallets arrived from Processing Plant A!")
            del in_transit_orders[day] 
        
        # Afternoon: Downstream retail demand
        daily_demand = random.randint(30, 60)
        inventory['Cold_Storage_1'] -= daily_demand
        print(f"Demand: {daily_demand} pallets shipped.")
        print(f"End-of-Day Stock: {inventory['Cold_Storage_1']} pallets.")
        
        # Evening: Agentic Logic using the DYNAMIC lead time from our map
        if inventory['Cold_Storage_1'] <= reorder_point:
            total_in_transit = sum(in_transit_orders.values())
            
            if inventory['Cold_Storage_1'] + total_in_transit <= reorder_point:
                arrival_day = day + lead_time  # Uses the variable we pulled straight from the map!
                in_transit_orders[arrival_day] = order_quantity
                print(f"--> [AGENT ACTION] Stock critical. Autonomously ordered {order_quantity} pallets.")
                print(f"--> [TRANSIT] Truck dispatched via map route. Will arrive in {lead_time} days (Day {arrival_day}).")
        
        days_tracker.append(day)
        stock_tracker.append(inventory['Cold_Storage_1'])
        print("-" * 50)

    # Generate the chart
    plt.figure(figsize=(10, 5))
    plt.plot(days_tracker, stock_tracker, marker='o', linestyle='-', color='#1f77b4', label='Daily Stock Level', linewidth=2)
    plt.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Stock Threshold (350)', linewidth=2)
    plt.title(f"Digital Twin Simulation - Network-Aware Lead Time ({lead_time} Days)", fontsize=14, fontweight='bold')
    plt.xlabel("Day", fontsize=12)
    plt.ylabel("Pallets in Cold Storage 1", fontsize=12)
    plt.ylim(200, 600)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! Network-aware chart saved as inventory_chart.png")

if __name__ == "__main__":
    run_network_aware_simulation(15)