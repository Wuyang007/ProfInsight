import pandas as pd
import numpy as np
import altair as alt


def draw_university_profile(university_df):
    # Define a single selection that applies to both charts
    highlight = alt.selection_point(fields=['university_name'])

    # Tooltip for detailed information
    tooltip=[alt.Tooltip('university_name:N', title='University'),
            alt.Tooltip('community size (tenure track):Q', title='Faculty Community Size'),
            alt.Tooltip('average impact factor:Q', title='Average Impact Factors', format='.2f')]

    # Community Size plot with tooltip and cross-chart selection
    community_size = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('university_name', sort='-y', axis=None),
        y=alt.Y('community size (tenure track)', title='Community Size'),
        color=alt.condition(highlight, alt.value('#4a6fa9'), alt.value('lightgray')),  # Highlight selected bar
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),  # Fade unselected bars
        tooltip=tooltip
    ).add_params(
        highlight  # Add interactive selection using add_params
    ).properties(width=800, height=100)

    # Impact Factor plot with tooltip and cross-chart selection
    impact_factor = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('university_name', sort='-y', title=''),
        y=alt.Y('average impact factor', scale=alt.Scale(domain=[0, 13]), title='Average Impact Factor', ),
        color=alt.condition(highlight, alt.value('#f28f8a'), alt.value('lightgray')),  # Highlight selected bar
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),  # Fade unselected bars
        tooltip=tooltip
    ).add_params(
        highlight  # Add interactive selection using add_params
    ).properties(width=800, height=100)

    # Combine both charts vertically
    chart = (community_size & impact_factor).configure_legend(
        title=None,  # Remove legend title for a cleaner look
        symbolType='circle',  # Change the legend symbol to circles for a modern feel
        symbolSize=150,  # Make the legend symbols bigger
        orient='bottom',  # Place legend at the bottom
        columns=5,
    ).configure_view(
        strokeWidth=0  # Remove borders for a cleaner appearance
    ).configure_axis(
        grid=False,  # Remove gridlines to simplify the design
        domain=False  # Remove axis lines for a more minimalistic look
    ).configure_scale(
        bandPaddingInner=0.3,  # Add some spacing between bars for readability
        bandPaddingOuter=0.2
    )

    return chart

def draw_distribution(university_df):
    selection = alt.selection_single(
        fields=['university_name'],  # Field to select on
        bind='legend',  # Bind the selection to the legend
        name='University'  # Name of the selection
    )

    # Create the Altair chart with improved aesthetics and interactivity
    chart = alt.Chart(university_df).mark_circle().encode(
        x=alt.X('average impact factor', scale=alt.Scale(domain=[4, 13]), title='Average Impact Factor'),
        y=alt.Y('professor publications per year', scale=alt.Scale(domain=[1, 9]), title='Professor Publications per Year'),
        size=alt.Size('community size (tenure track)', scale=alt.Scale(range=[50, 500]), legend=None),
        color=alt.Color('university_name', scale=alt.Scale(scheme='viridis'), legend=alt.Legend(
        title='University Names',
        orient='bottom',
        columns=6,  # Increase the number of columns in the legend
        rowPadding=5,  # Adjust padding to make space for the labels
        labelLimit=500  # Allow longer labels (you can adjust this depending on your needs)
    )),tooltip=['university_name', 'average impact factor', 'professor publications per year', 'community size (tenure track)'],
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2))  # Opacity change when selected
    ).add_selection(
        selection  # Add the interactive selection to the chart
    ).configure_axis(
        labelFont='Arial',  # Font for the axis labels
        titleFont='Arial',  # Font for the axis titles
        titleFontSize=14,   # Font size for axis titles
        labelFontSize=12,   # Font size for axis labels
    ).configure_mark(
        opacity=0.7,  # Slight transparency for circles
        filled=True    # Fill the circles with color
    ).properties(
        width=1000,  # Width of the chart
        height=400
    )

    return chart

