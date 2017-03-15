import pandas as pd
import numpy as np
import math

# Define logistic Function to calculate probability of classifier (range 0 to 1) for normalized values of features. We start with zero values of shape of features which
# gives probability = 0.5 and as normalized values go positive we get higher probability(towards 1) and as we get normalized negative values of features we go towards negative
# probability. P = 1/(1 + e(-w.x)) w=vector of parameters and x=feature.
def logit_func(vector, features):
    return float(1) / (1 + math.e**(-features.dot(vector)))


# Define Cost Function to maximize the probability of classifier given the features. So we have to maximize the probability of insurance buyers(YES) which is product of probability
# of each obervation being YES. i.e P(1)*P(2)*P(3)...Similarly we have to maximize the probability of each obervation in the dataset to be not buying insurance(NO).
# i.e.(1 - P(1)*P(2)*P(3)...). So to maximize we can do summation of classifier*log(Product of Probabilities). In this case probability is logistic function.
def cost_func(vector, features, classifier):
    logit_func_x = logit_func(vector,features)
    x = classifier * np.log(logit_func_x)   #Positive probability tending towards YES
    y = (1-classifier) * np.log(1 - logit_func_x)  #Negative probability tending towards NO
    #Now We will try to minimize the negative which is equivalent to maximizing the positive.
    # J = -classifier*log(Product of probability) - (1 - classifier)*(1 - log(Product of probability))
    J = -x - y
    return np.mean(J)  #Summation of all the product of probabilities is done here.

# Define gradient descent function here, where we try to go to the minimum value on the negative probability side. For this we set our starting point 0.001 and limit as 0.001
# These values on the curves should be sufficient to get the minimum point we are trying to reach.
def gd_func(vector_values, features, classifier, start=.001, limit=.001):
    #To normalize the data for each feature ,we calculate the Z-score by subtracting the mean and dividing by standard deviation. Z=(X-X(Mean))/Std.Dev
    features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)
    #Create a dataframe for several points for each of the features on the curve.  We have to find out the minimum point in this gradient descent dataframe.
    gd = []
    cost = cost_func(vector_values, features, classifier)
    # Start with 0 on the X-axis for the features and cost on the Y-axis
    gd.append([0, cost])
    # Run this in loop until we reach the minimum gradient value.
    start_cost = 1
    i = 1
    while(start_cost > limit):         # When limit is reached the gradient reaches minimum and gradient curve almost becomes a straight line.
        old_cost = cost
        #On derivating by vector w and simplifying the cost function we can fairly say that gradient is gradient = (logistic function - classifier)*features
        vector_values = vector_values - (start * (logit_func(vector_values, features) - (classifier)).T.dot(features))
        cost = cost_func(vector_values, features, classifier)
        gd.append([i, cost])
        start_cost = old_cost - cost
        i+=1
    return vector_values #These are the minimum gradient values or weight of parameters for each feature so that it is minimized to negative

# Prediction model using logistic function.
def logit_model(vector, features):
    #To normalize the data for each feature ,we calculate the Z-score by subtracting the mean and dividing by standard deviation. Z=(X-X(Mean))/Std.Dev
    features = (features - np.mean(features, axis=0)) / np.std(features, axis=0)
    logit_prob = logit_func(vector, features)
    prob_predicted = np.where(logit_prob >= .5, 1, 0)  #If gradient values are greater than 0.5 the probability is 1 else 0.
    return prob_predicted

input_data = pd.read_csv('C:/Users/sanketn/Downloads/Train1.csv')
df = pd.DataFrame(input_data, columns = ['Segment', 'Region', 'Priority', 'Amount', 'Volume', 'Cycle_Time', 'Rating', 'Conclusion'])

features = df[['Amount', 'Volume', 'Cycle_Time', 'Rating']]
classifier = np.where(df['Conclusion'] == 'YES', 1, 0)

# Number of features on which we are doing the prediction
shape = features.shape[1]
# Create dataframe with 0 values for shape of the prediction features
betas = np.zeros(shape)

minimum_gradient_values = gd_func(betas, features, classifier)
print(minimum_gradient_values)

predicted_classifier = logit_model(minimum_gradient_values, features)
print predicted_classifier