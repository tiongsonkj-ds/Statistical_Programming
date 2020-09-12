# =============================================================================
# Kelvin Tiongson
# 2/23/2020
# DATA-51100: Statistical Programming
# Spring 2020
# Programming Assignment 5 - Data Preparations and Statistics
# =============================================================================

print("DATA-51100, Spring 2020")
print("NAME: Kelvin Tiongson")
print("PROGRAMMING ASSIGNMENT #5\n")
      
import pandas as pd
import re

cps_path = 'cps.csv'
cps = pd.read_csv(cps_path)

# generate new dataframe with 9 specific columns requested
new_df = cps.loc[:, ['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total', 'College_Enrollment_Rate_School']]

# grab the lowest (class) grade
def get_lowest_grade(row):
    if ('PK') in row:
        return 'PK'
    elif ('K') in row:
        return 'K'
    else:
        split_row = row.split(',')
        integer_row = [int(x) for x in split_row]
        return str(min(integer_row))
    
# grab the highest (class) grade
def get_highest_grade(row):
    split_row = row.split(',')
    if (len(split_row) == 1):
        return row
    else:
        integer_row = [int(x) for x in split_row if x.isdigit()]
        return str(max(integer_row))

# grab School_Start_Hour
def get_starting_hour(row):
    if (row):
        times = re.findall(r'\d{1,2}(?:(?:am|pm)|(?::\d{1,2})(?:am|pm)?)', row)

        if len(times) == 0:
            split_row = row.split(' ')
            hour = split_row[0]
            if (not hour.isdigit()):
                numbers = [x for x in split_row if re.search(r'\d', x)]
                for element in numbers[0]:
                    if element.isdigit():
                        return int(element)
            else:
                return int(hour)
        else:
            starting_hour = times[0].split(':')[0]
            return int(starting_hour)

    


lowest_grade_col = cps['Grades_Offered_All'].apply(get_lowest_grade)
highest_grade_col = cps['Grades_Offered_All'].apply(get_highest_grade)
new_df['Lowest_Grade_Offered'] = lowest_grade_col
new_df['Highest_Grade_Offered'] = highest_grade_col

start_hour = cps['School_Hours'].fillna(0).apply(get_starting_hour)
start_times_8 = start_hour[start_hour == 8]
start_times_7 = start_hour[start_hour == 7]
start_times_9 = start_hour[start_hour == 9]

new_df['School_Start_Hour'] = start_hour.fillna(0)
new_df['School_Start_Hour'] = new_df['School_Start_Hour'].astype('int64')

# check which columns are null
check_cols_with_missing_data = new_df.isna().any()
# grab all columns that have missing data
cols_with_missing_data = check_cols_with_missing_data[check_cols_with_missing_data == True]
# fill in missing column data with mean
for col in cols_with_missing_data.index:
    mean_of_cols = new_df[col].mean()
    new_df = new_df.assign(College_Enrollment_Rate_School=new_df[col].fillna(mean_of_cols))
    
# display the first 10 rows of the DataFrame
first_ten = new_df[:10]
# set school id as index
school_id_index_df = first_ten.set_index(['School_ID'])
print(school_id_index_df.to_string())
print('')

# mean and standard deviation of college enrollment rate for high schools
# print out rows that are high schools
is_high_school_df = new_df[new_df['Is_High_School'] == True]
is_high_school_mean = is_high_school_df['College_Enrollment_Rate_School'].mean()
is_high_school_std = is_high_school_df['College_Enrollment_Rate_School'].std()
is_high_school_template = 'College Enrollment Rate for High Schools = {0:.2f} (sd={1:.2f})'
print(is_high_school_template.format(is_high_school_mean, is_high_school_std))
print('')

# mean and std of student counts for non high schools
is_not_high_school_df = new_df[new_df['Is_High_School'] == False]
student_count_total_mean = is_not_high_school_df['Student_Count_Total'].mean()
student_count_total_std = is_not_high_school_df['Student_Count_Total'].std()
is_not_high_school_template = 'Total Student Count for non-High Schools = {0:.2f} (sd={1:.2f})'
print(is_high_school_template.format(student_count_total_mean, student_count_total_std))

# print School_Start_Hour distribution times
print('\nDistribution of School_Start_Hours')
print('8am: ', start_times_8.count())
print('7am: ', start_times_7.count())
print('9am: ', start_times_9.count())
print('')

# number of schools outside of the loop neighborhood
zip_values = new_df['Zip'].value_counts()
loop = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60616]
outside_loop = [x for x in zip_values.index if x not in loop]
num_schools_out_of_loop = zip_values[outside_loop].sum()
print('\nNumber of schools outside the Loop: ', num_schools_out_of_loop)