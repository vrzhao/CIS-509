# -*- coding: utf-8 -*-
"""
@author: hina
"""
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot

# Read the data from the amazon-books.txt;
# populate amazonProducts nested dicitonary;
# key = ASIN; value = MetaData associated with ASIN
fhr = open('./amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
amazonBooks = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip() 
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['SalesRank'] = int(cell[5].strip())
    MetaData['TotalReviews'] = int(cell[6].strip())
    MetaData['AvgRating'] = float(cell[7].strip())
    MetaData['DegreeCentrality'] = int(cell[8].strip())
    MetaData['ClusteringCoeff'] = float(cell[9].strip())
    amazonBooks[ASIN] = MetaData
fhr.close()

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks[purchasedAsin]['Title'])
print ("SalesRank = ", amazonBooks[purchasedAsin]['SalesRank'])
print ("TotalReviews = ", amazonBooks[purchasedAsin]['TotalReviews'])
print ("AvgRating = ", amazonBooks[purchasedAsin]['AvgRating'])
print ("DegreeCentrality = ", amazonBooks[purchasedAsin]['DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks[purchasedAsin]['ClusteringCoeff'])
    
# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
# (1) YOUR CODE HERE: 
#     Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.

# get the depth-1 ego network and assign it to purchasedAsinEgoGraph
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph, purchasedAsin, radius=1)


# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# (2) YOUR CODE HERE: 
#     Use the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph

# create a list of edges which are tuples of two books and the weight between them
edges = []
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()

# Iterate through purchasedAsinEgoGraph for f t and e which are the two books and their weight respectively
for f, t, e in purchasedAsinEgoGraph.edges(data = True):
    # Check for to see if the weight exceeds the required threshold
    if e['weight'] >= threshold:
        # for edges that exceed the threshold add them to the purchasedAsinEgoTrimGraph and edges list.
        purchasedAsinEgoTrimGraph.add_edge(f,t,weight = e['weight'])
        edges.append([f,t,e['weight']])

# create a dictionary to contain the weights betwen the purchasedAsin and each other book that exceeded the threshold
weights = {}

# check for purchasedAsin in the edges, if found add the other book's 
# Asin and weight to the dictionary weights, setting the Asin as the dictonary key.
for n in edges:
    if(n[0] == purchasedAsin):
        weights[n[1]] = n[2]
    if(n[1] == purchasedAsin):
        weights[n[0]] = n[2]

# Next, recall that given the purchasedAsinEgoTrimGraph you constructed above, 
# you can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# (3) YOUR CODE HERE: 
#     Find the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, and assign it to purchasedAsinNeighbors

# Create a list of the neighbors of the purchasedAsin and put it into the list purchasedAsinNeighbors
purchasedAsinNeighbors = [i for i in purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)]

#answer = ['067187893X', '0694006246', '0688148999', '0399208534', '0399229191', 
#          '0399218858', '0808528858', '0805053883', '1581170769', '088708026X', 
#          '0064435962', '0688109942', '0152380116', '1929927266', '0152009981', 
#          '0694013013', '0152010661', '0399220496', '0399230130', '0399216596', 
#          '0152166084', '0399226907', '0060235152', '0698116453', '0399237720', 
#          '0399213015', '0399234276', '078570244X', '0152007717', '0399211667', 
#          '0399226842']
#
#print([i for i in purchasedAsinNeighbors if i in answer])


# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) YOUR CODE HERE: 
#     Note that, given an asin, you can get at the metadata associated with  
#     it using amazonBooks (similar to lines 49-56 above).
#     Now, come up with a composite measure to make Top Five book 
#     recommendations based on one or more of the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff. Feel free to compute
#     and include other measures. 


# create a list called ranks to hold the a list of all book ranks in amazonBooks
ranks = [0]*len(amazonBooks)

# iterate through amazonbooks by the key and insert the Sales rank into the list ranks on index j
j = 0
for i in amazonBooks.keys():
    ranks[j] = amazonBooks[i]['SalesRank']
    j = j + 1
    
# get the max rank and set the min to 1
Max = max(ranks)
Min = 1

# create a dictionary to hold each neighbors composite score recommendation score
neighbors = {}

# iterate through purchasedAsinNeighbors
for i in purchasedAsinNeighbors:
    
    # check to see if the TotalReviews are less than 1
    # if reviews are 0 than we give the book a reviewScore of 0
    if (amazonBooks[i]['TotalReviews'] < 1):
        reviewScore = 0
    # if TotalReviews are less than 10 but greater than 1 we give a reviewScore of 0.9
    # As the number of reviews are low, we are not confident that the average rating is correct
    # thus we reduce the value of the books average rating to 90%.
    elif (amazonBooks[i]['TotalReviews'] < 10):
        reviewScore = 0.9
    else:
        reviewScore = 1
    
    # here we scale the SalesRank to a score between a and b
    a = 0
    b = 0.5
    
    # if the Sales rank is 0 or less than we set the score to 0.
    if (amazonBooks[i]['SalesRank'] <= 0):
        rankScore = 0
    else:
        # This is a min max scalar function that takes books ranking and scales it between the limits a and b
        # We also inverted the salesRank so that books with a rank closer to 1 are given a higher score
        rankScore = (((b - a)*(Max - amazonBooks[i]['SalesRank']))/(Max - Min)) + a
    
    # We make a composite score calculated by multiplying the books average rating, reviewScore and weight together
    # rankScore is added additionally on the side, reconizing the value of popularity while not letting it dominate the recommendation score.    
    neighbors[i] = amazonBooks[i]['AvgRating'] * reviewScore * weights[i] + rankScore
    
    # if a book has a score of 0, we delete it from the neighbors list 
    # For the score to be 0, either the AvgRating or TotalReviews must be 0.
    # Thus we will not be recommending the book.
    if neighbors[i] == 0:
        del neighbors[i]

# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5) YOUR CODE HERE:  
    
    
# sort the neighbors in decending order based on the composite score previously calculated
rec = sorted(neighbors.items(), key = itemgetter(1), reverse = True)

# print the top 5 recommendations
print ('\n')
print ("Recommendations:")
print ("--------------------------------------------------------------")

# check to see if there are at least 5 recommendations. 
# If there are less than 5 neighbors, print all of them.
if(len(rec) < 5):
    for i in range(len(rec)):
        print ("ASIN = ", rec[i][0]) 
        print ("Title = ", amazonBooks[rec[i][0]]['Title'])
        print ("SalesRank = ", amazonBooks[rec[i][0]]['SalesRank'])
        print ("TotalReviews = ", amazonBooks[rec[i][0]]['TotalReviews'])
        print ("AvgRating = ", amazonBooks[rec[i][0]]['AvgRating'])
        print ("DegreeCentrality = ", amazonBooks[rec[i][0]]['DegreeCentrality'])
        print ("ClusteringCoeff = ", amazonBooks[rec[i][0]]['ClusteringCoeff'])
        print ('\n')
else:
    for i in range(5): 
        print ("ASIN = ", rec[i][0]) 
        print ("Title = ", amazonBooks[rec[i][0]]['Title'])
        print ("SalesRank = ", amazonBooks[rec[i][0]]['SalesRank'])
        print ("TotalReviews = ", amazonBooks[rec[i][0]]['TotalReviews'])
        print ("AvgRating = ", amazonBooks[rec[i][0]]['AvgRating'])
        print ("DegreeCentrality = ", amazonBooks[rec[i][0]]['DegreeCentrality'])
        print ("ClusteringCoeff = ", amazonBooks[rec[i][0]]['ClusteringCoeff'])
        print ('\n')
    

