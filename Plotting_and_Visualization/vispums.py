#Assignment Information
print("Data 51100 - Spring 2020")
print("Kelvin Tiongson")
print("Programming Assignment #6")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# read in file to DataFrame
input_file = 'ss13hil.csv'
df = pd.read_csv(input_file)

fig = plt.figure(figsize=(15,10))

# Top left Plot (Pie chart of languages)
plot11 = fig.add_subplot(2, 2, 1)
plot11.pie(df['HHL'].value_counts(),startangle=242.5,radius=.4)
plot11.legend(['English Only','Spanish','Other Indo-European',\
'Asian and Pacific Island languages','Other'], loc='upper left')
plot11.set_ylabel('HHL')
plot11.set_title('Household Languages')
plot11.axis('equal')

# Top right Plot (Histogram of Household Income)
plot12 = fig.add_subplot(2, 2, 2)
df['HINCP'].dropna().plot.kde()
plot12.hist(df['HINCP'].dropna(),
    bins=np.logspace(np.log10(10.0),np.log10(10000000.0), 100),
    #density=True,    # This line works for new versions  (switch as needed)
    normed=True,    # This line works for older versions  
    color='#7FBF7F'
)

plot12.set_xscale("log")
plot12.lines[0].set_linestyle("--")
plot12.lines[0].set_color("black")
plot12.title.set_text('Distribution of Household Income')
plot12.set_xlabel('Household Income ($) - Log Scaled')
plot12.set_ylabel('Density')

# Bottom left Plot ( Bar chart )
plot21 = fig.add_subplot(2, 2, 3)
sums = df['WGTP'].groupby(df['VEH']).sum()/1000

plot21.bar(range(len(sums)),sums,color='red')
plot21.set_ylabel('Thousands of Households')
plot21.set_xlabel('# of Vehicles')
plot21.set_title('Vehicles Available in Households')

# Bottom right Plot ( )
plot22 = fig.add_subplot(2, 2, 4)
taxp_values_dict = {1:0,2:1,3:50,4:100,5:150,6:200,7:250,8:300,9:350,10:400,
11:450,12:500,13:550,14:600,15:650,16:700,17:750,18:800,19:850,20:900,21:950,
22:1000,23:1100,24:1200,25:1300,26:1400,27:1500,28:1600,29:1700,30:1800,
31:1900,32:2000,33:2100,34:2200,35:2300,36:2400,37:2500,38:2600,39:2700,
40:2800,41:2900,42:3000,43:3100,44:3200,45:3300,46:3400,47:3500,48:3600,
49:3700,50:3800,51:3900,52:4000,53:4100,54:4200,55:4300,56:4400,57:4500,
58:4600,59:4700,60:4800,61:4900,62:5000,63:5500,64:6000,65:7000,66:8000,
67:9000,68:10000 }

df['TAXP_DERIVED'] = df['TAXP'].dropna().apply(lambda x:taxp_values_dict[x])

sp = plot22.scatter(df['VALP'],df['TAXP_DERIVED'],s=df['WGTP'],marker='o',\
c=df['MRGP'],cmap=plt.cm.get_cmap('bwr',20),alpha=.5)
plot22.set_xlim([0,1200000])
plot22.set_ylim(
ymin=0     # versions < matplotlib 3.2
#bottom=0  # version >= matplotlib 3.2
)
plot22.set_ylabel('Taxes ($)')
plot22.set_xlabel('Property Value ($)')
plot22.set_title('Property Taxes vs Property Values')

cb = plt.colorbar(sp)
cb.ax.set_ylabel('First Mortgage Payment (Monthly $)')

# This will allow some spacing between the subplots
fig.tight_layout(pad=3.0)

# Show the plots
plt.show()

# Save the plots
plt.savefig('pums.png')