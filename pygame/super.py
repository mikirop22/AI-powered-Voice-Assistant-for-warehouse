#welcome to the Supermarket Pathfinder software! 
#install libraries 
import sqlite3 
from tkinter import * 

#connect database 
conn = sqlite3.connect('Supermarket Items.db') 
cur = conn.cursor() 
#create database 
cur.execute("""CREATE TABLE IF NOT EXISTS "Item" ("ID" INTEGER NOT NULL UNIQUE,"Name" TEXT NOT NULL,"Description" TEXT,PRIMARY KEY("ID" AUTOINCREMENT))""") 
cur.execute("""CREATE TABLE IF NOT EXISTS "Location" ("ID" INTEGER NOT NULL UNIQUE, "Aisle" INTEGER NOT NULL, "Bay" TEXT NOT NULL, "Shelf" INTEGER NOT NULL, PRIMARY KEY("ID" AUTOINCREMENT))""") 
cur.execute("""CREATE TABLE IF NOT EXISTS "Link" ("Item_ID" INTEGER, "Location_ID" INTEGER, FOREIGN KEY("Item_ID") REFERENCES "Item"("ID"), 
FOREIGN KEY("Location_ID") REFERENCES "Location"("ID"), PRIMARY KEY("Item_ID","Location_ID"))""") 


#manager login screen 
def login(): 
    #destroy the first menu 
    window.destroy() 
    #make variables global 
    global password_attempt 
    global manager_login 
    #create the login window 
    manager_login = Tk() 
    manager_login.geometry("200x100") 
    manager_login.title("Manager Login") 
    pass_label = Label(manager_login, text="Password:") 
    password_attempt = Entry(manager_login, show="*") 
    pass_label.grid(row=0, column=0) 
    password_attempt.grid(row=0,column=1) 
    #button that runs the password check function 
    login_button = Button(manager_login, text="Login", command=password_check).grid(row=1, column=1) 
 

#check that the password entered in the manager login is correct 
def password_check(): 
    password = "WnK2!d" 
    if password_attempt.get() == password: 
        print("Success") 
        manager_menu() 
    else: 
        print("Incorrect.") 
        password_attempt.delete(0, END) 
 

#manager option menu 
def manager_menu(): 
    manager_login.destroy() 
    global manager_menu 
    manager_menu = Tk() 
    manager_menu.title("Manager Menu") 
    edit_button = Button(manager_menu, text="Edit Item", padx=30, pady=10, command=find_item_to_edit).pack() 
    add_button = Button(manager_menu, text="Add New Item", padx=30, pady=10, command=add_item).pack() 


#find the location ID for the aisle bay and shelf combination 
def get_location_id(aisle,bay,shelf): 
    cur.execute("SELECT ID FROM Location WHERE Aisle = ? AND Bay = ? AND Shelf = ?",(aisle,bay,shelf)) 
    location_id = str(cur.fetchall()) 
    location_id = location_id[2:] 
    location_id = location_id[:-3] 
    location_id = int(location_id) 
    print("id: ",location_id) 
    return location_id 


def submit_edit(): 
    #get the inputs 
    name = new_item_name.get() 
    description = new_item_description.get() 
    aisle = int(new_item_aisle.get()) 
    bay = new_item_bay.get() 
    shelf = new_item_shelf.get() 
    #destroy previous window 
    edit_item.destroy() 
    #check validity of inputs 
    bays = ["L1","L2","L3","L4","L5","R1","R2","R3","R4","R5"] 
    shelves = ["A","B","C","D","E"] 
    if bay in bays and shelf in shelves and aisle < 6 and aisle > 0: 
        #update name and description 
        cur.execute("UPDATE Item SET Name = ?, Description = ? WHERE ID = ?",(name,description,item_id)) 
        #update link table 
        location_id = get_location_id(aisle,bay,shelf) 
        cur.execute("UPDATE Link SET Location_ID = ? WHERE Item_ID = ?",(location_id,item_id)) 
        print("submitted") 