def add_link(df):
    link_dict = {
        'Carnegie Mellon University': 'https://www.cmu.edu/bme/People/Faculty/index.html',
        'Columbia University': 'https://www.bme.columbia.edu/directory?gsarqfields%5Bbiotypetid%5D=30',
        'Cornell University': 'https://www.bme.cornell.edu/bme/faculty-directory',
        'Duke University': 'https://bme.duke.edu/faculty',
        'ETH Zurich': 'https://biomed.ee.ethz.ch/institute/People/principal-investigators.html',
        'Georgia Institute of Technology': 'https://bioengineering.gatech.edu/program-faculty',
        'Harvard University': 'https://seas.harvard.edu/bioengineering/people?role%5B46%5D=46',
        'Imperial College London': 'https://www.imperial.ac.uk/bioengineering/people/academic-staff-and-research-fellows/',
        'Johns Hopkins University': 'https://www.bme.jhu.edu/people/faculty/',
        'Massachusetts Institute of Technology': 'https://be.mit.edu/faculty/?exposed_search&exposed_taxonomy_role%5B0%5D=35&exposed_taxonomy_role%5B1%5D=34&exposed_taxonomy_role%5B2%5D=32',
        'McGill University': 'https://www.mcgill.ca/bioengineering/people',
        'Nanyang Technological University': 'https://www.ntu.edu.sg/cceb/faculty-and-staff/chemical-engineering',
        'National University of Singapore': 'https://cde.nus.edu.sg/bme/about-us/people/academic-staff/?category=academic-3&search&sort=ASC',
        'Northwestern University': 'https://www.mccormick.northwestern.edu/biomedical/people/faculty/',
        'Peking University': 'https://future.pku.edu.cn/en/js/Faculty/index.htm',
        'Rice University': 'https://bioengineering.rice.edu/people',
        'Shanghai Jiao Tong University': 'https://en.bme.sjtu.edu.cn/lists-faculty.html',
        'Stanford University': 'https://bioengineering.stanford.edu/people/faculty',
        'Tsinghua University': 'https://www.med.tsinghua.edu.cn/en/Faculty/DepartmentofBiomedicalEngineering.htm',
        'University College London': 'https://www.ucl.ac.uk/biochemical-engineering/people/academics',
        'University of British Columbia': 'https://bme.ubc.ca/people/?custom_cat=faculty',
        'University of California Berkeley': 'https://bioeng.berkeley.edu/people',
        'University of California Los Angeles': 'https://samueli.ucla.edu/search-faculty/#be',
        'University of California San Diego': 'https://be.ucsd.edu/faculty',
        'University of California San Francisco': 'https://bts.ucsf.edu/people/faculty',
        'University of Cambridge': 'https://www.eng.cam.ac.uk/people/strategic-research-theme/181?field_user_surname_value_1=&field_user_list_category_tid=216',
        'University of Hong Kong': 'https://www.engineering.hku.hk/bmeengg/people-faculty/',
        'University of Michigan': 'https://bme.umich.edu/role/core/',
        'University of Oxford': 'https://ibme.ox.ac.uk/people/directory/?role=ac',
        'University of Pennsylvania': 'https://directory.seas.upenn.edu/bioengineering/',
        'University of Pittsburgh': 'https://www.engineering.pitt.edu/departments/bioengineering/people/faculty-research-interests/',
        'University of Sydney': 'https://www.sydney.edu.au/engineering/schools/school-of-biomedical-engineering/academic-staff.html',
        'University of Washington': 'https://bioe.uw.edu/faculty-staff/core-faculty/',
        'University of Tokyo': 'https://bioeng.t.u-tokyo.ac.jp/en/faculty/',
        'University of Toronto': 'https://bme.utoronto.ca/faculty-research/core-faculty/',
    }

    def find_link(name):
        return link_dict[name]
    
    df['link'] = df['university_name'].apply(find_link)
    
    df = df.set_index('university_name')

    return df

