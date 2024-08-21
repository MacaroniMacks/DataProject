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
sports = df['Sport'].unique()

# Dictionary to store correlation coefficients
correlation_results = {}

country = 'United Kingdom'

# Loop through each sport
for sport in sports:
    # Filter the data for the current sport
    sport_df = df[(df['Sport'] == sport) & (df['Country'] == country)]
    gdp_df = df2[(df2['Country'] == country)]

    # Check if either DataFrame is empty
    if sport_df.empty or gdp_df.empty:
        continue

    # Find the first year with GDP data
    first_gdp_year = gdp_df['Year'].min()

    # Count the number of distinct years after the first GDP year
    years_after_first_gdp_year = sport_df[sport_df['Year'] > first_gdp_year]['Year'].nunique()

    # Skip sports with 2 or fewer distinct years after the first GDP year
    if years_after_first_gdp_year <= 2:
        print(f"Skipping {sport} due to insufficient data after {first_gdp_year}.")
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