#edit an item in the database 
def edit_item(): 
    #variables 
    global edit_item 
    global new_item_name 
    global new_item_description 
    global new_item_aisle 
    global new_item_bay 
    global new_item_shelf 
    global item_id 
    item_id = id_input.get()
    #check that the item id is in the database
    cur.execute("SELECT ID FROM Item")
    all_ids_tuple = cur.fetchall()
    ids = []
    for i in all_ids_tuple:
        id_number = str(i)
        id_number = id_number[1:] 
        id_number = id_number[:-2]
        ids.append(id_number)
    if item_id in ids:
        #window setup 
        find_item.destroy() 
        edit_item = Tk() 
        edit_item.title("Edit Item") 
        edit_item.geometry("800x300") 
        #find the item's info 
        #name 
        cur.execute("SELECT Name FROM Item WHERE ID = ?",[item_id]) 
        orig_name = str(cur.fetchall()) 
        orig_name = orig_name[2:] 
        orig_name = orig_name[:-3] 
        #description 
        cur.execute("SELECT Description FROM Item WHERE ID = ?",[item_id]) 
        orig_desc = str(cur.fetchall()) 
        orig_desc = orig_desc[2:] 
        orig_desc = orig_desc[:-3] 
        #aisle, bay, and shelf
        orig_aisle, orig_bay, orig_shelf = get_location(item_id) 
        #location id 
        cur.execute("SELECT Location_ID FROM Link WHERE Item_ID = ?",[item_id]) 
        location_id = str(cur.fetchall()) 
        location_id = location_id[2:] 
        location_id = location_id[:-3] 
        location_id = int(location_id)  
        #labels for the original item info 
        id_ = Label(edit_item, text="ID: ") 
        name = Label(edit_item, text="Name: ") 
        description = Label(edit_item, text="Description: ") 
        aisle_number = Label(edit_item, text="Aisle: ") 
        bay_number = Label(edit_item, text="Bay: ") 
        shelf = Label(edit_item, text="Shelf: ") 
        original_id = Label(edit_item, text=item_id) 
        original_name = Label(edit_item, text=orig_name) 
        original_description = Label(edit_item, text=orig_desc) 
        original_aisle_number = Label(edit_item, text=orig_aisle) 
        original_bay_number = Label(edit_item, text=orig_bay) 
        original_shelf = Label(edit_item, text=orig_shelf) 
        #input boxes 
        new_item_name = Entry(edit_item, width=30) 
        new_item_description = Entry(edit_item, width=30) 
        new_item_aisle = Entry(edit_item, width=30) 
        new_item_bay = Entry(edit_item, width=30) 
        new_item_shelf = Entry(edit_item, width=30) 
        #labels for the inputs 
        name_label = Label(edit_item, text="New Name:") 
        description_label = Label(edit_item, text="New Description:") 
        aisle_label = Label(edit_item, text="New Aisle number:") 
        bay_label = Label(edit_item, text="New Bay:") 
        shelf_label = Label(edit_item, text="New Shelf:") 
        #positioning of widgets 
        id_.grid(row=0, column=0) 
        name.grid(row=1, column=0) 
        description.grid(row=2, column=0) 
        aisle_number.grid(row=3, column=0) 
        bay_number.grid(row=4, column=0) 
        shelf.grid(row=5, column=0) 
        original_id.grid(row=0, column=1) 
        original_name.grid(row=1, column=1) 
        original_description.grid(row=2, column=1) 
        original_aisle_number.grid(row=3, column=1) 
        original_bay_number.grid(row=4, column=1) 
        original_shelf.grid(row=5, column=1) 
        name_label.grid(row=1,column=5) 
        new_item_name.grid(row=1,column=6) 
        description_label.grid(row=2,column=5) 
        new_item_description.grid(row=2,column=6) 
        aisle_label.grid(row=3,column=5) 
        new_item_aisle.grid(row=3,column=6) 
        bay_label.grid(row=4,column=5) 
        new_item_bay.grid(row=4,column=6) 
        shelf_label.grid(row=5,column=5) 
        new_item_shelf.grid(row=5,column=6) 
        #submit button to commit changes 
        submit_button = Button(edit_item, text="Submit Edit", padx=30, pady=10, command=submit_edit) 
        submit_button.grid(row=6,column=1)
    else:
        print("ID not in database")


