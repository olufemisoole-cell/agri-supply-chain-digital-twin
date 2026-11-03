import random
import matplotlib.pyplot as plt
from network_graph import build_supply_chain_graph

def run_full_network_simulation(days):
    # 1. Load the complete Digital Twin Map (all 9 routes)
    G = build_supply_chain_graph()
    
    print("=" * 60)
    print(" ENTERPRISE DIGITAL TWIN: FULL NETWORK SIMULATION (9 ROUTES) ")
    print("=" * 60)
    
    # Print out all nodes and routes loaded from the map
    print(f"\n[MAP INSPECTION] Total Network Nodes: {G.number_of_nodes()}")
    print(f"[MAP INSPECTION] Total Transport Routes (Edges): {G.number_of_edges()}")
    
    for u, v, data in G.edges(data=True):
        print(f"   * Route: {u} -> {v} | Lead Time: {data['lead_time']} days | Cost: ${data['transit_cost']}")
    print("-" * 60)
    
    # 2. Define Inventory Levels for all Cold Storages & Retail Hubs in the network
    inventories = {
        'Cold_Storage_1': 500,
        'Cold_Storage_2': 500,
        'Cold_Storage_3': 500,
        'Retail_Hub_1': 200,
        'Retail_Hub_2': 200,
        'Retail_Hub_3': 200,
        'Retail_Hub_4': 200,
        'Retail_Hub_5': 200
    }
    
    reorder_threshold = 150 # Reorder point for warehouses
    order_qty = 200
    
    # Trackers for our final system-wide chart
    days_tracker = []
    cs1_tracker = []
    cs2_tracker = []
    cs3_tracker = []
    
    # In-transit tracker across the network
    in_transit_shipments = [] # Stores dictionaries of shipments
    
    print(f"\nStarting {days}-Day Full System Simulation...\n")
    
    for day in range(1, days + 1):
        print(f"=== DAY {day} ===")
        
        # 1. MORNING: Process incoming shipments across the network
        arrived_shipments = []
        for shipment in in_transit_shipments:
            shipment['remaining_lead_time'] -= 1
            if shipment['remaining_lead_time'] <= 0:
                # Shipment arrives at destination warehouse!
                dest = shipment['destination']
                qty = shipment['quantity']
                inventories[dest] += qty
                print(f"   [ARRIVAL] {qty} pallets arrived at {dest} from {shipment['source']}!")
                arrived_shipments.append(shipment)
                
        # Remove arrived shipments from active transit list
        for arrived in arrived_shipments:
            in_transit_shipments.remove(arrived)
            
        # 2. AFTERNOON: Downstream retail demand pulls inventory
        for node in inventories:
            if 'Retail' in node:
                # Retail demand
                demand = random.randint(10, 25)
                inventories[node] = max(0, inventories[node] - demand)
            elif 'Cold_Storage' in node:
                # Cold storage experiences daily baseline warehouse loss/demand
                demand = random.randint(25, 45)
                inventories[node] -= demand
        
        # 3. EVENING: Agentic Replenishment Logic for Cold Storages
        for cs_node in ['Cold_Storage_1', 'Cold_Storage_2', 'Cold_Storage_3']:
            if inventories[cs_node] <= reorder_threshold:
                # Find optimal inbound supplier route from our graph map!
                inbound_suppliers = list(G.predecessors(cs_node))
                best_supplier = inbound_suppliers[0] # Default to first
                lowest_cost = float('inf')
                
                # Optimize by cost
                for sup in inbound_suppliers:
                    cost = G.edges[sup, cs_node]['transit_cost']
                    if cost < lowest_cost:
                        lowest_cost = cost
                        best_supplier = sup
                        
                lead_time = G.edges[best_supplier, cs_node]['lead_time']
                
                # Dispatch order
                in_transit_shipments.append({
                    'source': best_supplier,
                    'destination': cs_node,
                    'quantity': order_qty,
                    'remaining_lead_time': lead_time
                })
                print(f"   --> [AGENT ACTION] Low stock at {cs_node} ({inventories[cs_node]} left). Ordered {order_qty} from {best_supplier} (Lead Time: {lead_time} days).")

        # Record daily metrics for charting
        days_tracker.append(day)
        cs1_tracker.append(inventories['Cold_Storage_1'])
        cs2_tracker.append(inventories['Cold_Storage_2'])
        cs3_tracker.append(inventories['Cold_Storage_3'])
        
        print(f"   [End-of-Day Status] CS1: {inventories['Cold_Storage_1']} | CS2: {inventories['Cold_Storage_2']} | CS3: {inventories['Cold_Storage_3']}")
        print("-" * 50)

    # 4. Generate Multi-Warehouse Enterprise Chart
    plt.figure(figsize=(10, 6))
    plt.plot(days_tracker, cs1_tracker, marker='o', label='Cold Storage 1', linewidth=2)
    plt.plot(days_tracker, cs2_tracker, marker='s', label='Cold Storage 2', linewidth=2)
    plt.plot(days_tracker, cs3_tracker, marker='^', label='Cold Storage 3', linewidth=2)
    
    plt.axhline(y=reorder_threshold, color='red', linestyle='--', label='Safety Threshold (150)', linewidth=2)
    plt.title("Enterprise Digital Twin - Multi-Warehouse Inventory Simulation (All 9 Routes Active)", fontsize=13, fontweight='bold')
    plt.xlabel("Day", fontsize=12)
    plt.ylabel("Pallet Stock Levels", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! Full enterprise multi-warehouse chart saved as inventory_chart.png")

if __name__ == "__main__":
    run_full_network_simulation(15)