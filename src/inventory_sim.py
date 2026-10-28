import random
import matplotlib.pyplot as plt

def run_agentic_inventory_simulation(days):
    inventory = {'Cold_Storage_1': 500}
    reorder_point = 350
    order_quantity = 200
    lead_time = 2  
    
    in_transit_orders = {}
    
    # NEW: Lists to track data for our chart
    days_tracker = []
    stock_tracker = []
    
    print(f"Starting {days}-Day Agentic Replenishment Simulation...\n")
    print("-" * 50)
    
    for day in range(1, days + 1):
        print(f"--- DAY {day} ---")
        
        # 1. MORNING: Receive incoming shipments
        if day in in_transit_orders:
            arriving_stock = in_transit_orders[day]
            inventory['Cold_Storage_1'] += arriving_stock
            print(f"[ARRIVAL] {arriving_stock} pallets arrived from Processing Plant A!")
            del in_transit_orders[day] 
        
        # 2. AFTERNOON: Fulfill downstream demand
        daily_demand = random.randint(30, 60)
        inventory['Cold_Storage_1'] -= daily_demand
        
        print(f"Demand: {daily_demand} pallets shipped.")
        print(f"End-of-Day Stock: {inventory['Cold_Storage_1']} pallets.")
        
        # 3. EVENING: Agentic Logic 
        if inventory['Cold_Storage_1'] <= reorder_point:
            total_in_transit = sum(in_transit_orders.values())
            
            if inventory['Cold_Storage_1'] + total_in_transit <= reorder_point:
                arrival_day = day + lead_time
                in_transit_orders[arrival_day] = order_quantity
                print(f"--> [AGENT ACTION] Stock critical. Autonomously ordered {order_quantity} pallets.")
        
        # NEW: Save today's data for the chart
        days_tracker.append(day)
        stock_tracker.append(inventory['Cold_Storage_1'])
        
        print("-" * 50)

    # NEW: Generate the visual chart
    plt.figure(figsize=(10, 5))
    
    # Plot the daily stock
    plt.plot(days_tracker, stock_tracker, marker='o', linestyle='-', color='#1f77b4', label='Daily Stock Level', linewidth=2)
    
    # Add a red dashed line for the safety threshold
    plt.axhline(y=reorder_point, color='red', linestyle='--', label='Safety Stock Threshold (350)', linewidth=2)
    
    # Formatting the chart to look professional
    plt.title("Agentic AI Replenishment - Warehouse Inventory Simulation", fontsize=14, fontweight='bold')
    plt.xlabel("Day", fontsize=12)
    plt.ylabel("Pallets in Cold Storage 1", fontsize=12)
    plt.ylim(200, 600)  # Keep the Y-axis fixed for clean viewing
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Save the chart as an image file
    plt.savefig("inventory_chart.png", bbox_inches='tight')
    print("\nSuccess! Chart saved as inventory_chart.png")

if __name__ == "__main__":
    # Run it for 15 days this time to get a beautiful, long sawtooth curve
    run_agentic_inventory_simulation(15)