def find_item_to_edit(): 
    global id_input 
    global find_item 
    manager_menu.destroy() 
    find_item = Tk() 
    find_item.title("Find Item To Edit") 
    find_item.geometry("800x100") 
    info_label = Label(find_item, text="Enter the ID of the item you would like to edit below.") 
    id_label = Label(find_item, text="ID:") 
    id_input = Entry(find_item, width=20) 
    button = Button(find_item, text="Edit", command=edit_item) 
    info_label.grid(row=0,column=0) 
    id_label.grid(row=1,column=0) 
    id_input.grid(row=1,column=1) 
    button.grid(row=2,column=0) 


#submit a new item to the database 
def submit_item(): 
    #connect database 
    conn = sqlite3.connect('Supermarket Items.db') 
    cur = conn.cursor() 
    #define possible inputs 
    bays = ["L1","L2","L3","L4","L5","R1","R2","R3","R4","R5"] 
    shelves = ["A","B","C","D","E"] 
    names = [] 
    cur.execute("SELECT Name FROM Item") 
    for row in cur.fetchall(): 
        names.append(row) 
    print(names) 
    #get the inputs 
    name = item_name.get() 
    description = item_description.get() 
    aisle = int(item_aisle.get()) 
    bay = item_bay.get() 
    shelf = item_shelf.get().upper() 
    #check that each input is valid then update the database accordingly 
    if bay in bays and shelf in shelves and aisle < 6 and aisle > 0 and name not in names: 
        cur.execute("INSERT INTO Item (Name, Description) VALUES (?,?)", (name, description)) 
        cur.execute("SELECT ID FROM Item WHERE Name = ? AND Description = ?",(name,description)) 
        id_number = str(cur.fetchall()) 
        id_number = id_number[2:] 
        id_number = id_number[:-3] 
        id_number = int(id_number) 
        print("item id: ",id_number) 
        location_id = get_location_id(aisle,bay,shelf) 
        cur.execute("INSERT INTO Link (Item_ID, Location_ID) VALUES (?,?)", (id_number,location_id)) 
        print("item submitted") 
    elif bay not in bays: 
        print("Incorrect bay format.") 
    elif shelf not in shelves: 
        print("Incorrect shelf format.") 
    elif name in names: 
        print("Item already exists.") 
    else: 
        print("Aisle does not exist.") 
    #commit changes 
    conn.commit() 
    #close database 
    conn.close()      
    #clear input boxes 
    item_name.delete(0, END) 
    item_description.delete(0, END) 
    item_aisle.delete(0, END) 
    item_bay.delete(0, END) 
    item_shelf.delete(0, END) 
    return 


#interface to add a new item to the database 
def add_item(): 
    manager_menu.destroy() 
    global item_name 
    global item_description 
    global item_aisle 
    global item_bay 
    global item_shelf 
    global add_item 
    add_item = Tk() 
    add_item.title("Add New Item") 
    add_item.geometry("300x300") 
    #input boxes 
    item_name = Entry(add_item, width=30) 
    item_description = Entry(add_item, width=30) 
    item_aisle = Entry(add_item, width=30) 
    item_bay = Entry(add_item, width=30) 
    item_shelf = Entry(add_item, width=30) 
    #labels for the inputs 
    name_label = Label(add_item, text="Name:") 
    description_label = Label(add_item, text="Description:") 
    aisle_label = Label(add_item, text="Aisle number:") 
    bay_label = Label(add_item, text="Bay:") 
    shelf_label = Label(add_item, text="Shelf:") 
    #positioning of widgets 
    name_label.grid(row=0,column=0) 
    item_name.grid(row=0,column=1) 
    description_label.grid(row=1,column=0) 
    item_description.grid(row=1,column=1) 
    aisle_label.grid(row=2,column=0) 
    item_aisle.grid(row=2,column=1) 
    bay_label.grid(row=3,column=0) 
    item_bay.grid(row=3,column=1) 
    shelf_label.grid(row=4,column=0) 
    item_shelf.grid(row=4,column=1) 
    #submit button to commit changes 
    submit_button = Button(add_item, text="Submit Item", padx=30, pady=10, command=submit_item) 
    submit_button.grid(row=6,column=1) 


