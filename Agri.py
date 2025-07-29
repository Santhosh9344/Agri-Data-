import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("D:\guvi project 2\ICRISAT-District Level Data - ICRISAT-District Level Data.csv")

# Make all Column Name into Lower case
df.columns = df.columns.str.strip().str.lower()

# All area, production, and yield fields
crop_cols = [col for col in df.columns if any(key in col.lower() for key in ["area", "production", "yield"])]

# Replace negative values with 0
df[crop_cols] = df[crop_cols].mask(df[crop_cols] < 0, 0)

# Convert YIELD from KG to TONS
for col in crop_cols:
    if "yield" in col.lower() and "kg per ha" in col.lower():
        df[col] = df[col] / 1000
        df.rename(columns={col: col.replace("KG PER HA", "TON HA")}, inplace=True)

# Removing 	Dist Code and State Code
df = df.drop(columns=["dist code", "state code"])

# Dropping duplicate rows
df = df.drop_duplicates()

# Fix the data type
df["year"] = df["year"].astype(int)
df["state name"] = df["state name"].astype(str)
df["dist name"] = df["dist name"].astype(str)

# Saving the cleaned data to a new CSV file
df.to_csv("cleaned_icrisat_data.csv", index=False)
df.info()

#Exploratory Data Analysis (EDA):

# Load the cleaned dataset
df = pd.read_csv("cleaned_icrisat_data.csv")

