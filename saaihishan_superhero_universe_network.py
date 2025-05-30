# -*- coding: utf-8 -*-
"""Saaihishan Superhero Universe Network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PrKxNxf-P2qO_aXSE0Nxb60NGyMw0RqM
"""

import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import matplotlib.pyplot as plt

def load_data():
    """Load superhero and connection data from CSV files."""
    try:
        heroes = pd.read_csv('superheroes.csv')
        links = pd.read_csv('links.csv')
    except FileNotFoundError:
        # Create empty DataFrames if files don't exist
        heroes = pd.DataFrame(columns=['id', 'name', 'created_at'])
        links = pd.DataFrame(columns=['source', 'target'])
    return heroes, links

def save_data(heroes, links):
    """Save data back to CSV files."""
    heroes.to_csv('superheroes.csv', index=False)
    links.to_csv('links.csv', index=False)

def analyze_network(heroes, links):
    """Create and analyze the network graph."""
    G = nx.Graph()

    # Add nodes (superheroes)
    for _, row in heroes.iterrows():
        G.add_node(row['id'], name=row['name'], created_at=row['created_at'])

    # Add edges (connections)
    for _, row in links.iterrows():
        G.add_edge(row['source'], row['target'])

    return G

def get_network_stats(G, heroes):
    """Calculate and return network statistics."""
    stats = {}

    stats['total_superheroes'] = G.number_of_nodes()
    stats['total_connections'] = G.number_of_edges()

    # Superheroes added in the last 3 days
    today = datetime.now().date()
    three_days_ago = today - timedelta(days=3)
    recent_heroes = heroes[pd.to_datetime(heroes['created_at']).dt.date >= three_days_ago]
    stats['recently_added'] = recent_heroes[['id', 'name', 'created_at']].to_dict('records')

    # Top 3 most connected superheroes
    degrees = dict(G.degree())
    top_connected = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:3]
    stats['top_connected'] = []
    for hero_id, connections in top_connected:
        hero_name = heroes[heroes['id'] == hero_id]['name'].values[0]
        stats['top_connected'].append({'id': hero_id, 'name': hero_name, 'connections': connections})

    # dataiskole information
    if 'dataiskole' in heroes['name'].values:
        dataiskole = heroes[heroes['name'] == 'dataiskole']
        dataiskole_id = dataiskole['id'].values[0]
        stats['dataiskole'] = {
            'added_date': dataiskole['created_at'].values[0],
            'friends': []
        }
        for neighbor in G.neighbors(dataiskole_id):
            friend_name = heroes[heroes['id'] == neighbor]['name'].values[0]
            stats['dataiskole']['friends'].append({'id': neighbor, 'name': friend_name})

    return stats

