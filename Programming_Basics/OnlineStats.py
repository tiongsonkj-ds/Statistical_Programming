# =============================================================================
# Kelvin Tiongson
# 1/19/2020
# DATA-51100: Statistical Programming
# Spring 2020
# Programming Assignment 1 - Online Descriptive Statistics
# =============================================================================

print("DATA-51100, Spring 2020")
print("NAME: Kelvin Tiongson")
print("PROGRAMMING ASSIGNMENT #1")

numbers = []
first_display = 'Mean is %.2f and Variance is 0'
display = 'Mean is %.2f and Variance is %.6f'

# mean after n − 1th value was entered
mean = 0
# variance after n - 1th value was entered
variance = 0
# updated mean after nth value was entered
updated_mean = 0
# updated variance after nth value was entered
updated_variance = 0

# ask user for the input
user_input = int(input("Enter a number: "))
while user_input >= 0:
    # add user input to the list of numbers
    numbers.append(user_input)

    # num of values entered
    n = len(numbers)
    
    # calculate updated mean using the formula
    updated_mean = mean + ((user_input - mean)/n)
    
    # calculate updated variance using the formula (if n > 1)
    if n > 1:
        updated_variance = (((n - 2)/(n - 1)) * variance) + (((user_input - mean)**2)/n)

    # logging the mean and variance (if n > 1)
    # changing the stored value of the mean and the variance (if n > 1)
    if n == 1:
        print(first_display % (updated_mean))
        mean = user_input
    else:
        print(display % (updated_mean, updated_variance))
        mean = updated_mean
        variance = updated_variance
    
    # ask for new input
    user_input = int(input("Enter a number: "))