#1.Top 7 Rice Producing States
top_rice_states = df.groupby('state name')['rice production (1000 tons)'].sum().nlargest(7)
top_rice_states.plot(kind='bar', color='green', title='1. Top 7 States by Rice Production')
plt.ylabel('Total Rice Production (tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

# 2.Top 5 Wheat Producing States (Bar and Pie)
top5_wheat = df.groupby('state name')['wheat production (1000 tons)'].sum().nlargest(5)

#Bar Chart
top5_wheat.plot(kind='bar', color='gold', title='2. Top 5 States by Wheat Production')
plt.ylabel('Total Wheat Production (tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

#Pie Chart
top5_wheat.plot(kind="pie", autopct="%1.1f%%", title="2. Wheat Production Share")
plt.ylabel("")
plt.tight_layout()
plt.show()

#3.Top 5 Oilseed Producing States
top_oilseed_states = df.groupby('state name')['oilseeds production (1000 tons)'].sum().nlargest(5)
top_oilseed_states.plot(kind='bar', color='olive', title='3. Top 5 States by Oilseed Production')
plt.ylabel('Total Oilseed Production (tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

# 4.Top 7 Sunflower Producing States
top_sunflower_states = df.groupby('state name')['sunflower production (1000 tons)'].sum().nlargest(7)
top_sunflower_states.plot(kind='bar', color='orange', title='4. Top 7 States by Sunflower Production')
plt.ylabel('Total Sunflower Production (tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

# 5. India's Sugarcane Production (Last 50 Years)
last_50y = df[df['year'] >= df['year'].max() - 50]
sugarcane_trend = last_50y.groupby('year')['sugarcane production (1000 tons)'].sum()
sugarcane_trend.plot(kind='line', marker='o', title="5. India's Sugarcane Production (Last 50 Years)")
plt.ylabel('Production (tons)')
plt.xlabel('Year')
plt.tight_layout()
plt.show()

#6. Rice vs Wheat Production Over Time
rice_wheat_trend = last_50y.groupby('year')[['rice production (1000 tons)', 'wheat production (1000 tons)']].sum()
rice_wheat_trend.plot(marker='o', title='6. Rice vs Wheat Production (Last 50 Years)')
plt.ylabel('Production (tons)')
plt.xlabel('Year')
plt.tight_layout()
plt.show()

#7.  Rice Production by West Bengal Districts
rice_wb = df[df['state name'] == 'West Bengal']
rice_wb_grouped = rice_wb.groupby('dist name')['rice production (1000 tons)'].sum().nlargest(10)
rice_wb_grouped.plot(kind='bar', title='7. Top Rice Producing Districts in West Bengal')
plt.ylabel('Rice Production (1000 Tons)')
plt.xlabel('District')
plt.tight_layout()
plt.show()

#8. Top 10 Wheat Production Years From UP
wheat_up = df[df['state name'] == 'Uttar Pradesh']
wheat_years = wheat_up.groupby('year')['wheat production (1000 tons)'].sum().nlargest(10)
wheat_years.plot(kind='bar', color='gold', title='8. Top 10 Wheat Production Years in UP')
plt.ylabel('Wheat Production (1000 Tons)')
plt.xlabel('Year')
plt.tight_layout()
plt.show()

#9. Millet Production (Last 50 Years)
millet = df[df['year'] >= df['year'].max() - 50]
millet_grouped = millet.groupby('year')['pearl millet production (1000 tons)'].sum()
millet_grouped.plot(kind='line', marker='o', title='9. Millet Production in India (Last 50 Years)')
plt.ylabel('Production (1000 Tons)')
plt.xlabel('Year')
plt.tight_layout()
plt.show()

#10. Sorghum Production (Kharif and Rabi) by Region
sorghum_kharif = df.groupby('state name')['kharif sorghum production (1000 tons)'].sum().nlargest(7)
sorghum_rabi = df.groupby('state name')['rabi sorghum production (1000 tons)'].sum().nlargest(7)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
sorghum_kharif.plot(kind='bar', ax=ax[0], color='steelblue', title='10. Top Sorghum Kharif States')
sorghum_rabi.plot(kind='bar', ax=ax[1], color='salmon', title='10. Top Sorghum Rabi States')
ax[0].set_ylabel("Production (1000 Tons)")
ax[1].set_ylabel("Production (1000 Tons)")
plt.tight_layout()
plt.show()

#11. Top 7 States for Groundnut Production
groundnut = df.groupby('state name')['groundnut production (1000 tons)'].sum().nlargest(7)
groundnut.plot(kind='bar', color='brown', title='11. Top 7 States for Groundnut Production')
plt.ylabel('Groundnut Production (1000 Tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

#12. Soybean Production by Top 5 States and Yield Efficiency
soyabean = df.groupby('state name')[['soyabean production (1000 tons)', 'soyabean yield (kg per ha)']].sum()
top_soyabean = soyabean.nlargest(5, 'soyabean production (1000 tons)')
# Plot
ax = top_soyabean['soyabean production (1000 tons)'].plot(
    kind='bar', color='green', width=0.4, ylabel='Production (1000 Tons)', legend=True)

top_soyabean['soyabean yield (kg per ha)'].plot(
    kind='line', color='black', marker='o', secondary_y=True,
    ylabel='Yield (ton/ha)', legend=True, ax=ax)

plt.title('12. Soyabean Production vs Yield (Top 5 States)')
plt.tight_layout()
plt.show()


#13. Oilseed Production in Major States
top_oilseed = df.groupby('state name')['oilseeds production (1000 tons)'].sum().nlargest(10)
top_oilseed.plot(kind='bar', color='olive', title='13. Oilseed Production in Major States')
plt.ylabel('Production (1000 Tons)')
plt.xlabel('State')
plt.tight_layout()
plt.show()

#14.Impact of Area Cultivated on Production (Rice, Wheat, Maize)
fig, axs = plt.subplots(1, 3, figsize=(13, 5))
sns.scatterplot(data=df, x='rice area (1000 ha)', y='rice production (1000 tons)', ax=axs[0], color='skyblue')
axs[0].set_title('14. Rice: Area vs Production')
sns.scatterplot(data=df, x='wheat area (1000 ha)', y='wheat production (1000 tons)', ax=axs[1], color='gold')
axs[1].set_title('14. Wheat: Area vs Production')
sns.scatterplot(data=df, x='maize area (1000 ha)', y='maize production (1000 tons)', ax=axs[2], color='lightgreen')
axs[2].set_title('14. Maize: Area vs Production')
plt.tight_layout()
plt.show()

#15.  Rice vs. Wheat Yield Across States
yield_state = df.groupby('state name')[['rice yield (kg per ha)', 'wheat yield (kg per ha)']].mean().dropna()

yield_state.sort_values('rice yield (kg per ha)', ascending=False).plot(
    kind='bar',figsize=(10, 6),title='15. Rice vs Wheat Yield (kg per ha) Across States')
plt.ylabel("Average Yield (kg per ha)")
plt.xlabel("State")
plt.tight_layout()
plt.show()



