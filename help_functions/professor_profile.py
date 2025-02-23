import altair as alt
import pandas as pd
import pandas as pd
# import plotly.graph_objects as go

from scholarly import scholarly
from itertools import combinations
from collections import Counter
import networkx as nx

import re
import ast

def extract_words(text):
    # Use a regular expression to find all words (letters only)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    return ' '.join(words)

def create_base_chart(df):
    log_scale = alt.Scale(type='log', domain=[0.5, 100])
    base_chart = alt.Chart(df).mark_circle(size=25).encode(
        x=alt.X('num_of_pub', title='Number of publications per year'),
        #y='ave_if',
        y=alt.Y('ave_if', scale=log_scale, title='Average impact factor'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),legend=None),
        tooltip=[alt.Tooltip('university_name:N', title='University'),
                alt.Tooltip('professor_name:N', title='Professor'),
                alt.Tooltip('num_of_pub:Q', title='Number of Publications'),
                alt.Tooltip('ave_if:Q', title='Average Impact Factor'),
                alt.Tooltip('impact_level:N', title='Impact Level')],
    ).properties(
        width=800, 
        height=300,
    )
    histogram_impact_factor = alt.Chart(df).mark_bar(color='lightgray').encode(
        y=alt.Y('ave_if', bin=alt.Bin(maxbins=100), scale=log_scale, title='', axis=None),
        x=alt.X('count():Q', axis=None),
        #color=alt.Color('university_name:N', scale=alt.Scale(scheme='tableau10'), legend=None),
        tooltip=[alt.Tooltip('count():Q', title='Frequency')]
    ).properties(
        width=50,
        height=300,
    )

    histogram_num_pub = alt.Chart(df).mark_bar(color='lightgray').encode(
        x=alt.X('num_of_pub', bin=alt.Bin(maxbins=50), title='Number of Publications per Year', axis=None),
        y=alt.Y('count():Q', axis=None),
        #color=alt.Color('university_name:N', scale=alt.Scale(scheme='tableau10'), legend=None),
        tooltip=[alt.Tooltip('count():Q', title='Frequency')]
    ).properties(
        width=800,
        height=50,
    )


    # Concatenate the scatter plot and the histogram horizontally
    top_chart = alt.hconcat(base_chart, histogram_impact_factor)  # Top row: scatter plot + impact factor histogram
    combined_chart = alt.vconcat(histogram_num_pub, top_chart)
    return combined_chart

def prof_info(name):
    search_query = scholarly.search_author(name)

    # Retrieve the first search result (the most relevant one)
    if search_query:
        author = next(search_query)
        if author:
            author_data = scholarly.fill(author)
            url_profile = author_data['url_picture']

            personal_profile = {}
            personal_profile['affiliation'] = author_data['affiliation'],
            personal_profile['interests'] = author_data['interests'],
            personal_profile['total_citation'] = author_data['citedby']
            personal_profile['hindex'] = author_data['hindex']
            profile_df = pd.DataFrame(personal_profile, index=['content'])


            citation_df = pd.DataFrame(author_data['cites_per_year'], index=['citation']).T.reset_index()
            citation_chart = alt.Chart(citation_df.tail(10)).mark_bar(size=20, color='grey').encode(
                x=alt.X('index:O', title=''),  # X axis as ordinal with title 'Year'
                y=alt.Y('citation:Q')  # Y axis for citation count
            )

            text_chart = alt.Chart(citation_df.tail(10)).mark_text(
                align='center',  # Align the text in the center of the bar
                baseline='bottom',  # Place the text above the bars
                dy=-5,  # Adjust vertical position of the text
                color='grey',
            ).encode(
                x=alt.X('index:O', title=''),
                y=alt.Y('citation:Q'),
                text='citation:Q'  # Show the citation count as text
            )
            chart = (citation_chart+text_chart).configure_axis(
                grid=False  # Remove grid lines
            ).configure_view(
                stroke=None  # Remove any border around the chart
            ).configure_mark(
                opacity=0.86  # Adjust opacity for a cleaner look
            ).properties(width=300, height=150)
            

            publication_list = []
            for pub in author_data['publications'][:5]:
                pub_info_dict = {}
                pub_info_dict['title'] = pub['bib']['title']
                pub_info_dict['Publish Data'] = pub['bib']['pub_year']
                pub_info_dict['journal'] = extract_words(pub['bib']['citation'])
                pub_info_dict['citations'] = pub['num_citations']
                publication_list.append(pub_info_dict)
            publication_df = pd.DataFrame(publication_list)

            
            
            return url_profile, profile_df.T, chart, publication_df
        else:
            print('No data Found')
    else:
        print('No data Found')