def create_list(): 
    window.destroy() 
    global shopping_list 

    #define functions to be used 
    def update(contents): 
        #empty the list 
        item_list.delete(0,END) 
        #add the items into the list 
        for i in contents: 
            item_list.insert(END, i) 

    def update_shopping_list(contents): 
        #empty the list 
        shopping_list_box.delete(0,END) 
        #add the items into the list 
        for i in contents: 
            shopping_list_box.insert(END, i) 

    def autofill(event): 
        #empty the box 
        search.delete(0, END) 
        #add the clicked item into the box 
        search.insert(0, item_list.get(ACTIVE))         

    def filter_search(event): 
        #get the value in the search box 
        searched_for = search.get() 
        #if all input is deleted, show the entire list of available items 
        if searched_for == "": 
            contents = items 
        else: 
            #loop through the items checking if the searched term is in the list 
            contents = [] 
            for i in items: 
                if searched_for.lower() in i.lower(): 
                    #add any matches to the contents of the on screen list 
                    contents.append(i) 
        #update the on screen list 
        update(contents) 

    def add_item(): 
        #add the item selected to the shopping list 
        current_item = search.get() 
        if current_item in items: 
            shopping_list.append(current_item) 
            update_shopping_list(shopping_list) 
    #make the window 
    global customer_menu 
    customer_menu = Tk() 
    customer_menu.title("Create Shopping List") 
    customer_menu.geometry("400x500") 
    label = Label(customer_menu, text="Add items by typing in the box below.") 
    label.grid(row=0,column=0) 
    shopping_list_label = Label(customer_menu, text="Your List:") 
    shopping_list_label.grid(row=3,column=0) 
    #button to add each item 
    add_to_list = Button(customer_menu, text="Add Item", command=add_item) 
    add_to_list.grid(row=5,column=0) 
    #run the pathfinding function 
    run_pathfinder = Button(customer_menu, text="Find Route", command=pathfind) 
    run_pathfinder.grid(row=6,column=0) 
    #get the items from the database into a list 
    items = [] 
    cur.execute("SELECT * FROM Item") 
    for row in cur.fetchall(): 
        items.append(row[1]) 
    #search box 
    search = Entry(customer_menu) 
    search.grid(row=1,column=0) 
    #On-screen list of all items 
    item_list = Listbox(customer_menu, width=50) 
    item_list.grid(row=2,column=0) 
    #Add items to the on-screen list 
    update(items) 
    #autofill feature 
    #Create a binding on the item list when an item is clicked 
    item_list.bind("<<ListboxSelect>>", autofill) 
    #Search filter feature 
    #Create a binding on the search box 
    search.bind("<KeyRelease>", filter_search) 
    #display the shopping list on screen 
    shopping_list = [] 
    shopping_list_box = Listbox(customer_menu, width=50) 
    shopping_list_box.grid(row=4,column=0) 


def get_location(node_id): 
    #find the location id for the current item 
    cur.execute("SELECT Location_ID FROM Link WHERE Item_ID = ?", [node_id]) 
    location_id = str(cur.fetchall()) 
    #prepare the location id for fetching from the database 
    location_id = location_id[2:] 
    location_id = location_id[:-3] 
    location_id = int(location_id)
    #get the location of that item 
    cur.execute("SELECT Aisle, Bay, Shelf FROM Location WHERE ID = ?", [location_id]) 
    abs_tuple = cur.fetchall()                    
    aisle_number = abs_tuple[0][0] 
    bay = abs_tuple[0][1]    
    shelf = abs_tuple[0][2]
    return aisle_number, bay, shelf