def draw_university_topic_profile():
    df = pd.read_csv('datasets/tables/university_topic_profile_scaled.csv')
    
    long_data = df.melt(
        id_vars='university',
        var_name = 'research area',
        value_name = 'value'
    )
    heatmap = alt.Chart(long_data).mark_rect().encode(
        x=alt.X('university:O', 
                title='',
                sort=None,  # Keeps the original order of universities
                #axis=alt.Axis(labelAngle=-45)),  # Rotates x-axis labels for better readability
                ),
        y=alt.Y('research area:O', 
                title='',
                sort=None),  # Keeps original order of research areas
        color=alt.Color('value:Q', 
                        title='Normalized significance',
                        scale=alt.Scale(scheme='blues'),
                        legend=None
                        ),  # Light blue color scheme
                        
        tooltip=[
            alt.Tooltip('university:N', title='University'),
            alt.Tooltip('research area:N', title='Research Area'),
            alt.Tooltip('value:Q', title='Value')
        ]
    ).properties(
        width=960,  # Adjust width for responsive design
        height=480  # Adjust height for responsive design
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).interactive()  # Adds zoom and pan functionality

    return heatmap


def draw_university_comparison(university_list):
    df = pd.read_csv('datasets/tables/university_topic_profile_scaled.csv')
    df = df.set_index('university')

    plot_df = df.T.reset_index()
    target_columns = ['index']+university_list
    target_df = plot_df[target_columns]
    target_df_long = target_df.melt(id_vars=['index'], var_name = 'University', value_name = 'Significance')
    chart = alt.Chart(target_df_long).mark_bar(cornerRadius=5).encode(
        x=alt.X('index:N', title=''),  # Rotate x labels for readability
        y=alt.Y('Significance:Q', title='Significance'),
        color=alt.Color('University:N', scale=alt.Scale(scheme='viridis'), legend=alt.Legend(orient='top')),  # Different colors for universities
        xOffset=alt.XOffset('University:N'),  # Shift bars to be side by side
        tooltip=['University', 'Significance']
    ).properties(
        width=1000,  # Adjust width
        height=400
    )
    return chart






def draw_university_given_topic(topic):
    # Read and preprocess the data
    df = pd.read_csv('datasets/numeric_table/university_topic_profile.csv')
    df['university'] = df['university'].str.replace('_', ' ')
    df = df.set_index('university')

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df)
    normalized_df = pd.DataFrame(normalized_data, columns=df.columns, index=df.index)
    normalized_df = normalized_df.reset_index()

    # Melt the data
    long_data = normalized_df.melt(
        id_vars='university',
        var_name='research area',
        value_name='value'
    )

    # Filter for the given topic
    long_data_mi = long_data[long_data['research area'] == topic]
    long_data_mi['value'] = long_data_mi['value'] * 10
    long_data_mi['value'] = long_data_mi['value'].astype(int)

    # Create emoji bars
    long_data_mi['emoji_bar'] = long_data_mi['value'].apply(lambda x: '🔬' * x)

    # Sort the data and keep top 15 universities
    long_data_mi = long_data_mi.sort_values(by='value', ascending=False)
    long_data_mi = long_data_mi.head(15)
    sequence = long_data_mi['university'].tolist()

    # Create the chart
    chart = alt.Chart(long_data_mi).mark_text(
        align='left',  # Align text to the left
        baseline='middle',
        fontSize=20
    ).encode(
        y=alt.Y('university:N', title=None, sort=sequence),
        text='emoji_bar:N'
    ).properties(
        title="Biomedical Engineering Scores by University", 
        width=250,
        height = 500
    )

    # Configure the view
    chart = chart.configure_view(
        stroke=None  # Removes the border around the plot area
    ).configure_axis(
        labelAngle=0,  # Prevents rotation of axis labels
        labelFontSize=14,  # Adjusts font size for axis labels
        titleFontSize=16  # Adjusts font size for axis title
    )
    return chart