def visualize_network(G, heroes):
    """Visualize the network and save as image."""
    plt.figure(figsize=(12, 10))

    id_to_name = {row['id']: row['name'] for _, row in heroes.iterrows()}
    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5)

    labels = {node: id_to_name.get(node, str(node)) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')

    plt.title("Superhero Network", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('superhero_network.png')
    plt.show(block=False)  # Changed to non-blocking
    plt.pause(0.1)  # Small pause to allow the plot to render

def add_new_superhero(heroes):
    """Allow user to add a new superhero."""
    print("\n--- Add New Superhero ---")
    name = input("Enter superhero name: ").strip()

    if name in heroes['name'].values:
        print(f"Error: Superhero '{name}' already exists!")
        return heroes

    # Generate new ID
    new_id = heroes['id'].max() + 1 if not heroes.empty else 1

    # Get current date in YYYY-MM-DD format
    created_at = datetime.now().strftime('%Y-%m-%d')

    new_hero = pd.DataFrame({'id': [new_id], 'name': [name], 'created_at': [created_at]})
    heroes = pd.concat([heroes, new_hero], ignore_index=True)

    print(f"Successfully added {name} (ID: {new_id}) on {created_at}")
    return heroes

def add_new_connection(heroes, links):
    """Allow user to add multiple new connections for a single source superhero."""
    print("\n--- Add New Connections ---")
    print("Current superheroes:")
    print(heroes[['id', 'name']].to_string(index=False))

    try:
        source_id = int(input("\nEnter source superhero ID: "))
    except ValueError:
        print("Error: Please enter a valid numeric ID")
        return links

    # Validate source ID exists
    if source_id not in heroes['id'].values:
        print(f"Error: Superhero with ID {source_id} doesn't exist!")
        return links

    # Get target IDs
    target_input = input("Enter target superhero ID(s), separated by commas: ").strip()
    target_ids = [tid.strip() for tid in target_input.split(',')]

    new_connections = []
    source_name = heroes[heroes['id'] == source_id]['name'].values[0]

    for target in target_ids:
        try:
            target_id = int(target)
        except ValueError:
            print(f"Skipping invalid target ID: {target}")
            continue

        # Validate target ID exists
        if target_id not in heroes['id'].values:
            print(f"Error: Superhero with ID {target_id} doesn't exist - skipping")
            continue

        # Skip if connecting to self
        if source_id == target_id:
            print(f"Warning: Cannot connect {source_name} to itself - skipping")
            continue

        # Check if connection already exists
        if ((links['source'] == source_id) & (links['target'] == target_id)).any() or \
           ((links['source'] == target_id) & (links['target'] == source_id)).any():
            target_name = heroes[heroes['id'] == target_id]['name'].values[0]
            print(f"Warning: Connection between {source_name} and {target_name} already exists - skipping")
            continue

        new_connections.append({'source': source_id, 'target': target_id})
        target_name = heroes[heroes['id'] == target_id]['name'].values[0]
        print(f"Added connection: {source_name} ↔ {target_name}")

    if new_connections:
        new_links = pd.DataFrame(new_connections)
        links = pd.concat([links, new_links], ignore_index=True)
        print(f"\nSuccessfully added {len(new_connections)} new connection(s) for {source_name}")
    else:
        print("\nNo valid new connections were added")

    return links

def user_menu():
    """Display interactive menu for user."""
    print("\n===== Superhero Network Manager =====")
    print("1. View Network Statistics")
    print("2. Add New Superhero")
    print("3. Add New Connections")
    print("4. Visualize Network")
    print("5. Exit")

    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if 1 <= choice <= 5:
                return choice
            print("Please enter a number between 1 and 5")
        except ValueError:
            print("Please enter a valid number")

def main():
    # Load data
    heroes, links = load_data()

    while True:
        choice = user_menu()

        if choice == 1:  # View stats
            G = analyze_network(heroes, links)
            stats = get_network_stats(G, heroes)

            print("\n=== Superhero Network Analysis ===")
            print(f"Total superheroes: {stats['total_superheroes']}")
            print(f"Total connections: {stats['total_connections']}")

            print("\nRecently added (last 3 days):")
            for hero in stats['recently_added']:
                print(f"- {hero['name']} (ID: {hero['id']}, Added: {hero['created_at']})")

            print("\nTop 3 most connected:")
            for hero in stats['top_connected']:
                print(f"- {hero['name']} (ID: {hero['id']}): {hero['connections']} connections")

            if 'dataiskole' in stats:
                print("\ndataiskole info:")
                print(f"- Added: {stats['dataiskole']['added_date']}")
                print("- Friends:")
                for friend in stats['dataiskole']['friends']:
                    print(f"  - {friend['name']} (ID: {friend['id']})")

        elif choice == 2:  # Add superhero
            heroes = add_new_superhero(heroes)
            save_data(heroes, links)

        elif choice == 3:  # Add connections
            links = add_new_connection(heroes, links)
            save_data(heroes, links)

        elif choice == 4:  # Visualize
            try:
                G = analyze_network(heroes, links)
                visualize_network(G, heroes)
                print("Network visualization saved as 'superhero_network.png'")
                print("Note: The plot window may appear behind your terminal. You can continue using the program.")
            except ImportError:
                print("Error: matplotlib is required for visualization. Install with 'pip install matplotlib'")

        elif choice == 5:  # Exit
            print("Saving data and exiting...")
            save_data(heroes, links)
            # Close any open matplotlib windows
            plt.close('all')
            break

if __name__ == "__main__":
    main()

