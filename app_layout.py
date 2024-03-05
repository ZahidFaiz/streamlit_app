# app_layout.py
import streamlit as st
import plotly.graph_objects as go

def apply_container_style():
    container_style = """
        <style>
            .blue-container {
                border: 1px solid #4472C4;
                background-color: #4472C4;
                padding: 10px;
                color: white;
                border-radius: 5px;
                text-align: center;
            }
        </style>
    """
    st.markdown(container_style, unsafe_allow_html=True)

def create_bar_chart(data, title):
    fig = go.Figure()

    for value_column in data.columns[1:]:
        fig.add_trace(go.Bar(
            x=data['Category'],
            y=data[value_column],
            text=data[value_column],
            name=value_column,
             marker_color='#5F84A2'
        ))

    fig.update_layout(barmode='stack', title=title, height=400,paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF')

    # Display the chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)

def create_pie_chart(data, labels_column, values_column, title):
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=data[labels_column],
        values=data[values_column],
        textinfo='percent+label' 
    ))

    fig.update_layout(title=title, height=400, showlegend=False, paper_bgcolor='#FFFFFF', plot_bgcolor='#FFFFFF')

    # Display the chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)