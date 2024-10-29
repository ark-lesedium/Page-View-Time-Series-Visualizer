import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Global variable to hold the DataFrame
df = None

def load_data():
    global df
    df = pd.read_csv('fcc-forum-pageviews.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

def clean_data(df):
    lower_bound = df['value'].quantile(0.025)
    upper_bound = df['value'].quantile(0.975)
    df_cleaned = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)].copy()  # Make a copy
    return df_cleaned

def draw_line_plot():
    df = load_data()
    df = clean_data(df)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['value'])
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    fig.autofmt_xdate()
    
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df = load_data()
    df = clean_data(df)
    
    df_bar = df.groupby([df.index.year, df.index.month]).mean().unstack()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.plot(kind='bar', ax=ax)
    
    ax.set_title('Average Daily Page Views by Month and Year')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df = load_data()
    df = clean_data(df).copy()  # Make a copy after cleaning
    
    # Create new columns for year and month using .loc
    df.loc[:, 'year'] = df.index.year
    df.loc[:, 'month'] = df.index.month_name()  # Get month names
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
    
    sns.boxplot(x='year', y='value', data=df, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    sns.boxplot(x='month', y='value', data=df, ax=ax2, order=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    fig.savefig('box_plot.png')
    return fig