def get_item_name(item_id): 
    #find the item name
    cur.execute("SELECT Name FROM Item WHERE ID = ?", [item_id]) 
    #prepare the name for returning to the program
    item_name = str(cur.fetchall()) 
    item_name = item_name[2:] 
    item_name = item_name[:-3]  
    return item_name


#pathfinding function to find the least distance route 
def pathfind(): 
    customer_menu.destroy() 
    #replace all of the item names in shopping list with their IDs 
    for i in range(len(shopping_list)): 
        current_name = shopping_list[i] 
        cur.execute("SELECT ID FROM Item WHERE Name = ?", [current_name]) 
        current_item_id = str(cur.fetchall()) 
        #make the fetched ids into singular numbers 
        current_item_id = current_item_id[2:] 
        current_item_id = current_item_id[:-3] 
        #add the ids back into the shopping list 
        shopping_list[i] = int(current_item_id)   

    #create a distance matrix to represent the shopping list 
    def create_graph(shopping_list): 
        #three lists to store the nodes, their adjacent nodes and the arc weight between each node in the graph 
        item_nodes = [] 
        arc_weights = [] 
        adjacent_nodes = [] 
        #loop through the items 
        for x in range(len(shopping_list)): 
            current_node = shopping_list.pop(x) 
            distances = [] 
            adjacents = [] 
            #loop through the items adjacent to the current item 
            for y in range(len(shopping_list)): 
                next_node = shopping_list[y] 
                current_aisle, current_bay, current_shelf = get_location(current_node) 
                next_aisle, next_bay, next_shelf = get_location(next_node) 
                #get the bay number from the bay string 
                bay_number = int(current_bay[1]) 
                next_bay_number = int(next_bay[1]) 
                #calculate the distance between the two items 
                current_position = int(current_aisle) + bay_number 
                next_position = int(next_aisle) + next_bay_number 
                #compare size of position to calculate the positive difference between the items (arc weight) 
                if current_position > next_position: 
                    arc_weight = current_position - next_position 
                elif next_position > current_position: 
                    arc_weight = next_position - current_position 
                else: 
                    arc_weight = 0 
                distances.append(arc_weight) 
                adjacents.append(next_node) 
            shopping_list.insert(x,current_node) 
            #update graph every time the shopping list is iterated through for the current item 
            item_nodes.append(current_node) 
            arc_weights.append(distances) 
            adjacent_nodes.append(adjacents) 
        return item_nodes, arc_weights, adjacent_nodes 

    #use the nearest neighbour method to find a route 
    def nearest_neighbor(shopping_list):
        all_items_nn = [] 
        all_distances_nn = [] 
        all_adjacents_nn = []     

        def remove_item(items, distances, adjacent_nodes, i): 
            #lists to store the graph when the current node is removed 
            edited_items = [] 
            edited_distances = [] 
            edited_adjacents = [] 
            #remove the current node, its associated distances and adjacents 
            removed_item = items.pop(i) 
            removed_distances = distances.pop(i) 
            removed_adjacency = adjacent_nodes.pop(i) 
            #append the remaining items to the edited item list 
            for item in items: 
                edited_items.append(item)       
            #lists to store the distances and adjacent nodes that will be popped 
            popped_adjacents = [] 
            popped_distances = [] 
            #pop all of the distances linking the current item to the other items, also pop the item itself from the other adjacency lists 
            position = 0 
            for adj in adjacent_nodes: 
                if removed_item in adj: 
                    index = adj.index(removed_item) 
                    popped_adjacents.append(adj.pop(index)) 
                    edited_adjacents.append(adj) 
                    popped_distances.append(distances[position].pop(index)) 
                    edited_distances.append(distances[position]) 
                position += 1 
            item_nodes = edited_items 
            arc_weights = edited_distances 
            adjacent_nodes = edited_adjacents 

        def next_node(current_index):
            for n in range(len(item_nodes)-1): 
                current_distances = [] 
                #add all of the distances for the current node to the current distances list 
                for n in range(len(arc_weights[current_index])): 
                    current_distances.append(arc_weights[current_index][n]) 
                #find the nearest neighbor and append the arc weight to the distances list 
                least_distance = min(current_distances) 
                #find the index of the least distance, which will correspond to the next item 
                least_distance_index = current_distances.index(least_distance) 
                #keep track of the last index so that item can be removed 
                previous_index = current_index 
                #update the current index to move onto the next node 
                nn_item_nodes.append(item_nodes[current_index]) 
                next_item = adjacent_nodes[current_index][least_distance_index] 
                remove_item(item_nodes, arc_weights, adjacent_nodes, previous_index) 
                current_index = item_nodes.index(next_item) 
                nn_nearest_nodes.append(item_nodes[current_index]) 
                nn_nearest_distances.append(least_distance)      
            return nn_item_nodes, nn_nearest_distances, nn_nearest_nodes 

        def select_node(item_nodes): 
            nn_item_nodes, nn_nearest_distances, nn_nearest_nodes = next_node(0) 
            all_items_nn.append(nn_item_nodes) 
            all_distances_nn.append(nn_nearest_distances) 
            all_adjacents_nn.append(nn_nearest_nodes) 

        for n in range(len(shopping_list)): 
            nn_item_nodes = [] 
            nn_nearest_distances = [] 
            nn_nearest_nodes = [] 
            item_nodes, arc_weights, adjacent_nodes = create_graph(shopping_list) 
            #for nn to find all possible routes, we have to rearrange the list so each node in the list is used as a starting point. 
            starting_node = item_nodes.pop(n) 
            starting_node_distances = arc_weights.pop(n) 
            starting_node_adjacents = adjacent_nodes.pop(n) 
            item_nodes.insert(-1,starting_node) 
            arc_weights.insert(-1, starting_node_distances) 
            adjacent_nodes.insert(-1, starting_node_adjacents) 
            select_node(item_nodes) 
        #find out which route has the lowest cost 
        total_cost = 100000 
        route_index = 0 
        #loop through each nearest neighbor result 
        for x in all_distances_nn: 
            current_cost = 0 
            #add together all of the distances 
            for y in x: 
                current_cost += y 
            #add the cost of beginning and ending at the entrance to the cost 
            #find the distance of the first item from the entrance 
            first_item_id = all_items_nn[all_distances_nn.index(x)][0] 
            #get the aisle and bay numbers 
            first_aisle, first_bay, first_shelf = get_location(first_item_id) 
            first_bay = int(first_bay[1]) 
            #find the distance of the last item from the entrance 
            last_item_id = all_items_nn[all_distances_nn.index(x)][-1] 
            #get the aisle and bay numbers 
            last_aisle, last_bay, last_shelf = get_location(last_item_id) 
            last_bay = int(last_bay[1]) 
            #add these to the current cost 
            current_cost += int(first_aisle) 
            current_cost += int(first_bay) 
            current_cost += int(last_aisle) 
            current_cost += int(last_bay) 
            #check the cost against the final cost to find the lowest cost route 
            if current_cost < total_cost: 
                total_cost = current_cost 
                route_index = all_distances_nn.index(x) 
        final_route_items = all_items_nn[route_index] 
        final_route_adjacents = all_adjacents_nn[route_index] 
        return final_route_items, final_route_adjacents, route_index   

    #order the item ids to display on the map 
    def final_route_nn(items, adjacents, index): 
        final_route = [] 
        final_route.append(items[0]) 
        n = 0 
        for i in adjacents: 
            final_route.append(i) 
        return final_route     

    #create the map 
    def customer_map(final_items_ordered): 
        #lists to be used in loop  
        worded_locations = []        
        coords_list = []        
        #counter to keep track of the item index
        n = 1
        for item_id in final_items_ordered: 
            #make a list of all the item names             
            all_items_list = [] 
            for item in final_items_ordered:  
                name = get_item_name(item) 
                all_items_list.append(name) 
            #get item name  
            item_name = get_item_name(item_id) 
            #get location 
            #find the location id for the current item 
            cur.execute("SELECT Location_ID FROM Link WHERE Item_ID = ?", [item_id]) 
            location_id = str(cur.fetchall()) 
            #prepare the location id for fetching from the database 
            location_id = location_id[2:] 
            location_id = location_id[:-3] 
            location_id = int(location_id) 
            #get the location of that item to use with the coordinates 
            aisle_number, current_bay, shelf_name = get_location(location_id)
            bay_number = int(current_bay[1]) 
            #get a written version of the location 
            aisle_name = "Aisle " + str(aisle_number) 
            if "L" in current_bay: 
                bay_name = "Left Bay " + str(bay_number) 
            else: 
                bay_name = "Right Bay " + str(bay_number) 
            location_name = aisle_name + ", " + bay_name + ", " + shelf_name 
            worded_locations.append(location_name)  
            #find the coords for the box on the canvas corresponding with the location 
            box_coordinates = [] 
            if "L" in current_bay: 
                coord = (2*aisle_number-1)*100 
                box_coordinates.append(coord) 
            elif "R" in current_bay: 
                coord = (2*aisle_number-1)*100+125 
                box_coordinates.append(coord) 
            coord_two = bay_number*100 
            box_coordinates.append(coord_two) 
            box_coordinates.append(coord+75) 
            box_coordinates.append(coord_two+100) 
            coords_list.append([n,box_coordinates])    
            n += 1
        #make the map interface for the items
        create_customer_map(final_items_ordered, worded_locations, coords_list, all_items_list)
        
    def create_customer_map(item_ids, locations, coordinate_list, item_list):
        global map_window 
        #create map interface to show the customer where to go 
        map_window = Tk() 
        map_window.title("Shopping Journey Map") 
        map_window.geometry("1200x800") 
        map_canvas = Canvas(map_window, width = 1200, height = 800, bg = "white" ) 
        map_canvas.pack() 
        #draw the aisles 
        map_canvas.create_rectangle(100, 100, 175, 600, width=5) 
        map_canvas.create_rectangle(225, 100, 375, 600, width=5) 
        map_canvas.create_rectangle(425, 100, 575, 600, width=5) 
        map_canvas.create_rectangle(625, 100, 775, 600, width=5) 
        map_canvas.create_rectangle(825, 100, 975, 600, width=5) 
        map_canvas.create_rectangle(1025, 100, 1100, 600, width=5) 
        map_canvas.create_line(100, 200, 175, 200, width=5) 
        map_canvas.create_line(100, 300, 175, 300, width=5) 
        map_canvas.create_line(100, 400, 175, 400, width=5) 
        map_canvas.create_line(100, 500, 175, 500, width=5) 
        map_canvas.create_line(225, 200, 375, 200, width=5) 
        map_canvas.create_line(225, 300, 375, 300, width=5) 
        map_canvas.create_line(225, 400, 375, 400, width=5) 
        map_canvas.create_line(225, 500, 375, 500, width=5) 
        map_canvas.create_line(425, 200, 575, 200, width=5) 
        map_canvas.create_line(425, 300, 575, 300, width=5) 
        map_canvas.create_line(425, 400, 575, 400, width=5) 
        map_canvas.create_line(425, 500, 575, 500, width=5) 
        map_canvas.create_line(625, 200, 775, 200, width=5) 
        map_canvas.create_line(625, 300, 775, 300, width=5) 
        map_canvas.create_line(625, 400, 775, 400, width=5) 
        map_canvas.create_line(625, 500, 775, 500, width=5) 
        map_canvas.create_line(825, 200, 975, 200, width=5) 
        map_canvas.create_line(825, 300, 975, 300, width=5) 
        map_canvas.create_line(825, 400, 975, 400, width=5) 
        map_canvas.create_line(825, 500, 975, 500, width=5) 
        map_canvas.create_line(1025, 200, 1100, 200, width=5) 
        map_canvas.create_line(1025, 300, 1100, 300, width=5) 
        map_canvas.create_line(1025, 400, 1100, 400, width=5) 
        map_canvas.create_line(1025, 500, 1100, 500, width=5) 
        map_canvas.create_line(300, 100, 300, 600, width=5) 
        map_canvas.create_line(500, 100, 500, 600, width=5) 
        map_canvas.create_line(700, 100, 700, 600, width=5) 
        map_canvas.create_line(900, 100, 900, 600, width=5) 
        #text for the aisles 
        map_canvas.create_text((200, 350), text = '1') 
        map_canvas.create_text((400, 350), text = '2') 
        map_canvas.create_text((600, 350), text = '3') 
        map_canvas.create_text((800, 350), text = '4') 
        map_canvas.create_text((1000, 350), text = '5') 
        #draw the entrance 
        map_canvas.create_rectangle(100, 25, 200, 75, width=5) 
        #text for the entrance 
        map_canvas.create_text((150, 50), text = 'Entrance') 
        #colour the items' bays in red 
        for c in coordinate_list:            
            coords = c[1]            
            map_canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3], width=5, fill="red") 
        #add item numbers to the bays in red        
        sorted_items = []        
        for i in coordinate_list:            
            if i[0] not in sorted_items:                
                current_items = []                
                current_items.append(i[0])               
                sorted_items.append(i[0])               
                current_coords = i[1]                
                for n in range(len(coordinate_list)):                   
                    if coordinate_list[n][1] == i[1] and coordinate_list[n][0] not in current_items and sorted_items:                       
                        current_items.append(coordinate_list[n][0])                       
                        sorted_items.append(coordinate_list[n][0])                
                print(current_items)               
                x_pos = i[1][0] + 20               
                y_pos = i[1][1] + 25                
                map_canvas.create_text((x_pos,y_pos), text=current_items) 
        #create the text  
        map_canvas.create_text((50, 630), text="Shopping List:")        
        map_canvas.create_text((400, 630), text="Item Locations:")
        #show the shopping list 
        shopping_list = Listbox(map_window, width=30) 
        list_window = map_canvas.create_window(200, 700, window=shopping_list)        
        n = 1        
        for item in item_list: 
            shopping_list.insert(END,str(n)+". "+item) 
            n += 1       
        #show the location list            
        location_list = Listbox(map_window, width=30) 
        list_window = map_canvas.create_window(550, 700, window=location_list)         
        n = 1       
        for location in locations: 
            location_list.insert(END,str(n)+". "+location) 
            n += 1           
        #buttons 
        close = Button(map_window, text="Close map", command=map_window.destroy) 
        button_window = map_canvas.create_window(800, 700, window=close) 
        mainloop()
        
    #if there is less than 3 items in the list, do not run the pathfinder, just show the location for each item. 
    if len(shopping_list) <= 2: 
        items, distances, adjacents = create_graph(shopping_list) 
        final_items_ordered = items 
    #if there more than 2 items, a solution can be found using nearest neighbor 
    else:  
        final_items, final_adjacents, route_index = nearest_neighbor(shopping_list) 
        final_items_ordered = final_route_nn(final_items, final_adjacents, route_index) 
    #display that route to the customer 
    print("final route: ",final_items_ordered) 
    customer_map(final_items_ordered) 
 

#interface initialise 
window = Tk() 
window.title("Supermarket Pathfinder") 
window.geometry("200x200") 
#initial buttons to call customer and manager functions 
customer_button = Button(window, text="Customer", padx=30, pady=10, command=create_list).pack() 
manager_button = Button(window, text="Manager", padx=30, pady=10, command=login).pack() 
mainloop() 