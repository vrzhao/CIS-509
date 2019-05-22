# -*- coding: utf-8 -*-
"""
Assignment
"""

# you must NOT import or use any other packages or modules besides these
import math
from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is expected in the form of a nested dictionary:
    # at the top level, it has User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
    def __init__(self, usersItemRatings, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            

    #################################################
    # calcualte the pearson correlation between two item ratings dictionaries userXItemRatings and userYItemRatings
    #
    # userXItemRatings and userYItemRatings data is expected in the form of dictionaries of item ratings
    # Example:
    #      userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    #      userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    #
    # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        # (1) YOUR CODE HERE
        
        # create 6 variables to hold the values required for calculating the pearson correlation with a single loop
        n = 0
        x = 0
        x2 = 0
        y2 = 0
        y = 0
        xy = 0
               
        # iterate through the item ratings on common keys and record the ratings
        for i in userXItemRatings.keys():
            if i in userYItemRatings:
                n = n + 1
                x = x + userXItemRatings[i] 
                x2 = x2 + userXItemRatings[i]**2 
                y = y + userYItemRatings[i] 
                y2 = y2 + userYItemRatings[i]**2 
                xy = xy + userXItemRatings[i]*userYItemRatings[i]
        
        # error check #1
        if n == 0:
            return -2
        
        # calculate the denominator for the pearson correlation
        denom = math.sqrt(x2-(x**2)/n)*math.sqrt(y2-(y**2)/n)
        
        # error check #2
        if denom == 0:
            return -2
        
        # calculate the numorator for the pearson correlation
        numor = xy - (x*y)/n
        
        # return the pearson correlation
        return numor/denom
    
        # Things to keep in mind as you code this section:
        # (a) this method must calcualte and return the pearson correlation between the two given dictionaries of items ratings.
        # (b) the number, names, or format of the input parameters to this method must NOT be changed.
        # (c) the method must use the computationally efficient form of pearson correlation to calucalte the pearson correlation
        # (d) the method must use only a total of 1 for loop to calcualte the pearson correlation
        # (e) the method must compute the value of n as the number of common keys in the dictionaries 
        # (f) the method must perform the following error checks:
        #     if n=0, return value of -2
        #     if the denominator of the pearson correlation=0, return value of -2
        # (g) if neither of the error conditions in (f) occured, return the pearson correlation

    #################################################
    # make recommendations for userX from the k most similar nearest neigibors (NNs)
    # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
    
    def recommendKNN(self, userX):
        
        # (2) YOUR CODE HERE
        
        # create dictionaries to hold the user correlations and normalized user correlations
        pearson = dict()
        pearsonNormal = dict()
        
        # for userY not equal to userX, call the pearsonFn function to find the correlation between them
        for userY in self.usersItemRatings.keys():
            if(userY != userX):
                # record the resulting correlation in dictionary pearson
                pearson[userY] = self.pearsonFn(self.usersItemRatings[userX], self.usersItemRatings[userY])
                
                # delete the value if it is an error, otherwise store the normalized version in dictionary pearsonNormal
                if pearson[userY] == -2:
                    del pearson[userY]
                else:
                    pearsonNormal[userY] = (pearson[userY]+1)/2
        
        # create a dictionary to hold the recommendations and their scores
        recommendations = dict()
        
        # create list of sorted tuples in decending order based on the correlation between userX and other other users
        pearsonSorted = sorted(pearsonNormal.items(), key = lambda x: x[1], reverse = True)
        
        # check if there are at least k items in ps, if lenght of ps is less than k, replace k with length of ps
        if len(pearsonSorted) < self.k:
            self.k = len(pearsonSorted)
        
        # create a list to hold the weights for recomendations 
        weight = [0]*self.k
        denom = 0
        
        # iterate through the top k users to calculate the denominator used to calculte the weights
        for i in range(0,self.k):
            denom = denom + pearsonSorted[i][1]
            
        # iternate again to calculate the weights for recommendation score prediction
        for i in range(0,self.k):
            weight[i] = pearsonSorted[i][1]/denom
        
        
        # iterate through the item ratings for userX and the top k correlated users to get the recommended items and their predicted scores
        for j in range(0, self.k):
            for i, l in self.usersItemRatings[pearsonSorted[j][0]].items():
                if i not in self.usersItemRatings[userX]: 
                    if i in recommendations:
                        recommendations[i] = recommendations[i] + l*weight[j]
                    else:
                        recommendations[i] = l*weight[j]
        
        # create a new dict that will hold the recommendations with scores rounded to two decimal places
        recommendationRounded = dict()
        
        # round the recommendations scores to two decimal places
        for i in recommendations.keys():
            recommendationRounded[i] = round(recommendations[i],2)
        
        recommendationSorted = sorted(recommendationRounded.items(), key = itemgetter(1), reverse = True)

        # return the recommendations and scores
        return recommendationSorted

        # Things to keep in mind as you code this section:
        # (a) this method must calcualte and return the recommendations for userX from the k most similar nearest neighbors
        # (b) the number, names, or format of the input parameters to this method must NOT be changed
        # (c) the method must use self.usersItemRatings (set during class object instantiation) to get the other users and their item ratings
        # (d) the method must use self.k (set during class object instantiation) to get the value of k
        # (e) the method must use the PearsonFn method defined in this class to calcualte similarity
               
        # Steps you might want to follow as you code this section:
        # (a) first, for given userX, get the sorted list of users - by most similar to least similar:
        #     - remember to exclude simialrity of user from himself 
        #     - remember to exclude any users with similarity of -2 (since that means error condition) 
        # (b) then, calcualte the weighted average item recommendations for userX from userX's k NNs
        # (c) then, return sorted list of recommendations (sorted highest to lowest ratings)
        #     example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]


        
