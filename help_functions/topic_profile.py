import altair as alt
import pandas as pd

def topic_profile(option):
    # Read the data
    df = pd.read_csv('datasets/tables/topic_significance_year.csv')
    df_growth = pd.read_csv('datasets/tables/topic_significance_growth.csv')

    # Filter the data based on the selected option
    if option == 'Last 3 years':
        df = df.iloc[-3:, :]
        df_growth = df_growth.iloc[-3:,:]
    elif option == 'Last 5 years':
        df = df.iloc[-5:, :]
        df_growth = df_growth.iloc[-5:,:]
    else:
        df = df.iloc[:, :]
        df_growth = df_growth.iloc[1:,:]

    # Process data for the distribution chart
    df_dist = df.sum(axis=0).to_frame()
    df_dist = df_dist.reset_index()
    df_dist.columns = ['topic', 'significance']

    # Process data for the growth chart
    topic_growth_df = df_growth.mean(axis=0).to_frame()
    topic_growth_df = topic_growth_df.reset_index()
    topic_growth_df.columns = ['topic', 'growth']

    # Distribution chart
    chart_dist = alt.Chart(df_dist).mark_bar(cornerRadius=10).encode(
        x=alt.X('significance:Q', axis=None),
        y=alt.Y('topic:N', title='', sort='-x'),
        color=alt.Color('significance:Q', scale=alt.Scale(scheme='greens'), legend=None),
        tooltip=['topic:N', 'significance:Q']
    ).properties(
        width=200, height=450, title='Subfield Significance'
    )

    # Growth chart
    grow_chart = alt.Chart(topic_growth_df).mark_bar(opacity=0.85, cornerRadius=5).encode(
        x='growth',
        y=alt.Y('topic', sort='-x', title=''),
        color=alt.condition(
            alt.datum["growth"] > 0,
            alt.value("#1f4e79"),  # Darker blue for positive growth
            alt.value("#8b0000")   # Darker red for negative growth
        )
    ).properties(
        width=400, height=450, title='Subfield Growth (%)'
    )

    # Concatenate the charts horizontally and add space between them
    chart = (chart_dist | grow_chart).configure_axis(
        labelFontSize=10, titleFontSize=12
    ).configure_view(
        strokeWidth=0  # Removes the surrounding box line
    ).properties(
        spacing=100  # Adds space between the two charts
    ).configure_title(
        fontSize=12, anchor='middle', color='#333'  # Center align title
    )

    return chart
