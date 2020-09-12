#Variables holding our file names
input_file = "prog2-input-data.txt"
output_file = "prog2-output-data.txt"

#Assignment Information
def print_initial_stmt():
    print("Data 51100 - Spring 2020")
    print("Group 5")
    print('Student Name: Kelvin Tiongson')
    print("Programming Assignment #2")

def print_clusters(clusters):
    for c in clusters:
        print(c,clusters[c])


def print_point_assignments(data,point_assignments):
    for p in data:
        print("Point",p,"in cluster",point_assignments[p])


# Funtion to open a new file and write the output.
def point_assignments_to_file(data,point_assignments,output_file):
    f = open(output_file, "w")
    for p in data:
        f.write("Point "+str(p)+" in cluster "+str(point_assignments[p])+"\n")
    f.close()


#Funtion to read and print the generated output file. 
def read_output_file():
    print ('Output File Contents')
    print ('--------------------')
    file = open(output_file, "r")
    print ('Read the data from outputfile: {} \n'.format(output_file))
    print (file.read())


def assign_to_clusters(data,clusters,centroids,point_assignments):
    # Iterate over the centroids and compare to data points
    for i in range(len(data)):
        closestCentroid = abs(centroids[0]-data[i])
        closestCentroidCluster = 0
        for n in range(len(clusters)):
            if abs(centroids[n]-data[i]) < closestCentroid:
                closestCentroid = abs(centroids[n]-data[i])
                closestCentroidCluster = n
                
        # Assign data point to proper cluster, i.e., cluster with closest
        # distanced centroid
        point_assignments[data[i]] = closestCentroidCluster
        clusters[closestCentroidCluster].append(data[i])


def compute_centroids(centroids,clusters):
    for n in range(len(clusters)):
        centroids[n] = sum(clusters[n])/len(clusters[n])


# Read in information before interacting with user as there is no point
# in interacting with our user if there is an issue with the file
data = [float(line.rstrip()) for line in open(input_file)]


print ('\n')
print ('Output')
print ('------')

print_initial_stmt()

print ('\n')
# get the amount of clusters from the user
k = int(input("Enter the number of clusters: "))

# initialize our centroids
centroids = dict(zip(range(k),data[0:k])) 

# initialize our working space for the clustering process
clusters = dict(zip(range(k),[[] for i in range(k)]))
old_point_assignments = { i : 0 for i in data }
point_assignments = { i : 0 for i in data }

# this will count the iteration number for output purposes
iteration = 1

# emulated do/while loop
while True:

    print("Iteration ",iteration)
    
    # Process the (re)assignment of clusters
    assign_to_clusters(data,clusters,centroids,point_assignments)
     
    # just seeing values per iteration            
    print_clusters(clusters)
    
    # Assess whether all values stayed in their previous clusters
    if old_point_assignments == point_assignments:
        break # since there will be no more new changes to the clusters
    else: # recompute the centroids for the next pass of reclustering
        old_point_assignments = dict(point_assignments) # shallow copy
    
        # compute the centroid (arithmetic mean) per cluster
        compute_centroids(centroids,clusters)
        
        # reinitialize
        clusters = dict(zip(range(k),[[] for i in range(k)])) 
    
    iteration = iteration + 1
print ('\n')    
print_point_assignments(data,point_assignments)
print ('\n')  
point_assignments_to_file(data,point_assignments,output_file)   
read_output_file()

