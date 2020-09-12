# =============================================================================
# Kelvin Tiongson
# 3/7/2020
# DATA-51100: Statistical Programming
# Spring 2020
# Programming Assignment 7 - Aggregating ACS PUMS Data
# =============================================================================

print("DATA-51100, Spring 2020")
print("NAME: Kelvin Tiongson")
print("PROGRAMMING ASSIGNMENT #7\n")
      
import pandas as pd

# load csv
input_file = 'ss13hil.csv'
df = pd.read_csv(input_file)

# expand col width for table 1
pd.set_option('max_colwidth', 70)

# Table 1
print('*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***')
hincp_hht = df['HINCP'].groupby(df['HHT'])
described_sorted_values = hincp_hht.describe().sort_values(by=['mean'], ascending=False)
described_sorted_values.index.names = ['HHT - Household/family type']
table1_cols = described_sorted_values[['mean', 'std', 'count', 'min', 'max']]
table1_index = {
        1: 'Married couple household',
        2: 'Other family household:Male householder, no wife present',
        3: 'Other family household:Female householder, no husband present',
        4: 'Nonfamily household:Male householder:Living alone',
        5: 'Nonfamily household:Male householder:Not living alone',
        6: 'Nonfamily household:Femaile householder:Living alone',
        7: 'Nonfamily household:Female householder:Not living alone'
}
table1 = table1_cols.rename(index=table1_index)
print(table1.to_string())


# Table 2
print('\n*** Table 2 - HHL vs. ACCESS - Frequency Table ***')
print('                                             sum')
print('                                            WGTP')
cleaned_df = df.loc[:, ['HHL', 'ACCESS', 'WGTP']].dropna()
hhl_crosstab = pd.crosstab(
        cleaned_df['HHL'],
        cleaned_df['ACCESS'],
        values=cleaned_df['WGTP'],
        aggfunc='sum',
        normalize='all',
        margins=True
)
table2 = hhl_crosstab.applymap(lambda x: '{0:.2f}%'.format(x*100))
table2.columns = ['Yes w/ Subsrc.', 'Yes, w/o Subsrc.', 'No', 'All']
table2.index = [
    'English only',
    'Spanish',
    'Other Indo-European languages',
    'Asian and Pacific Island languages',
    'Other language',
    'All'
]
table2.columns.name = 'ACCESS'
table2.index.name = 'HHL - Household language'
print(table2)


# Table 3
print('\n*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***')
quant_analysis = pd.qcut(df['HINCP'].dropna(), 3)
def get_stats(group):
    rows = group.index.values
    group.household_count = df['WGTP'][rows].sum()
    return {
        'min': '{0:.0f}'.format(group.min()),
        'max': '{0:.0f}'.format(group.max()),
        'mean': '{0:.6f}'.format(group.mean()),
        'household_count': group.household_count
    }

grouped_qa = df['HINCP'].dropna().groupby(quant_analysis)
table3 = grouped_qa.apply(get_stats).unstack()
table3_index = [
    'low',
    'medium',
    'high'
]
table3.index = table3_index
table3.index.name = 'HINCP'
print(table3)
    
