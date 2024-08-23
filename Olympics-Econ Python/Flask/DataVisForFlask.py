import matplotlib
matplotlib.use('Agg')  # Ensure Matplotlib uses the 'Agg' backend for non-interactive plots

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import render_template

def generateGraphs(country_input, sport_input):
    
    country = country_input
    sport = sport_input

    # 1. Reading Percentages-and-GDP.csv
    url1 = 'https://res.cloudinary.com/dkkh1tnhm/raw/upload/v1724429289/Percentages-and-GDP_ppoqqx.csv'
    df = pd.read_csv(url1, sep=",")
    print("DataFrame df loaded:", df.head())  # Debugging line

    # 2. Reading GDPsFormatted.csv
    url2 = 'https://res.cloudinary.com/dkkh1tnhm/raw/upload/v1724429290/GDPsFormatted_ztejiy.csv'
    df2 = pd.read_csv(url2, sep=",")
    print("DataFrame df2 loaded:", df2.head())  # Debugging line

    # 3. Reading GDPperCapitaFormatted.csv
    url3 = 'https://res.cloudinary.com/dkkh1tnhm/raw/upload/v1724429289/GDPperCapitaFormatted_wcemj2.csv'
    df3 = pd.read_csv(url3, sep=",")
    print("DataFrame df3 loaded:", df3.head())  # Debugging line

    # Convert 'Year' columns to numeric and handle errors
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df2['Year'] = pd.to_numeric(df2['Year'], errors='coerce')
    df3['Year'] = pd.to_numeric(df3['Year'], errors='coerce')

    # Remove rows where 'Year' is NaN
    df = df.dropna(subset=['Year'])
    df2 = df2.dropna(subset=['Year'])
    df3 = df3.dropna(subset=['Year'])

    # Convert 'Year' to integer
    df['Year'] = df['Year'].astype(int)
    df2['Year'] = df2['Year'].astype(int)
    df3['Year'] = df3['Year'].astype(int)

    # Ensure 'GDP' is numeric
    df2['GDP'] = pd.to_numeric(df2['GDP'], errors='coerce')
    df3['GDP'] = pd.to_numeric(df3['GDP per Capita'], errors='coerce')

    correlation_results = {}

    # Filter the data for the current sport
    sport_df = df[(df['Sport'] == sport) & (df['Country'] == country)]
    gdp_df = df2[(df2['Country'] == country)]
    gdp_per_capita_df = df3[(df3['Country'] == country)]

    print("Filtered sport_df:", sport_df.head())  # Debugging line
    print("Filtered gdp_df:", gdp_df.head())  # Debugging line
    print("Filtered gdp_per_capita_df:", gdp_per_capita_df.head())  # Debugging line


    # Check if either DataFrame is empty
    if sport_df.empty or gdp_df.empty:
        return render_template('results.html', 
                               message=f"Skipping {sport} due to insufficient data.",
                               correlation_results={})

    # Find the first year with GDP data
    first_gdp_year = gdp_df['Year'].min()

    # Count the number of distinct years after the first GDP year
    years_after_first_gdp_year = sport_df[sport_df['Year'] > first_gdp_year]['Year'].nunique()

    # Skip sports with 2 or fewer distinct years after the first GDP year
    if years_after_first_gdp_year <= 2:
        return render_template('results.html', 
                               message=f"Skipping {sport} due to insufficient data after {first_gdp_year}.",
                               correlation_results={})

    # Remove rows where 'Year' is NaN
    sport_df = sport_df.dropna(subset=['GDP'])
    gdp_df = gdp_df.dropna(subset=['GDP'])
    gdp_per_capita_df = gdp_per_capita_df.dropna(subset=['GDP per Capita'])

    # Sort data by Year
    sport_df = sport_df.sort_values(by='Year')
    gdp_df = gdp_df.sort_values(by='Year')
    gdp_per_capita_df = gdp_per_capita_df.sort_values(by='Year')

    # Create a complete range of years based on sport data
    min_year = sport_df['Year'].min()
    max_year = sport_df['Year'].max()

    # Create a DataFrame with all years in the range
    all_years = pd.DataFrame({'Year': range(min_year, max_year + 1)})

    # Merge to ensure every year is present in the GDP DataFrame
    gdp_df = pd.merge(all_years, gdp_df, on='Year', how='left')
    gdp_per_capita_df = pd.merge(all_years, gdp_per_capita_df, on='Year', how='left')

    # Interpolate missing GDP values
    gdp_df['GDP'] = gdp_df['GDP'].interpolate(method='linear')
    gdp_per_capita_df['GDP per Capita'] = gdp_per_capita_df['GDP per Capita'].interpolate(method='linear')

    # Calculate the percentage change in GDP and percentage change in medals won
    gdp_df['GDP_Percentage_Change'] = gdp_df['GDP'].pct_change() * 100
    sport_df['Percentage_of_Medals_Won_Change'] = sport_df['percentage_of_medals_won_for_this_sport'].pct_change() * 100

    # Calculate the percentage change in GDP per capita
    gdp_per_capita_df['GDP_per_Capita_Percentage_Change'] = gdp_per_capita_df['GDP per Capita'].pct_change() * 100

    # Fill missing values with 0 in percentage changes for plotting
    gdp_df['GDP_Percentage_Change'] = gdp_df['GDP_Percentage_Change'].fillna(0)
    gdp_per_capita_df['GDP_per_Capita_Percentage_Change'] = gdp_per_capita_df['GDP_per_Capita_Percentage_Change'].fillna(0)
    sport_df['Percentage_of_Medals_Won_Change'] = sport_df['Percentage_of_Medals_Won_Change'].fillna(0)
    

    # Create a dictionary to store the paths to the images
    image_paths = {}

    def save_plot_as_image(fig, title):
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return base64.b64encode(img.getvalue()).decode('utf8')

    # Plot percentage of medals won over time
    plt.figure(figsize=(18, 6))
    plt.plot(sport_df['Year'], sport_df['percentage_of_medals_won_for_this_sport'], marker='o')
    plt.title(f'Percentage of Medals Won Over Time for {country} ({sport})')
    plt.xlabel('Year')
    plt.ylabel('Percentage of Medals Won for This Sport')
    plt.grid(True)
    image_paths['medals_won'] = save_plot_as_image(plt.gcf(), 'Percentage of Medals Won Over Time')
    plt.close()

    # Plot percentage change in percentage of medals won over time
    plt.figure(figsize=(18, 6))
    plt.plot(sport_df['Year'], sport_df['Percentage_of_Medals_Won_Change'], marker='o', color='red')
    plt.title(f'Percentage Change in Percentage of Medals Won Over Time for {country} ({sport})')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change in Medals Won')
    plt.grid(True)
    image_paths['medals_won_change'] = save_plot_as_image(plt.gcf(), 'Percentage Change in Medals Won Over Time')
    plt.close()

    # Plot GDP over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_df['Year'], gdp_df['GDP'], marker='x', color='green')
    plt.title(f'GDP Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('GDP')
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True)
    image_paths['gdp'] = save_plot_as_image(plt.gcf(), 'GDP Over Time')
    plt.close()

    # Plot percentage change in GDP over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_df['Year'], gdp_df['GDP_Percentage_Change'], marker='o', color='blue')
    plt.title(f'Percentage Change in GDP Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change in GDP')
    plt.grid(True)
    image_paths['gdp_change'] = save_plot_as_image(plt.gcf(), 'Percentage Change in GDP Over Time')
    plt.close()

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
    image_paths['dual_axis'] = save_plot_as_image(fig, 'Percentage Change in Medals Won and GDP Over Time')
    plt.close()

    # Calculate Pearson correlation coefficient between percentage changes
    # Ensure the lengths of the series are the same before computing correlation
    common_years = sport_df.merge(gdp_df, on='Year', how='inner')
    if not common_years.empty:
        correlation = common_years['Percentage_of_Medals_Won_Change'].corr(common_years['GDP_Percentage_Change'])
        correlation_results[sport] = correlation
    else:
        correlation_results[sport] = None

    # Plot GDP per Capita over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_per_capita_df['Year'], gdp_per_capita_df['GDP per Capita'], marker='x', color='green')
    plt.title(f'GDP per Capita Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('GDP per Capita')
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True)
    image_paths['gdp_per_capita'] = save_plot_as_image(plt.gcf(), 'GDP per Capita Over Time')
    plt.close()

    # Plot percentage change in GDP per Capita over time
    plt.figure(figsize=(18, 6))
    plt.plot(gdp_per_capita_df['Year'], gdp_per_capita_df['GDP_per_Capita_Percentage_Change'], marker='o', color='blue')
    plt.title(f'Percentage Change in GDP per Capita Over Time for {country}')
    plt.xlabel('Year')
    plt.ylabel('Percentage Change in GDP per Capita')
    plt.grid(True)
    image_paths['gdp_per_capita_change'] = save_plot_as_image(plt.gcf(), 'Percentage Change in GDP per Capita Over Time')
    plt.close()

    # Dual-axis plot for percentage change in medals won and GDP per Capita percentage change
    fig, ax1 = plt.subplots(figsize=(18, 6))

    # Plot the percentage change in medals won on the primary y-axis
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Percentage Change in Medals Won', color=color)
    ax1.plot(sport_df['Year'], sport_df['Percentage_of_Medals_Won_Change'], marker='o', color=color, label='Percentage Change in Medals Won')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    # Create a second y-axis to plot the GDP per Capita percentage change
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Percentage Change in GDP per Capita Over Time', color=color)
    ax2.plot(gdp_per_capita_df['Year'], gdp_per_capita_df['GDP_per_Capita_Percentage_Change'], marker='x', color=color, label='Percentage Change in GDP per Capita Over Time')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add a title and show the plot
    plt.title(f'Percentage Change in Medals Won and GDP per Capita Over Time for {country} ({sport})')
    fig.tight_layout()  # Adjust layout to prevent overlap
    image_paths['dual_axis_alt'] = save_plot_as_image(fig, 'Percentage Change in Medals Won and GDP per Capita Over Time')
    plt.close()

    # Calculate Pearson correlation coefficient between percentage changes
    # Ensure the lengths of the series are the same before computing correlation
    common_years = sport_df.merge(gdp_per_capita_df, on='Year', how='inner')
    if not common_years.empty:
        correlation = common_years['Percentage_of_Medals_Won_Change'].corr(common_years['GDP_per_Capita_Percentage_Change'])
        correlation_results[sport] = correlation
    else:
        correlation_results[sport] = None

    return render_template('results.html', 
                           message=f"Results for {sport} and {country}",
                           image_paths=image_paths,
                           correlation_results=correlation_results)

