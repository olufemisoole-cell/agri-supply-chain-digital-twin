import networkx as nx
import matplotlib.pyplot as plt

def build_supply_chain_graph():
    # Initialize a directed graph (goods flow in one direction)
    G = nx.DiGraph()

    # Add Nodes (Facilities)
    plants = ['Processing_Plant_A', 'Processing_Plant_B']
    warehouses = ['Cold_Storage_1', 'Cold_Storage_2', 'Cold_Storage_3']
    retailers = ['Retail_Hub_1', 'Retail_Hub_2', 'Retail_Hub_3', 'Retail_Hub_4', 'Retail_Hub_5']

    G.add_nodes_from(plants, type='Plant')
    G.add_nodes_from(warehouses, type='Warehouse')
    G.add_nodes_from(retailers, type='Retailer')

    # Add Routes (Lead time in days, transit cost in $)
    G.add_edge('Processing_Plant_A', 'Cold_Storage_1', lead_time=2, transit_cost=500)
    G.add_edge('Processing_Plant_A', 'Cold_Storage_2', lead_time=3, transit_cost=750)
    G.add_edge('Processing_Plant_B', 'Cold_Storage_2', lead_time=2, transit_cost=400)
    G.add_edge('Processing_Plant_B', 'Cold_Storage_3', lead_time=4, transit_cost=900)

    G.add_edge('Cold_Storage_1', 'Retail_Hub_1', lead_time=1, transit_cost=150)
    G.add_edge('Cold_Storage_1', 'Retail_Hub_2', lead_time=1, transit_cost=200)
    G.add_edge('Cold_Storage_2', 'Retail_Hub_3', lead_time=2, transit_cost=300)
    G.add_edge('Cold_Storage_2', 'Retail_Hub_4', lead_time=1, transit_cost=100)
    G.add_edge('Cold_Storage_3', 'Retail_Hub_5', lead_time=2, transit_cost=250)

    return G

def visualize_network(G):
    # Set up colors based on facility type
    color_map = []
    for node, data in G.nodes(data=True):
        if data['type'] == 'Plant':
            color_map.append('lightblue')
        elif data['type'] == 'Warehouse':
            color_map.append('lightgreen')
        else:
            color_map.append('lightcoral')

    plt.figure(figsize=(12, 7))
    pos = nx.spring_layout(G, seed=42) 
    
    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=2500, 
            font_size=9, font_weight='bold', edge_color='gray', arrows=True)
    
    # Add labels for the routes
    edge_labels = {(u, v): f"{d['lead_time']} days\n${d['transit_cost']}" 
                   for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Agri-Food Supply Chain Digital Twin - Base Network")
    
    # Save the plot as an image file 
    plt.savefig("supply_chain_map.png")
    print("Success! Map saved as supply_chain_map.png")

if __name__ == "__main__":
    print("Building Supply Chain Network...")
    supply_network = build_supply_chain_graph()
    visualize_network(supply_network)