import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import calendar


#importing dataset
# dataframe= pd.read_csv('Unemployment in India.csv')
dataframe= pd.read_csv('Unemployment_Rate_upto_11_2020.csv')

# Remove leading and trailing spaces from column names
dataframe.columns = dataframe.columns.str.strip()

print(dataframe)
print(dataframe.columns)


#data cleaning
#checking any missing values
dataframe['Estimated Employed']= pd.to_numeric(dataframe['Estimated Employed'], errors='coerce')
print(dataframe.isnull().sum())


#correcting column names
dataframe.columns=["States", "Date", "Frequency",
                   "Estimated Unemployment Rate","Estimated Employed",
                   "Estimated Labour Participation Rate", "Region",
                   "longitude", "latitude"]


#Data Visualization:

#Graph 1: India's General Employment
plt.figure(figsize=(10,6))
sns.histplot(x='Estimated Employed', hue= 'Region', data= dataframe, bins=20, kde=True, palette='viridis')
plt.title('Distribution of Estimated Employed Population in India by Region')
plt.xlabel('Estimated Employed')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
plt.close()


# #Graph 2: Dashboard
unemp= dataframe[['States', 'Region', 'Estimated Unemployment Rate']]
figure= px.sunburst(unemp, path=['Region', 'States'],
                    values='Estimated Unemployment Rate', width= 700,
                    height= 700, color_continuous_scale='RdY1Gn',
                    title='Unemployment Rate in India')
figure.show()



#Graph 3: Unemployment Rate According to Different States in India

StateUnemployment= dataframe.groupby('States')['Estimated Unemployment Rate'].mean().reset_index()
unempSorted= StateUnemployment.sort_values(by='Estimated Unemployment Rate', ascending=False)
plt.figure(figsize=(12,6))
sns.barplot(x='States', y='Estimated Unemployment Rate', data=unempSorted, palette='magma')
plt.xticks(rotation= 90)
plt.xlabel('State')
plt.ylabel('Average Unemployment Rate')
plt.title('Unemployment Rate According to Different States in India')
plt.tight_layout()
plt.show()
plt.close()


#Graph 4: Monthly average Unemployment Rate

#extracting months from the date column
dataframe['Date']= pd.to_datetime(dataframe['Date'])
dataframe['Month']= dataframe['Date'].dt.month

#defining monthly average unemployment
MonthlyAvg= dataframe.groupby('Month')['Estimated Unemployment Rate'].mean()

plt.figure(figsize=(8,6))
sns.barplot(x=MonthlyAvg.index ,y=MonthlyAvg.values, palette='viridis')
plt.title('Average Monthly Unemployment Rate in India')
plt.xlabel('Month')
plt.ylabel('Average Unemployment Rate')
plt.xticks(np.arange(0,12), calendar.month_abbr[1:13], rotation=90)
plt.show()
plt.close()


#Graph 5: Employed vs. Laboour Participation Rate

plt.figure(figsize=(10,6))
sns.scatterplot(x='Estimated Employed', y='Estimated Labour Participation Rate', data=dataframe)
plt.xlabel('Employed')
plt.ylabel('Labour Participation Rate')
plt.title('Employed vs. Labour Participation Rate')
plt.show()
plt.close()


#Graph 6: Employment Rate over Time

plt.figure(figsize=(10,6))
plt.fill_between(MonthlyAvg.index, MonthlyAvg.values, color='skyblue',
                 alpha=0.4, label='Monthly Average Unemployment Rate')
plt.plot(MonthlyAvg.index, MonthlyAvg.values, marker='o', linestyle='-', color='b')

#highlighting peak covid-19
covid=4 #4 as covid emerged in april
plt.axvline(x=covid, color='r', linestyle='--', label='COVID-19 Peak (April 1st 2020)')
plt.xlabel('Month')
plt.ylabel('Average Unemployment Rate')
plt.title('Monthly Average Unemployment Rate')
plt.xticks(np.arange(1,13), calendar.month_abbr[1:13], rotation=90)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
plt.close()