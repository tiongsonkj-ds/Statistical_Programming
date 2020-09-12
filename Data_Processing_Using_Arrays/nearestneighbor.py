# =============================================================================
# Kelvin Tiongson
# 2/9/2020
# DATA-51100: Statistical Programming
# Spring 2020
# Programming Assignment 3 - Nearest Neighbor Classification
# =============================================================================

print("DATA-51100, Spring 2020")
print("NAME: Kelvin Tiongson")
print("PROGRAMMING ASSIGNMENT #3")

# numpy
import numpy as np

# load files of training example
testing_path = 'iris-testing-data.csv'
training_path = 'iris-training-data.csv'

testing_attributes = []
testing_class_labels = []
# reading each line of the testing data
test_data = [line.rstrip() for line in open(testing_path)]

# going through each line of the testing data
# splitting each line to separate attributes and class labels
for line in test_data:
    split_line = line.split(',')
    testing_attributes.append(split_line[:4])
    testing_class_labels.append(split_line[-1])

# creating the 2d ndarray for attributes and turning into a float
test_attr_ndarr = np.array(testing_attributes).astype(float)
# creating a 1d ndarray for training class labels
test_class_labels_ndarr = np.array(testing_class_labels)

# do the same thing with the training data
training_attributes = []
training_class_labels = []
train_data = [line.rstrip() for line in open(training_path)]

for line in train_data:
    split_line = line.split(',')
    training_attributes.append(split_line[:4])
    training_class_labels.append(split_line[-1])

train_attr_ndarr = np.array(training_attributes).astype(float)
train_class_labels_ndarr = np.array(training_class_labels)


# subtract everything from test array with train array
subtr_attr = test_attr_ndarr[:,np.newaxis] - train_attr_ndarr

# squares each value in the subtracted array
squared_attr = np.square(subtr_attr)

# sums everything in the second column, which was each row of squared values
sum_attr = np.sum(squared_attr, 2)

# gives the square root of each value
sqrt_attr = np.sqrt(sum_attr)

# find the min value of each row
smallest_value_per_row = np.argmin(sqrt_attr, axis=1)

# new list where each element is the training class with that smallest distance
closest_training_label = [training_class_labels[i] for i in smallest_value_per_row]

# print testing example classification
print('\n#, True, Predicted')
num_of_accurate = 0
for i in range(len(testing_class_labels)):
    row = i + 1
    row_template = '{0:s},{1:s},{2:s}'
    print(row_template.format(str(row), testing_class_labels[i], closest_training_label[i]))
    if (testing_class_labels[i] == closest_training_label[i]):
        num_of_accurate += 1
        
# calculate accuracy
accuracy = (num_of_accurate / len(testing_class_labels)) * 100
accuracy_template = 'Accuracy: {0:.2f}%'
print(accuracy_template.format(accuracy))
