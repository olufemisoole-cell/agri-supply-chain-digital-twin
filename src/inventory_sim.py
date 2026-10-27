import random

def run_agentic_inventory_simulation(days):
    # Initial state
    inventory = {'Cold_Storage_1': 500}
    reorder_point = 350
    order_quantity = 200
    lead_time = 2  # Days it takes for a truck to arrive from Processing Plant A
    
    # Track orders on the road: {arrival_day: quantity}
    in_transit_orders = {}
    
    print(f"Starting {days}-Day Agentic Replenishment Simulation...\n")
    print("-" * 50)
    
    for day in range(1, days + 1):
        print(f"--- DAY {day} ---")
        
        # 1. MORNING: Receive incoming shipments FIRST (if any arrive today)
        if day in in_transit_orders:
            arriving_stock = in_transit_orders[day]
            inventory['Cold_Storage_1'] += arriving_stock
            print(f"[ARRIVAL] {arriving_stock} pallets arrived from Processing Plant A!")
            del in_transit_orders[day] # Clear the truck from the tracker
        
        # 2. AFTERNOON: Fulfill downstream demand
        daily_demand = random.randint(30, 60)
        inventory['Cold_Storage_1'] -= daily_demand
        
        print(f"Demand: {daily_demand} pallets shipped to retail hubs.")
        print(f"End-of-Day Stock: {inventory['Cold_Storage_1']} pallets.")
        
        # 3. EVENING: Agentic Logic (Check if we need to order)
        if inventory['Cold_Storage_1'] <= reorder_point:
            # Check if we already have shipments on the way to prevent over-ordering
            total_in_transit = sum(in_transit_orders.values())
            
            if inventory['Cold_Storage_1'] + total_in_transit <= reorder_point:
                arrival_day = day + lead_time
                in_transit_orders[arrival_day] = order_quantity
                print(f"--> [AGENT ACTION] Stock critical. Autonomously ordered {order_quantity} pallets.")
                print(f"--> [TRANSIT] Shipment dispatched. Will arrive on Day {arrival_day}.")
        
        print("-" * 50)

if __name__ == "__main__":
    # Let's run it for 10 days so we have time to see the shipment arrive!
    run_agentic_inventory_simulation(10)