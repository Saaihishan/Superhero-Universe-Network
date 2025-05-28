# Superhero-Universe-Network


This is a Python application designed to manage, analyze, and visualize a network of superheroes and their relationships. It allows users to add superheroes, define connections, view network statistics, and generate a visual representation of the network.

---

## How to Run the Code

1. **Install Required Libraries**  
   Ensure you have the necessary libraries installed:
   ```bash
   pip install pandas networkx matplotlib
   
2. **Prepare Required Files**
Ensure the following CSV files are in your working directory (they will be created automatically if missing):

superheroes.csv

links.csv

3. **Run the Script**
   
Execute the script using Python:

python superhero_network.py

4. **Follow the Menu**
Once running, you can:

View network statistics

Add new superheroes

Add new connections

Visualize the network graph

## Sample Output

**Statistics**

===== Superhero Network Manager =====
1. View Network Statistics
2. Add New Superhero
3. Add New Connections
4. Visualize Network
5. Exit
Enter your choice (1-5): 3

--- Add New Connections ---
Current superheroes:
 id            name
  1      Spider-Man
  2       Iron Man
  3           Thor
  4           Hulk
  5 Captain America
  6   Black Widow
  7 Doctor Strange
  8  Black Panther
  9 Scarlet Witch
 10        Ant-Man
 11    dataiskole

Enter source superhero ID: 11
Enter target superhero ID(s), separated by commas: 2,3,99,5,11,7
Added connection: dataiskole ↔ Iron Man
Added connection: dataiskole ↔ Thor
Error: Superhero with ID 99 doesn't exist - skipping
Added connection: dataiskole ↔ Captain America
Warning: Cannot connect dataiskole to itself - skipping
Added connection: dataiskole ↔ Doctor Strange

Successfully added 4 new connection(s) for dataiskole


**Network Visualization**


A visual graph of the superhero network will be displayed and saved as superhero_network.png in the working directory.




## Tools and Libraries Used

pandas – For reading and writing tabular data in CSV format.

networkx – For creating, analyzing, and managing the graph structure of the superhero network.

matplotlib – For visualizing the network graph.

datetime – For handling timestamps related to superhero creation.

## Notes

Each superhero must have a unique name.

Self-connections and duplicate connections are automatically prevented.

The created_at field is automatically filled with the current date when a new superhero is added.

The application highlights specific information if a superhero named dataiskole is present in the dataset.

All updates are saved back to the corresponding CSV files after each operation.


## File Structure


├── superhero_network.py       # Main application script
├── superheroes.csv            # Superhero data (auto-generated if not present)
├── links.csv                  # Connection data (auto-generated if not present)
└── superhero_network.png      # Network graph image (generated after visualization)


Example Interactive Menu

===== Superhero Network Manager =====
1. View Network Statistics
2. Add New Superhero
3. Add New Connections
4. Visualize Network
5. Exit
Enter your choice (1-5):

This tool is useful for exploring network analysis concepts in a simplified context. It can be adapted for other types of social or relational networks as needed.


