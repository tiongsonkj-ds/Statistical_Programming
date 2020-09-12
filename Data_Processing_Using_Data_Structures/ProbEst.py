# =============================================================================
# Kelvin Tiongson
# 2/16/2020
# DATA-51100: Statistical Programming
# Spring 2020
# Programming Assignment 4 - Estimating Probabilities
# =============================================================================

print("DATA-51100, Spring 2020")
print("NAME: Kelvin Tiongson")
print("PROGRAMMING ASSIGNMENT #4")
print('')

import pandas as pd

# load cars csv file into a pandas DataFrame
cars = pd.read_csv('cars.csv')
rows = cars.shape[0]

# unique values of make and probabilities
makes = cars['make']
unique_make = makes.unique()
prob_make = makes.value_counts() / rows

# creates a new dataframe that has prob(asp && make)
def calc_prob_asp_given_make():
    dataframe = pd.DataFrame()
    for make in unique_make:
        specific_car = cars[cars['make'] == make]
        prob_make_std = specific_car[specific_car['aspiration'] == 'std'].shape[0] / rows
        prob_make_turbo = specific_car[specific_car['aspiration'] == 'turbo'].shape[0] / rows
        new_list = [prob_make_std, prob_make_turbo]
        new_frame = pd.DataFrame(new_list, columns=[make], index=['std','turbo'])
        dataframe = dataframe.append(new_frame.T)
    return dataframe

# create cond prob dataframe
def calc_cond_prob(prob_asp_given_make):
    df = pd.DataFrame()
    for make in unique_make:
        cond_prob_std = prob_asp_given_make.loc[make]['std'] / prob_make[make]
        cond_prob_turbo = prob_asp_given_make.loc[make]['turbo'] / prob_make[make]
        cond_prob_list = [cond_prob_std, cond_prob_turbo]
        new_frame = pd.DataFrame(cond_prob_list, columns=[make], index=['std','turbo'])
        df = df.append(new_frame.T)
    return df

def get_make_probabilities(make):
    prob = prob_make[make] * 100
    template = 'Prob(make={0:s}) = {1:.2f}%'
    return template.format(make, prob)

prob_asp_given_make_df = calc_prob_asp_given_make()
cond_prob_df = calc_cond_prob(prob_asp_given_make_df)
# go through each value, and print out the row with index and then display it as a percentage
for make in unique_make:
    row = cond_prob_df.loc[make]
    std = row['std'] * 100
    turbo = row['turbo'] * 100
    std_template = 'Prob(aspiration=std|make={0:s}) = {1:.2f}%'
    turbo_template = 'Prob(aspiration=turbo|make={0:s}) = {1:.2f}%'
    print(std_template.format(make, std))
    print(turbo_template.format(make, turbo))

print('')
# print out prob of each make
for make in unique_make:
    print(get_make_probabilities(make))
