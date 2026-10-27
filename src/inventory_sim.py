import random

def run_inventory_simulation(days):
    # 1. Set the starting inventory for your main warehouse
    # Let's say Cold Storage 1 starts with 500 pallets of agricultural goods
    inventory = {'Cold_Storage_1': 500} 
    
    print(f"Starting {days}-Day Inventory Simulation...\n")
    print(f"Initial Stock: {inventory['Cold_Storage_1']} pallets in Cold_Storage_1\n")
    print("-" * 40)
    
    # 2. The "Clock" - simulating day by day
    for day in range(1, days + 1):
        
        # Simulate downstream retailers pulling random demand (between 30 and 60 pallets a day)
        daily_demand = random.randint(30, 60)
        
        # Subtract today's demand from the warehouse
        inventory['Cold_Storage_1'] -= daily_demand
        
        # Print the daily status update
        print(f"Day {day}: Retail hubs ordered {daily_demand} pallets.")
        print(f"         Remaining Stock: {inventory['Cold_Storage_1']} pallets.")
        
        # 3. Supply Chain Logic: Trigger a warning if stock drops below a safety threshold
        if inventory['Cold_Storage_1'] <= 350:
            print(f"  --> [ALERT] Safety stock threshold breached! Agentic AI needs to trigger a replenishment order from Processing Plant A.")
        
        print("-" * 40)

if __name__ == "__main__":
    # Run the simulation for 7 days
    run_inventory_simulation(7)