def prof_univ_bar(professor_name, selected_university, df):
    university_df = df[df['university_name'] == selected_university]
    university_df['opacity'] = 0.1
    university_df.loc[university_df['professor_name']==professor_name,'opacity'] = 1
    university_df['size'] = 0.02
    university_df.loc[university_df['professor_name']==professor_name,'size'] = 0.04
    chart = alt.Chart(university_df).mark_bar().encode(
        y=alt.Y('professor_name',sort='-x', axis=None),
        x=alt.X('overall_impact', title='Overall Impact'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),title = f'Rank at {selected_university}', legend=alt.Legend(orient='top', direction='horizontal')),
        opacity=alt.Opacity('opacity', legend=None),

        tooltip=[
            alt.Tooltip('professor_name:N', title='Professor name'),  # Tooltip for professor names
            alt.Tooltip('num_of_pub:Q', title='Publication per year'),  # Format overall impact
            alt.Tooltip('overall_impact:Q', title = 'Overall contribution', format = '.2f'),
            alt.Tooltip('ave_if:Q', title = 'Average impact factor', format = '.2f'),
            alt.Tooltip('Community Contribution:N', title='Community Contribution')  # Add contribution to tooltip
        ]
    ).properties(width=100, height=600)
    return chart

def univ_bar(selected_university, df):
    university_df = df[df['university_name'] == selected_university] 
    chart = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('professor_name',sort='-y', axis=None),
        y=alt.Y('overall_impact', title='Overall Impact'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),legend=alt.Legend(orient='top', direction='horizontal')),
        tooltip=[
            alt.Tooltip('professor_name:N', title='Professor name'),  # Tooltip for professor names
            alt.Tooltip('num_of_pub:Q', title='Publication per year'),  # Format overall impact
            alt.Tooltip('overall_impact:Q', title = 'Overall contribution', format = '.2f'),
            alt.Tooltip('ave_if:Q', title = 'Average impact factor', format = '.2f'),
            alt.Tooltip('Community Contribution:N', title='Community Contribution')  # Add contribution to tooltip
        ]
    ).properties(width=800, height=400)
    return chart



def profile_individual(university, name):
    df = pd.read_csv('datasets/prof_topic.csv')
    unique_name = university+'--'+name
    person_info = df[df['Unnamed: 0']==unique_name]

    person_topic_info = person_info.iloc[:,1:].T
    person_topic_info.columns = ['score']
    person_topic_info = person_topic_info.sort_values(by='score', ascending=False)
    person_topic_info = person_topic_info.head(8)
    person_topic_info=person_topic_info.reset_index()
    max_radius = person_topic_info.iloc[0,1]
    fig = go.Figure()

    # Add trace to radar plot with improved color style
    fig.add_trace(go.Scatterpolar(
        r=person_topic_info['score'].tolist() + [person_topic_info['score'].iloc[0]],  # Close the circle
        theta=person_topic_info['index'].tolist() + [person_topic_info['index'].iloc[0]],  # Close the circle
        fill='toself',
        line=dict(color='deepskyblue', width=2),  # Change line color
        fillcolor='rgba(135, 206, 250, 0.3)'  # Light blue fill color with transparency
    ))

    # Update layout for radar plot
    fig.update_layout(
        title='',
        width=400,  # Set the figure width (increase for larger plots)
        height=400,  # Set the figure height    
        title_x=0.5,  # Center the title
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_radius],  # Adjust according to your data range
                showticklabels=True,
                ticks='outside',
                ticklen=5
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='black'),  # Customize axis labels
                showticklabels=True,
                ticks='outside'
            )
        ),
        legend=dict(
            title='Legend',
            title_font_size=13,
            font=dict(size=12, color='black')
        ),
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
    )


    return fig


