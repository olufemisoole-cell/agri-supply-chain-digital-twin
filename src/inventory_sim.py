import random
import matplotlib.pyplot as plt
from network_graph import build_supply_chain_graph

def run_multi_route_optimization_simulation(days):
    # 1. Load the Digital Twin Map
    G = build_supply_chain_graph()
    
    target_warehouse = 'Cold_Storage_2'
    
    print(f"Connected to Digital Twin Map!")
    print(f"-> Analyzing Inbound Routes for: {target_warehouse}\n")
    
    # 2. OPTIMIZATION LOGIC: Find all incoming routes to Cold_Storage_2
    # NetworkX lets us look at all predecessors (nodes that point TO our target warehouse)
    inbound_suppliers = list(G.predecessors(target_warehouse))
    
    print(f"-> Found {len(inbound_suppliers)} alternative supplier plants feeding {target_warehouse}:")
    
    best_supplier = None
    lowest_cost = float('inf') # Start with an infinitely high cost placeholder
    
    # Evaluate each route to find the optimal (cheapest) one
    for plant in inbound_suppliers:
        edge_data = G.edges[plant, target_warehouse]
        l_time = edge_data['lead_time']
        t_cost = edge_data['transit_cost']
        
        print(f"   * Route from {plant}: Lead Time = {l_time} days | Cost = ${t_cost}")
        
        # Optimization Rule: Choose the route with the lowest transit cost
        if t_cost < lowest_cost:
            lowest_cost = t_cost
            best_supplier = plant
            optimal_lead_time = l_time

    print(f"\n[OPTIMIZATION RESULT] AI Agent selected optimal route:")
    print(f"-> Supplier: {best_supplier} -> {target_warehouse}")
    print(f"-> Optimized Lead Time: {optimal_lead_time} days")
    print(f"-> Optimized Cost: ${lowest_cost}\n")
    
    # 3. Simulation Setup for Cold Storage 2
    inventory = {target_warehouse: 500}
    reorder_point = 350
    order_quantity = 200
    
    in_transit_orders = {}
    days_tracker = []
    stock_tracker = []
    
    print(f"Starting {days}-Day Multi-Route Optimized Simulation...\n")
    print("-" * 50)
    
    for day in range(1, days + 1):
        print(f"--- DAY {day} ---")
        
        # Morning: Receive incoming shipments from the optimal plant
        if day in in_transit_orders:
            arriving_stock = in_transit_orders[day]
            inventory[target_warehouse] += arriving_stock
            print(f"[ARRIVAL] {arriving_stock} pallets arrived from {best_supplier}!")
            del in_transit_orders[day] 
        
        # Afternoon: Downstream retail demand
        daily_demand = random.randint(35, 65)
        inventory[target_warehouse] -= daily_demand
        print(f"Demand: {daily_demand} pallets shipped.")
        print(f"End-of-Day Stock: {inventory[target_warehouse]} pallets.")
        
        # Evening: Agentic Logic using the OPTIMIZED lead time from the winning route
        if inventory[target_warehouse] <= reorder_point:
            total_in_transit = sum(in_transit_orders.values())
            
            if inventory[target_warehouse] + total_in_transit <= reorder_point:
                arrival_day = day + optimal_lead_time
                in_transit_orders[arrival_day] = order_quantity
                print(f"--> [AGENT ACTION] Stock critical at {target_warehouse}.")
                print(f"--> [OPTIMIZED DISPATCH] Truck dispatched via {best_supplier}. Arriving in {optimal_lead_time} days (Day {arrival_day}).")
        
        days_tracker.append(day)
        stock_tracker.append(inventory[target_warehouse])
        print("-" * 50)

    # Generate the chart
    plt.figure(figsize=(10, 5))
    plt.plot(days_tracker, stock_tracker, marker='o', linestyle='-', color='#2ca02c', label=f'Stock Level ({target_warehouse})', linewidth=2)
    plt.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Stock Threshold (350)', linewidth=2)
    plt.title(f"Multi-Route Optimization - {target_warehouse} (Optimized via {best_supplier})", fontsize=14, fontweight='bold')
    plt.xlabel("Day", fontsize=12)
    plt.ylabel(f"Pallets in {target_warehouse}", fontsize=12)
    plt.ylim(200, 600)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! Multi-route optimized chart saved as inventory_chart.png")

if __name__ == "__main__":
    run_multi_route_optimization_simulation(15)