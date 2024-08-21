import pandas as pd
import matplotlib.pyplot as plt

# Reading the databases
data = pd.read_csv("Percentages-and-GDP.csv")
df = pd.DataFrame(data)

data2 = pd.read_csv("GDPsFormatted.csv")
df2 = pd.DataFrame(data2)

# Convert 'Year' columns to numeric and handle errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df2['Year'] = pd.to_numeric(df2['Year'], errors='coerce')

# Remove rows where 'Year' is NaN
df = df.dropna(subset=['Year'])
df2 = df2.dropna(subset=['Year'])

# Convert 'Year' to integer
df['Year'] = df['Year'].astype(int)
df2['Year'] = df2['Year'].astype(int)

# Ensure 'GDP' is numeric
df2['GDP'] = pd.to_numeric(df2['GDP'], errors='coerce')

# Get unique sports
sports = ['Weightlifting', 'Boxing']

# Dictionary to store correlation coefficients
correlation_results = {}

country = 'Australia'

# Loop through each sport
for sport in sports:
    # Filter the data for the current sport
    sport_df = df[(df['Sport'] == sport) & (df['Country'] == country)]
    gdp_df = df2[(df2['Country'] == country)]

    # Check if either DataFrame is empty
    if sport_df.empty or gdp_df.empty:
        print(f"Skipping {sport} due to insufficient data.")
        continue

    # Check if there are 2 or fewer distinct years of data
    years_after_1960 = sport_df[sport_df['Year'] > 1960]['Year'].nunique()
    if years_after_1960 <= 2:
        print(f"Skipping {sport} due to 2 or fewer distinct years of data.")
        continue

    # Remove rows where 'Year' is NaN
    sport_df = sport_df.dropna(subset=['GDP'])
    gdp_df = gdp_df.dropna(subset=['GDP'])

    # Sort data by Year
    sport_df = sport_df.sort_values(by='Year')
    gdp_df = gdp_df.sort_values(by='Year')

    # Create a complete range of years based on sport data
    min_year = sport_df['Year'].min()
    max_year = sport_df['Year'].max()

    # Create a DataFrame with all years in the range
    try: all_years = pd.DataFrame({'Year': range(min_year, max_year + 1)})
    except TypeError:
        continue

    # Merge to ensure every year is present in the GDP DataFrame
    gdp_df = pd.merge(all_years, gdp_df, on='Year', how='left')

    # Interpolate missing GDP values
    gdp_df['GDP'] = gdp_df['GDP'].interpolate(method='linear')

    # Calculate the percentage change in GDP and percentage change in medals won
    gdp_df['GDP_Percentage_Change'] = gdp_df['GDP'].pct_change() * 100
    sport_df['Percentage_of_Medals_Won_Change'] = sport_df['percentage_of_medals_won_for_this_sport'].pct_change() * 100

    # Fill missing values with 0 in percentage changes for plotting
    gdp_df['GDP_Percentage_Change'] = gdp_df['GDP_Percentage_Change'].fillna(0)
    sport_df['Percentage_of_Medals_Won_Change'] = sport_df['Percentage_of_Medals_Won_Change'].fillna(0)

    # Plot percentage of medals won over time
    plt.figure(figsize=(18, 6))
    plt.plot(sport_df['Year'], sport_df['percentage_of_medals_won_for_this_sport'], marker='o')
    plt.title(f'Percentage of Medals Won Over Time for {country} ({sport})')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Medals Won for This Sport')
    plt.grid(True)
    plt.show()

    # Plot percentage change in percentage of medals won over time
    plt.figure(figsize=(18, 6))
    plt.plot(sport_df['Year'], sport_df['Percentage_of_Medals_Won_Change'], marker='o', color='red')
    plt.title(f'Percentage Change in Percentage of Medals Won Over Time for {country} ({sport})')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change in Medals Won')
    plt.grid(True)
    plt.show()

    # Plot GDP over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_df['Year'], gdp_df['GDP'], marker='x', color='green')
    plt.title(f'GDP Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('GDP')
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True)
    plt.show()

    # Plot percentage change in GDP over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_df['Year'], gdp_df['GDP_Percentage_Change'], marker='o', color='blue')
    plt.title(f'Percentage Change in GDP Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change in GDP')
    plt.grid(True)
    plt.show()

    # Dual-axis plot for percentage change in medals won and GDP percentage change
    fig, ax1 = plt.subplots(figsize=(18, 6))

    # Plot the percentage change in medals won on the primary y-axis
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Percentage Change in Medals Won', color=color)
    ax1.plot(sport_df['Year'], sport_df['Percentage_of_Medals_Won_Change'], marker='o', color=color, label='Percentage Change in Medals Won')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    # Create a second y-axis to plot the GDP percentage change
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Percentage Change in GDP', color=color)
    ax2.plot(gdp_df['Year'], gdp_df['GDP_Percentage_Change'], marker='x', color=color, label='Percentage Change in GDP')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add a title and show the plot
    plt.title(f'Percentage Change in Medals Won and GDP Over Time for {country} ({sport})')
    fig.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

    # Calculate Pearson correlation coefficient between percentage changes
    # Ensure the lengths of the series are the same before computing correlation
    common_years = sport_df.merge(gdp_df, on='Year', how='inner')
    if not common_years.empty:
        correlation = common_years['Percentage_of_Medals_Won_Change'].corr(common_years['GDP_Percentage_Change'])
        correlation_results[sport] = correlation
    else:
        correlation_results[sport] = None

# Print the correlation coefficients for each sport
print("Pearson correlation coefficients:")
for sport, correlation in correlation_results.items():
    if correlation is not None:
        print(f'{sport}: {correlation:.2f}')
    else:
        print(f'{sport}: Not enough data for correlation calculation')