def draw_network():
    canvas_width = 1400
    canvas_height = 400

    edge_df = pd.read_csv('../datasets/chart/network/edges.csv')
    nodes_df = pd.read_csv('../datasets/chart/network/nodess.csv')
    university_positions = pd.read_csv('../datasets/chart/network/text_position.csv')

    # **Edge Chart with Better Visibility**
    edge_chart_list = []
    for i in range(12):
        row_range_top = i * 5000
        row_range_bottom = i * 5000 + 5000
        edges_chart = alt.Chart(edge_df.iloc[row_range_top:row_range_bottom, :]).mark_line(
            color='gray', opacity=0.2, size=0.5  # Softer color, better opacity
        ).encode(
            x=alt.X('x:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  
            y=alt.Y('y:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  
            x2='x_target:Q',  
            y2='y_target:Q',  
            #size=alt.Size('Weight:Q', scale=alt.Scale(domain=[0, edge_df['Weight'].max()], range=[0.2, 2])),  
            tooltip=[alt.Tooltip('Weight:Q', title='Edge Weight')]
        ).properties(
            width=canvas_width, height=canvas_height
        ).interactive()

        edge_chart_list.append(edges_chart)

    # **Node Chart with Interactive Filtering**
    node_chart = alt.Chart(nodes_df).mark_circle(stroke='black', strokeWidth=0.5, size=10).encode(
        x='x',
        y='y',
        color=alt.Color(
            'university_name:N',
            scale=alt.Scale(scheme='tableau20'),
            legend=None
            
        ),
        size=alt.Size('overall_impact', legend=None),
        tooltip=['university_name', 'name']
    ).properties(
        width=canvas_width, height=canvas_height
    ).interactive()

    text_labels = alt.Chart(university_positions).mark_text(
        align='center',  # Align text to the left of the cluster
        baseline='middle',
        fontSize=8,
        dy=10,
    ).encode(
        x='x:Q',  # Use the average x position
        y='y:Q',  # Use the average y position
        text='university_name:N',  # Display the university name
        color=alt.Color('university_name:N', scale=alt.Scale(scheme='tableau20'))  # Same color as nodes
    )

    # **Combine All Edge Charts**
    overall_chart = edge_chart_list[0]
    for chart in edge_chart_list[1:]:
        overall_chart += chart

    # **Final Chart: Merging Edges and Nodes**
    overall_chart = (overall_chart + node_chart+text_labels).configure_view(
        strokeWidth=0  # Removes unnecessary border
    ).configure_axis(
        grid=False
    ).configure_legend(
        titleFontSize=14, labelFontSize=12
    )

    # Show the chart
    return overall_chart


def compare_prof(uni_1, prof_1, uni_2, prof_2):

    df = pd.read_csv('datasets/prof_topic.csv')
    unique_name_1 = uni_1+'--'+prof_1
    unique_name_2 = uni_2+'--'+prof_2

    person_info_1 = df[df['Unnamed: 0']==unique_name_1]
    person_topic_info_1 = person_info_1.iloc[:,1:].T

    person_info_2 = df[df['Unnamed: 0']==unique_name_2]
    person_topic_info_2 = person_info_2.iloc[:,1:].T

    features = person_topic_info_1.index.tolist()

    values_left = person_topic_info_1.values[:,0]
    values_right = person_topic_info_2.values[:,0]

    values_left_neg = [-v for v in values_left]

    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=features,
        x=values_left_neg,  # Negative values for left bars
        orientation='h',
        name=prof_1,
        marker=dict(color="rgba(47, 108, 153, 0.8)")  # Softer Blue with 90% transparency
    ))

    # Add right-side bars (Darker Red with 90% transparency)
    fig.add_trace(go.Bar(
        y=features,
        x=values_right,  # Positive values for right bars
        orientation='h',
        name=prof_2,
        marker=dict(color="rgba(184, 50, 42, 0.8)")  # Softer Red with 90% transparency
    ))

    # Customize layout (Remove background and grid lines)
    fig.update_layout(
        title="",
        barmode='relative',  # Ensure bars don't overlap
        xaxis=dict(
            title="",
            tickvals=[-60, -40, -20, 0, 20, 40, 60],  # Ensure negative values appear symmetrically
            ticktext=[60, 40, 20, 0, 20, 40, 60],  # Remove negative sign in labels
            showgrid=False,  # Remove grid lines
            zeroline=False  # Remove center line
        ),
        yaxis=dict(title=None, showgrid=False),  # Remove y-axis grid lines
        plot_bgcolor="white",  # Remove background color
        paper_bgcolor="white",  # Remove full background color
        showlegend=True,
        height=400,  # Increase height to make the figure taller
        width=250  # Decrease width to make the figure narrower
    )

    # Show the figure
    return fig


def find_best_paper(university, name):
    paper_df = pd.read_csv('datasets/paper_with_title.csv')
    personal_df = paper_df[paper_df['university']==university]
    personal_df = personal_df[personal_df['professor_name']==name]

    personal_df = paper_df[paper_df['professor_authorship'].isin(['First Corresponding author', 'First Author'])]
    personal_df = personal_df.drop_duplicates(subset='PMID')
    personal_df = personal_df.sort_values(by='journal_if', ascending=False)

    personal_df['publish_date'] = pd.to_datetime(personal_df['publish_date'])
    personal_df['time']  = personal_df['publish_date'].dt.to_period('M')
    personal_df=personal_df[['time', 'PMID','title']]
    personal_df = personal_df.iloc[:10,:]
    personal_df.set_index('time', inplace=True)

    return personal_df 

