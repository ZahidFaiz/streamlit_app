# main_app.py
import streamlit as st
import plotly.graph_objects as go
from app_layout import apply_container_style, create_bar_chart, create_pie_chart
# from data_processing import *
from authenticate import *
from data_processing import data_prep
import pandas as pd
import plotly.express as px





def main():
    
    plot_bg_color = '#FFFFFF'
    # Load the dummy DataFrame from the CSV file
    dp = data_prep("temp.csv")

    title_container_style = """
        <style>
            .green-title-container {
                background-color: #FFFFFF;
                padding: 20px;
                color: #000000;
                border-radius: 5px;
                margin-bottom: 20px;
                text-align: center;
                font-size: 35px;
                font-weight: bold;
            }
        </style>
    """

    # Apply the style to the page
    st.markdown(title_container_style, unsafe_allow_html=True)

    # Add content to the title container
    st.markdown("<div class='green-title-container'>ZS DS3 MedTech Solution</div>", unsafe_allow_html=True)

    # Add separator lines in the sidebar
    separator_style = """
    <style>
        .separator {
            margin-top: 10px;
            margin-bottom: 10px;
            border-top: 1px solid #ddd;
        }
    </style>
    """
    st.sidebar.markdown(separator_style, unsafe_allow_html=True)
    st.sidebar.header("Filters")

    # Create dynamic filters based on DataFrame columns
    df = dp.df
    filters = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # Add sliders for numeric columns
            min_value = df[column].min()
            max_value = df[column].max()
            default_value = (min_value, max_value)
            filters[column] = st.sidebar.slider(f"Select {column} Range", min_value, max_value, default_value)
            st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        else:
            all_categories = df[column].unique()
            filters[column] = st.sidebar.multiselect(f"Select {column}", all_categories, default=all_categories)
            st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)


    # Display the loaded DataFrame based on filters
    filtered_df = dp.apply_filters(filters)

    # Set the background color using inline CSS
    filter_bg_color = """
        <style>
            [data-testid=stAppViewContainer] {
                background: #EEF0F4; 
            }
            [data-testid=stSidebarUserContent] {
                background: #FFFFFF;
            }
           
        </style>
    """
    st.markdown(filter_bg_color, unsafe_allow_html=True)

    # Create four containers in four columns
    col1, col2, col3, col4 = st.columns(4)
    # Define the style for the containers
    container_style = """
        <style>
            .blue-container {
                border: 1px solid #21345C;
                background-color: #21345C;
                padding: 10px;
                color: #FFFFFF;
                border-radius: 5px;
                text-align: center;
                font-size: 20px;
            }
        </style>
    """

    # Apply the style to the page
    st.markdown(container_style, unsafe_allow_html=True)
    # Add content to each container
    with col1:
        st.markdown("<div class='blue-container'>Total Claims Volume: {}</div>".format(filtered_df['Claims volume'].sum()), unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='blue-container'>Total Patient Volume: {}</div>".format(filtered_df['Patient Count'].sum()), unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='blue-container'>Total HCP Volume: {}</div>".format(filtered_df['HCP Count'].sum()), unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='blue-container'>Total Market Products: {}</div>".format(filtered_df['Product Name'].nunique()), unsafe_allow_html=True)

    container = st.container(border=True)

    filtered_df = dp.bar_chart1_df()

    selected_category = container.selectbox("Select Product", filtered_df['Product Name'].unique().tolist())

    plt_df = filtered_df[filtered_df["Product Name"] == selected_category]
    fig = go.Figure()
    fig.add_trace(
               go.Bar(x=plt_df['Time Period'], y=plt_df['Patient Count'],
                      text=plt_df['Patient Count'], name="Patient Count",marker_color='#5F84A2')
            )
    
    fig.add_trace(
               go.Scatter(x=plt_df['Time Period'], y=plt_df['Claims volume'],
                      text=plt_df['Claims volume'], mode='lines',marker_color='#BF9000', name='Claims volume')
            )
        
    # Define the layout
    fig.update_layout(
            title=' XYZ Claims / Patient Uptake vs Time',
            xaxis=dict(title='Time Period'),
            paper_bgcolor=plot_bg_color, plot_bgcolor=plot_bg_color,
            showlegend=True
        )
    
    
    container.plotly_chart(fig, use_container_width=True, className="stPlot")

    container = st.container(border=True)

    col1, col2, col3 = container.columns(3)
    with col1:

        # Placeholder for the main bar chart in the first row
        plt_df = dp.bar_chart2_df()
        main_bar_chart = go.Figure(go.Bar(x=plt_df['Geography Location'], y=plt_df['Patient Count'], text=plt_df['Patient Count'], name="Main Bar Chart",marker_color='#5F84A2'))
        st.plotly_chart(main_bar_chart.update_layout(showlegend=False, title = 'Top 10 States by XYZ patients',xaxis=dict(title='Geography Location'),
                                                     yaxis=dict(title='# Patients'),
                                                     paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF'),
                         use_container_width=True, className="stPlot")

    with col2:

        plt_df = dp.bar_chart3_df()
        main_bar_chart = go.Figure(go.Bar(x=plt_df['Patient Age'], y=plt_df['Patient Count'], text=plt_df['Patient Count'], name="Main Bar Chart",marker_color='#5F84A2'))
        st.plotly_chart(main_bar_chart.update_layout(showlegend=False, title = 'XYZ patients Age split',xaxis=dict(title='Patient Age'),
                                                     yaxis=dict(title='# Patients'),
                                                     paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF'),
                         use_container_width=True, className="stPlot")
    with col3:
        filtered_df = dp.pie_chart3_df()
        create_pie_chart(filtered_df, 'Patient Gender', 'Patient Count', 'XYZ Patient Gender Split')

    # data = {
    #     'Category': ['A', 'B', 'C'],
    #     'Value1': [10, 60, 30],
    #     'Value2': [60, 20, 30],
    #     'Value3': [30, 20, 40]
    # }
    # data = pd.DataFrame(data)
    container = st.container(border=True)
    color_sc = ['rgb(198,219,239)',
            'rgb(158,202,225)',
            'rgb(107,174,214)',
            'rgb(66,146,198)',
            'rgb(33,113,181)',
            'rgb(8,81,156)',
            'rgb(8,48,107)']
    col1, col2 = container.columns(2)
    with col1:
        data = dp.st_bar_chart1_df()
        fig = go.Figure()

        for value_column in data.columns[1:]:
            fig.add_trace(go.Bar(
                x=data['Time Period'],
                y=data[value_column],
                name=value_column,
                marker=dict(color=data[value_column], colorscale=color_sc)
            ))

        fig.update_layout(barmode='stack', xaxis=dict(title='Time Period'),
                                                     yaxis=dict(title='% Claims'),title=" XYZ Claims Share", height=400)

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        # Create a stacked bar chart using Plotly graph objects
        data = dp.st_bar_chart2_df()
        fig = go.Figure()

        for value_column in data.columns[1:]:
            fig.add_trace(go.Bar(
                x=data['Time Period'],
                y=data[value_column],
                name=value_column,
                marker=dict(color=data[value_column], colorscale=color_sc)
            ))

        fig.update_layout(barmode='stack', xaxis=dict(title='Time Period'),
                                                     yaxis=dict(title='% Patients'),title=" XYZ Patient Share", height=400)

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(layout="wide")

    check = check_password()

    if check == True:
        main()

