import streamlit as st
import pandas as pd
import altair as alt
import requests

import streamlit as st
import os
from PIL import Image


import sys
sys.path.append('help_functions')

from help_functions.university_profile import draw_distribution, draw_university_topic_profile, draw_university_comparison
from help_functions.professor_profile import prof_info, profile_individual, find_network, compare_prof


#--------------------------------------------------------------------------------------------
st.set_page_config(page_title="Prof-Insight", layout="wide")

st.sidebar.image('datasets/images/logo.png', width=150)

#st.sidebar.title("Prof-Insight")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.text_input("Search")
# this search for now doesn't work much.
st.sidebar.markdown("<br>", unsafe_allow_html=True)

selected_section = st.sidebar.radio("Go to", ["Welcome", "University overview", 'Professor overview', 'Topic overview', 'Find your professors', "About this project"])


st.sidebar.markdown("<div style='height: 100%;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### Contact Us")
st.sidebar.markdown("[Email us](mailto:wuyang.gao007@gmail.com)")

#--------------------------------------------------------------------------------------------
# following is for the overview page
if selected_section == "Welcome":

    col1, col2, col3 = st.columns([1, 3, 1])  # Set the column width ratio 1:3:1
    with col2: 
        st.image('datasets/images/welcome_page.png', caption='')
    st.markdown("""
    <style>
        .highlighted-text {
            font-size: 36px; /* Slightly smaller but still prominent */
            font-weight: 600; /* Semi-bold for a refined look */
            color: #003366; /* Dark blue color for professionalism */
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
            letter-spacing: 1px; /* Slight spacing between letters for readability */
            text-align: center; /* Center align text */
            margin-top: 40px; /* Space above text */
            margin-bottom: 40px; /* Space below text */
            line-height: 1.4; /* Adjust line height for better readability */
        }
        .info-bar {
            background-color: #e74c3c; /* Orange-red background color */
            color: #ffffff; /* White text color */
            font-size: 16px; /* Font size for the bar text */
            font-weight: 700; /* Bold text */
            text-align: center; /* Center align text */
            padding: 15px 0; /* Padding for top and bottom */
            margin: 20px 0; /* Margin for spacing */
            border-radius: 5px; /* Rounded corners for a softer look */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        }
    </style>
""", unsafe_allow_html=True)

    st.markdown("""
    <div class="highlighted-text">
        Find your perfect professor—AI-powered insights, no hassle!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('\n\n')

    col1, col2, col3 = st.columns([1, 0.5, 1]) 
    with col2:  
        st.image('datasets/images/logo.png', caption='')

#--------------------------------------------------------------------------------------------
# following is for the university page
elif selected_section == "University overview":
    st.title("🌍  Top Universities in Biomedical Engineering")

    # Add a subtle divider for a sleek look
    st.divider()  

    # Section: University Research Community
    st.subheader("1. University Research Community Size")
    st.markdown("Explore the size of each university's faculty (number of professors) and their impact in the field of biomedical engineering.")
    st.image('datasets/chart/university_treemap.png',  caption='interactive version is available on the github')
    st.caption("🔍 The size of each rectangle represents the tenure-track faculty community, while the color reflects research impact (impact factor).")


    st.divider() 
    st.subheader("2. Impact Factors vs Publication Frequency")
    st.markdown("""
    In this section, we examine two key metrics that drive academic success across universities:
    - **📚 Publication Frequency**: How often professors publish their research
    - **🌟 Average Impact Factor**: The influence and quality of their research

    By visualizing these factors, we can uncover patterns linking higher publication activity with research quality. 
    This allows us to explore the dynamic relationship between academic output and influence at top institutions.
    """)
    st.write("\n")

    university_df = pd.read_csv('datasets/tables/university_profile.csv')
    distribution_chart = draw_distribution(university_df)
    st.altair_chart(distribution_chart, use_container_width=True)
    st.write("\n")
    top_impact_factors = university_df[['university_name', 'average impact factor']].sort_values(by='average impact factor', ascending=False).head(5)
    top_publication_frequency = university_df[['university_name', 'professor publications per year']].sort_values(by='professor publications per year', ascending=False).head(5)

    gap1, col1, gap2, col2 = st.columns([0.1,1, 0.1, 1])

    with col1:
        # Top 5 Impact Factors
        st.markdown("**Top 5 Universities by Impact Factor**")
        st.dataframe(top_impact_factors)

    with col2:
        # Top 5 Publication Frequency
        st.markdown("**Top 5 Universities by Publication Frequency**")
        st.dataframe(top_publication_frequency)

    st.markdown('<br><br>', unsafe_allow_html=True) 
    st.divider() 
    st.subheader("3. Overview of Biomedical Engineering Subfields")
    st.markdown(
        """
        This dashboard compares **35 universities** across **20 research subfields** in Biomedical Engineering.
        - Explore an overall heatmap of research intensity.
        - Select a subfield to see which universities specialize in that area.
        """
    )

    university_topic_df = pd.read_csv('datasets/tables/university_topic_profile.csv')
    topic_list = university_topic_df.columns.tolist()
    topic_list = topic_list[1:]

    topic_university_chart = draw_university_topic_profile()

    col1, gap1, col2, gap2= st.columns([5,0.75,3, 0.25])
    with col1:
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')
        st.markdown('\n')

        st.markdown('**35 universities across 20 sub fields**')
        st.altair_chart(topic_university_chart, use_container_width=True)
    
    with col2:
        col1, col2 = st.columns([2,1])
        default_topic = topic_list[0]

        selected_topic = st.selectbox("Choose a research area:", topic_list, index=topic_list.index(default_topic))  # Set default selected topic

        #if button or selected_topic == default_topic:
        image_file_png = f'datasets/topic_ranking/{selected_topic}.png'
        st.write('\n')
        
        caption = f"Caption: Top 15 Universities Ranking for {selected_topic} (Ranked by Contribution)"
        st.image(image_file_png, use_container_width=True, caption=caption)
    
    st.divider() 
    st.subheader("4. University Research Comparison:")
    st.markdown("""
    Compare research metrics across three universities:

    - **Faculty Size**: Number of tenure-track professors.
    - **Publication Frequency**: Publications per professor per year.
    - **Average Impact Factor**: Average impact factor of publications.
    - **Subfield Expertise**: Expertise Profile in biomedical Engineering.

    """)

    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        selected_university_1 = st.selectbox(
            "Select University", 
            options=university_df['university_name'].unique(), 
            index=0,  # Default to the first element
            key='uni_1'
        )
    with col2:
        selected_university_2 = st.selectbox(
            "Select University", 
            options=university_df['university_name'].unique(), 
            index=1,  # Default to the first element
            key='uni_2'
        )
    with col3:
        selected_university_3 = st.selectbox(
            "Select University", 
            options=[""] + university_df['university_name'].unique().tolist(),  # Add an empty string at the beginning
            index=0,  # Default to the empty selection
            key='uni_3'
        )
    with col4:
        selected_university_4 = st.selectbox(
            "Select University", 
            options=[""] + university_df['university_name'].unique().tolist(),  # Add an empty string at the beginning
            index=0,  # Default to the empty selection
            key='uni_4'
        )

    selected_list = [selected_university_1, selected_university_2, selected_university_3, selected_university_4]
    compare_df = university_df[university_df['university_name'].isin(selected_list)]
    st.write('\n')
    st.markdown('- Academic metrics: ')
    gap1, col1, gap2 = st.columns([0.2, 4,0.2])
    with col1:
        st.write(compare_df)
    st.write('\n')
    st.markdown('- Subfields comparison: ')
    filtered_list = [university for university in selected_list if university]

    gap1, col1, gap2 = st.columns([0.2, 4,0.2])
    with col1:
        comparison_chart = draw_university_comparison(filtered_list)
        st.altair_chart(comparison_chart, use_container_width=True)

    st.divider()
    st.subheader('5. Questions?')

    user_question = st.text_input("🙋🏻 Ask me anything about universities:")

    # Add a submit button
    if st.button("Submit"):
        # Simulated response (can be replaced with actual logic once RAG is implemented)
        if user_question:
            st.write(f"**You asked:** {user_question}")
            st.write("**Chatbot's response:**")
            
            # Here, you can add logic for predefined responses based on keywords
            # or placeholders while you work on implementing the RAG system.
            
            # Example responses:
            if "university ranking" in user_question.lower():
                st.write("The top universities vary by field of research. For example, 'University of Tokyo' excels in engineering.")
            elif "faculty size" in user_question.lower():
                st.write("Faculty sizes can vary across universities, depending on their research community size.")
            elif "publications" in user_question.lower():
                st.write("Publications per year often depend on the university's faculty research output.")
            else:
                st.write("I am currently gathering more information. Please check back soon!")
        else:
            st.write("Please enter a question to ask.")
    #---

elif selected_section == "Professor overview":
    st.title("🧑🏻‍🎓 **Top Professors in Biomedical Engineering**")
    
    # Divider for clear section separation
    st.write('\n')
    st.divider()
    
    # Section Title
    st.header("1. University Network Visualization")
    st.markdown("""
        This visualization shows university collaborations based on publication data. 
        - **Nodes**: Each represents a professor.
        - **Edges**: Indicate collaborations between professors.
        - **Node size**: Reflects the profess's overall impact.
        - **Color**: Represent the university.

        
    """)
    #with open("datasets/chart/professor_network_summary.html", "r", encoding="utf-8") as f:
    st.image('datasets/chart/professor_university_network.png', caption='')
    st.write('Interactive version could be found in github 🔍')

    st.divider()

    st.header("2. Academic Metrics Overview")

    st.subheader("📏 Publication Frequency vs Impact Factor")
    # Load Data
    
    # Brief Description
    st.markdown("""
        In this section, we display key academic metrics for top Biomedical Engineering professors. 
        These metrics include:
        - **Publication frequency**
        - **Average impact factor**
        - **Overall contribution to the community**
        
        Explore how these factors are connected and how they contribute to the advancement of the field.
    """)

    
    # Display the base chart with a clear description
    st.markdown("Below is the visualization of publication frequency versus impact factor. This chart helps to understand the relationship between how often professors publish and the overall quality and impact of their research.")
    st.write('\n')
    st.write('\n')
    
    col1, col2, col3 = st.columns([0.5,4,1])
    with col2:
        #df = pd.read_csv('datasets/tables/professor_profile.csv')
        #st.table(df.head())
        #base_chart = create_base_chart(df)
        #st.altair_chart(base_chart)
        st.image('datasets/chart/academic_metrics_prof.png')
        st.write('hahaha')

    # Spacer for better page layout
    st.markdown('<br>', unsafe_allow_html=True)

    st.divider() 

    st.header("3. Check your professor")
    # University selection
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        default_university = "University of Toronto"
        default_professor = "Axel Gunther"

        # Filter professor list based on the selected university
        df = pd.read_csv('datasets/tables/professor_profile.csv')
        professor_list = df[df['university_name'] == default_university]['professor_name'].unique()

        # Create selectbox for university with default value
        selected_university = st.selectbox("Select University", options=df['university_name'].unique(), index=df['university_name'].unique().tolist().index(default_university))

        # Filter professor list based on the selected university
        professor_list = df[df['university_name'] == selected_university]['professor_name'].unique()

        # Create selectbox for professor with default value
        professor_name_input = st.selectbox("Select Professor", options=professor_list, index=professor_list.tolist().index(default_professor))
        st.write('Please bear with us for a moment while we fetch the data!')
        st.markdown('---')
    st.subheader('📜Basic Info')
    image_url, prof_df, prof_chart, pub_df = prof_info(professor_name_input)
    col2, gap2, col3, gap3, col4 = st.columns([0.4,0.1, 1.2, 0.1, 1])

    with col2:
        st.write('\n')
        st.image(image_url, use_column_width=True)
    with col3:
        st.write('\n')
        st.write('\n')
        st.dataframe(prof_df)
    with col4:
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.altair_chart(prof_chart)
    

    st.subheader("📝 Most Cited Publications")
    st.write("Here are some of the most influential papers authored by this professor.")
    st.dataframe(pub_df)
    st.write('\n')

    st.subheader('🧐 Research Expertise')
    col1, col2 = st.columns([2,1])
    with col1:
        fig = profile_individual(str(selected_university), str(professor_name_input))
        st.plotly_chart(fig, use_container_width=True)

    
    st.subheader("👨🏼‍🤝‍👨🏽 Academic Collaborations")
    col1, col2 = st.columns([2,1])
    with col1:
        chart = find_network(professor_name_input)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("Summary: ")
    st.write("""Dr. Axel Guenther is a Full Professor in the Department of Mechanical and Industrial Engineering at the University of Toronto, with a cross-appointment at the Institute of Biomedical Engineering. He earned his doctoral degree from the Swiss Federal Institute of Technology (ETH) in Zurich and conducted postdoctoral research at the Massachusetts Institute of Technology (MIT). 
OQCORE.CA

Dr. Guenther's research focuses on microfluidics, biofabrication, and the development of micro/nanosystems for biomedical applications. His work includes the creation of organs-on-chips and the 2D and 3D printing of organized soft materials, such as engineered human tissue substitutes.
CRAFTMICROFLUIDICS.CA

Throughout his career, Dr. Guenther has received several prestigious awards, including the ETH Silver Medal (2002), the Ontario Early Researcher Award (2009), and the I.W. Smith Award from the Canadian Society of Mechanical Engineers (2010). He currently holds the Wallace G. Chalmers Chair of Engineering Design (2012–present). 
OQCORE.CA

In addition to his academic achievements, Dr. Guenther has published over 30 scientific papers and holds patents for three licensed technologies. He co-organizes the annual "Ontario-on-a-Chip" event, which focuses on microfluidics, microreactors, and labs-on-a-chip, fostering collaboration between university researchers and industry professionals in chemical, pharmaceutical, biotechnology, advanced materials, and analytical device sectors. 
OQCORE.CA

Dr. Guenther also serves as the Scientific Director of the Centre for Microfluidic Systems in Chemistry and Biology in Toronto, further advancing research in this field. """)

    
    st.markdown('<br>', unsafe_allow_html=True) 

    
    st.divider() 
    st.title("4. Compare the professor")


    col1, gap1, col2, gap2 = st.columns([1, 0.1, 2, 0.1])
    with col1:
        default_university_a_1 = "University of Toronto"
        default_professor_a_1 = "Axel Gunther"

        # Create selectbox for university with default value
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        selected_university_a_1 = st.selectbox(
            "Select the First University", 
            options=df['university_name'].unique(), 
            index=df['university_name'].unique().tolist().index(default_university_a_1),
            key='search_a_u1'
            )

        professor_list_a_1 = df[df['university_name'] == selected_university_a_1]['professor_name'].unique()

        # Create selectbox for professor with default value
        professor_name_input_a_1 = st.selectbox(
            "Select the First Professor", 
            options=professor_list_a_1, 
            index=professor_list.tolist().index(default_professor_a_1),
            key='search_a_p1'
            )
        st.write('\n')
        st.markdown('---')
        st.write('\n')
        default_university_a_2 = "University of Toronto"
        default_professor_a_2 = "Edmond Young"

        # Create selectbox for university with default value
        selected_university_a_2 = st.selectbox(
            "Select the Second University", 
            options=df['university_name'].unique(), 
            index=df['university_name'].unique().tolist().index(default_university_a_2),
            key='search_u2'
            )

        professor_list_a_2 = df[df['university_name'] == selected_university_a_2]['professor_name'].unique()

        # Create selectbox for professor with default value
        professor_name_input_a_2 = st.selectbox(
            "Select the First Professor", 
            options=professor_list_a_2, 
            index=professor_list.tolist().index(default_professor_a_2),
            key='search_a_p2',
        )
    
    with col2:
        fig_compare = compare_prof(
                selected_university_a_1, 
                professor_name_input_a_1, 
                selected_university_a_2, 
                professor_name_input_a_2)
        
        st.plotly_chart(fig_compare, use_container_width=True)

    st.divider()
    st.subheader("Ask about professors:")

    # Set up the input box for the user to ask questions
    user_question = st.text_input("Ask me anything about professors:")

    # Add a submit button
    if st.button("Submit"):
        # Simulated response (can be replaced with actual logic once RAG is implemented)
        if user_question:
            st.write(f"**You asked:** {user_question}")
            st.write("**Chatbot's response:**")
            
            # Here, you can add logic for predefined responses based on keywords
            # or placeholders while you work on implementing the RAG system.
            
            # Example responses:
            if "university ranking" in user_question.lower():
                st.write("The top universities vary by field of research. For example, 'University of Tokyo' excels in engineering.")
            elif "faculty size" in user_question.lower():
                st.write("Faculty sizes can vary across universities, depending on their research community size.")
            elif "publications" in user_question.lower():
                st.write("Publications per year often depend on the university's faculty research output.")
            else:
                st.write("I am currently gathering more information. Please check back soon!")
        else:
            st.write("Please enter a question to ask.")

    