def find_network(professor):
    paper_df = pd.read_csv('datasets/numeric_table/co-author.csv')

    paper_df['co_authors'] = paper_df['co_authors'].apply(ast.literal_eval)
    mask = []
    for item in paper_df['co_authors']:
        mask.append(professor in item)
    
    person_network = paper_df[mask]

    person_network = person_network[person_network['length']>1]
    collaboration_series = person_network['co_authors']

    overall_pairs = []
    for item in collaboration_series:
        pairs = list(combinations(item, 2))
        overall_pairs.append(pairs)

    def flatten_list(lst):
        flattened = []
        for item in lst:
            if isinstance(item, list):
                flattened.extend(flatten_list(item))
            else:
                flattened.append(item)
        return flattened

    # Example usage
    flattened_list = flatten_list(overall_pairs)

    tuple_list = list(zip(flattened_list[::2], flattened_list[1::2]))
    flat_list = [item for tup in tuple_list for item in tup]

    normalized_pairs = [
        (pair[1], pair[0]) if pair[1] == professor else pair
        for pair in flat_list
    ]

    edge_weights = Counter(normalized_pairs)

    prof_df = pd.DataFrame([(name1, name2, weight) for (name1, name2), weight in edge_weights.items()],
                  columns=['Core_prof', 'Co_prof', 'Weight'])
    

    G = nx.Graph()
    for _, row in prof_df.iterrows():
        G.add_edge(row['Core_prof'], row['Co_prof'], weight=row['Weight'])
    pos = nx.spring_layout(G, seed=21) 
    nodes_df = pd.DataFrame([(node, pos[node][0], pos[node][1]) for node in G.nodes],
                        columns=['name', 'x', 'y'])
    
    edge_df = prof_df.merge(nodes_df, left_on='Core_prof', right_on='name', suffixes=('', '_source'))
    edge_df = edge_df.merge(nodes_df, left_on='Co_prof', right_on='name', suffixes = ('', '_target'))
    
    prof_df = pd.read_csv('datasets/professor_profile.csv')
    prof_df = prof_df[['university_name', 'professor_name','overall_impact']]

    prof_label_df = pd.read_csv('datasets/numeric_table/prof_label.csv')

    nodes_df = nodes_df.merge(prof_df, left_on='name', right_on='professor_name')
    nodes_df = nodes_df.merge(prof_label_df, left_on='name', right_on='professor')


    # Nodes Chart (with proper size encoding)
    nodes_chart = alt.Chart(nodes_df).mark_circle(
        opacity=1,  # Set opacity to 1
        stroke='black',  # Set circle edge color to black
        strokeWidth=0.5  # Set the thickness of the edge
    ).encode(
        x=alt.X('x:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        y=alt.Y('y:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        size=alt.Size('overall_impact:Q', scale=alt.Scale(range=[200, 1000]), legend=None),  # Node size
        color=alt.Color('label:N', title='University', legend=None)
    ).properties(
        width=400,
        height=400
    )

    # Edges Chart (size encoding for line thickness)
    edges_chart = alt.Chart(edge_df).mark_line(color='gray', opacity=1).encode(
        x=alt.X('x:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        y=alt.Y('y:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        x2='x_target:Q',  # Target node's x-coordinate
        y2='y_target:Q',  # Target node's y-coordinate
        #size=alt.Size('Weight:Q', scale=alt.Scale(domain=[0, edge_df['Weight'].max()], range=[1, 5])),  # Line thickness based on weight
        color=alt.Color('Weight:Q', legend=None),  # Line color based on weight
        tooltip=[alt.Tooltip('Weight:Q', title='Co-author times')]
    ).properties(
        width=400,
        height=400
    )

    # Text Chart (Node Labels)
    text_chart = alt.Chart(nodes_df).mark_text(baseline='middle', align='center', dx=0, dy=-16, size=12).encode(
        x=alt.X('x:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        y=alt.Y('y:Q', title='', axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False)),  # Hide axis
        text='name:N'
    ).properties(
        width=400,
        height=400
    )

    # Combine the charts
    final_chart = edges_chart + nodes_chart + text_chart

    # Apply configuration to remove the grid lines and the border around the chart
    final_chart = final_chart.configure_axis(
        grid=False,  # Hide grid lines
        ticks=False,  # Hide ticks
        labels=False,  # Hide labels
        domain=False  # Hide axis line
    ).configure_view(
        stroke=None  # Remove the border around the view
    )

    return final_chart



