# -*- coding: utf-8 -*-
import pandas as pd
df1 = pd.read_csv('religion.csv', sep=';', encoding = 'unicode_escape')
df2 = pd.read_csv('State Populations.csv', sep = ',')
df = pd.merge(df1, df2, how='inner', on = 'State')
df['Pop. density'] = (df['2018 Population'] / df['Square kilometers'])
print(df)
StateNames = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut", "District of Colombia", "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
StateAbb = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

df["StateAbb"] = df["State"].replace(StateNames, StateAbb)

df3 = pd.read_csv('relativesentiment.csv', sep = ',')
df = pd.merge(df, df3, how='inner', on='StateAbb')
df = df.sort_values('relative sentiment')
print(df)

df.to_csv('covariancefile.csv')

import matplotlib.pyplot as plt

# Create some mock data
state = df['StateAbb']
pop = df['Pop. density']
relg = df['Highly religious']

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('state (left: pro-Clinton, right: pro-Trump)')
ax1.set_ylabel('population density per square km', color="#1B5583")
ax1.plot(state, pop, color='#1B5583')
ax1.tick_params(axis='y', labelcolor='#1B5583')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('proportion of highly religious people', color="#B22222")  # we already handled the x-label with ax1
ax2.plot(state, relg, color="#B22222")
ax2.tick_params(axis='y', labelcolor="#B22222")

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.title("Religion and population density based on election votes")
plt.show()


# =============================================================================
# sent = list(df['relative sentiment'])
# relg = list(relg)
# 
# 
#     
# relg = [rel.replace(',','.') for rel in relg]
# relg = [float(rel) for rel in relg]
# 
# print(sent)
# print(relg)
# 
# 
# from numpy import cov
# covariance = cov(sent, relg)
# print("COV:")
# print(covariance)
# =============================================================================
