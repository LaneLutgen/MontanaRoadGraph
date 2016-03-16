"""
Lane Lutgen
CSCI 305 
Lab #2

***USING PYTHON 3.5***

NOTES: Need to finish processing input, currently at option == 3
"""


import re
import sys

"""
This def is responsible for providing instructions to the user
when the program is first executed after the graphs are created.
It can be called multiple times by process_input if the user wants to perform multiple tasks
"""
def begin_program():
	print ("Welcome to the Montana Road Network")
	print ("Enter 1 to find to find total number of connections for a given city")
	print ("Enter 2 to determine if two cites are directly connected")
	print ("Enter 3 to determine k-hop connections between cities")
	print ("Enter 4 to determine any non-direct connections between cities")
	print ("Enter any other value to exit")

	option = input()

	process_input(int(option))

"""
This def will always be called by begin_program, it takes in an integer value
that represents the user's choice of what task they want to perform on the 
map database 
"""
def process_input(option):
	if option == 1:
		city = input("Please enter the name of the city: ")
		print(city," has ", get_number_of_connections(city), "total conections.")
	elif option == 2:
		start_city = input("Please enter starting location: ")
		destination = input("Please enter destination: ")
		connection = is_connected(start_city, destination)
		if connection == True:
			print ("Direct connection found!")
		else:
			print ("No direct connection was found")
	elif option == 3:
		start_city = input("Please enter starting location: ")
		destination = input("Please enter destination: ")
		hops = input("Please enter maximum number of city connections (k-hops): ")
		k_hop = has_khop_connection(start_city, destination, hops)
		if k_hop == True:
			print (hops, "-hop connection was found.")
		else:
			print (hops, "-hop connection was not found")
	elif option == 4:
		start_city = input("Please enter starting location:")
		destination = input("Please enter destination:")
		connected = has_connection(start_city, destination)
		if connected == True:
			print ("Indirect connection found!")
		else:
			print ("Connection was not found")
	else:
		print("Goodbye")
		sys.exit()


	go_again = input("Would you like to try something else? Y/N\n")
	if go_again == "Y" or go_again == "y":
		begin_program()
	else:
		process_input("N")

"""
Reads the text file provided and creates a dictionary to be used
as an adjacency matrix that represents the graph data structure.
This def is run before user input is taken.
"""
def create_dictionary():
	with open("city1.txt") as city_file:
		from_word = "From"
		to_word = "To"
		miles_word = "Miles"
		for line in city_file:	
			words = re.split(r'\s{2,}', line)
			pointer = 0 #keep track of FROM, TO, and MILES FIELD
			for word in words:
				if len(words) == 1:
					break
				if pointer == 0:
					if word != "From" and from_word != word:
						from_word = word				
						dictionary[from_word] = {}
						graph[from_word] = set()
						#print (from_word)
					pointer = 1
				elif pointer == 1:
					if word != "To":
						to_word = word
						graph[from_word].add(to_word)
						#print (to_word)
					pointer = 2
				elif pointer == 2:
					if word != "Miles":
						miles_word = word
						if from_word != "From":
							dictionary[from_word][to_word] = miles_word
						#print (miles_word)
					pointer = 3
				else:
					pointer = 0


"""
Takes in a start location and finish location string and returns the 
distance between those cities if a direct connection exists.
"""
def find_distance(start, finish):
	try:
		return int(dictionary[start][finish])
	except:
		return 0

"""
Determines if there is a direct connection between two cities represented by
string inputs. If there is a value stored in the dictionary for the two city
keys, then the connection exists, if we get a KeyError, that means that the connection
does not exist.
"""
def is_connected(start, finish):
	try:
		dist = int(dictionary[start][finish])
		if dist >= 0:
			return True
		else:
			return False
	except:
		return False

"""
Takes in a city and determines the total number of connections to that given
city within the database. This includes both incoming and outgoing connections
"""
def get_number_of_connections(city):
	count = len(dictionary[city])
	for start in dictionary:
		#print (start)
		try:
			dist = dictionary[start][city]
			#print (dist)
			if int(dist) > 0:
				count = count +1
		except:
			pass
	return count

"""
Depth-first search algorithm. Takes in an adjacency list representation of a graph
as well as the desired start and finish destinations. Returns a set representation of
all the possible paths between the start and the finish destinations.
"""
def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

"""
Determines if there exists a k-hop connection between a start and finish destination, 
where k <= d. If the k-hop connection exists, one of the paths will be printed out as
well as the total distance.
"""
def has_khop_connection(start, finish, d):
	all_paths = list(dfs_paths(graph, start, finish))
	for l in all_paths:
		length = len(l)
		if length <= int(d):
			print_total_distance(l)
			return True
	return False

"""
Determines if there is a connection between two cities start and finish both direct
and indirect. If a direct or indirect connection is found, the path and the total 
distance will be printed out.
"""
def has_connection(start, finish):
	all_paths = list(dfs_paths(graph, start, finish))
	for l in all_paths:
		length = len(l)
		if length == 0:
			return False
		else:
			print_total_distance(l)
			return True

"""
Takes in a path, prints it, and then prints the total distance of that path. This is called
by both has_khop_connection and has_connection.
"""
def print_total_distance(path):
	print ("Path ", path)
	total_distance = 0
	for i in range(0, (len(path) - 1)):
		j = i + 1
		total_distance = total_distance +int(dictionary[path[i]][path[j]])
	print ("Total Distance ", total_distance)



"""
BEGIN PROGRAM
"""
dictionary = {} #adjacency matrix representation of the graph
graph = {} #adjacency list representation of the graph
create_dictionary() #reads the text file and creates the dictionary
begin_program() #begins the program and takes in user input


"""
TEST CODE
"""
#print (dictionary)
#d = find_distance("Bozeman", "Butte")
#d = get_number_of_connections("Bozeman")
#d = is_connected("Bozeman", "Butte")
#print ("Number: ",d)
#print (list(dfs_paths(graph, "Bozeman", "Ryegate")))
#print(has_connection("Bozeman", "Hysham"))
#print (d)
#graph={0:[1,2],1:[2],2:[0,3],3:[3]}