import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random



sales_data = pd.read_csv("file name")

#PLOT THE METRICS
def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)

#PLOT THE GAUGE
def plot_gauge(indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)


#PRESENT THE GRAPHS ON THE PAGE
def analyse_data():
    sales_data["Total_sales"] = sales_data["AveragePrice"]*sales_data["Total Volume"]
    total_sales = round(sales_data["Total_sales"].sum())
    average_rating = round(4.678495, 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    most_value_name = "Điện thoại Iphone14"
    most_value = 35000000

    #TOP ROW
    left, middle, right = st.columns(3)
    with left:
        plot_metric(
            "Total Sales",
            total_sales,
            prefix="VND",
            suffix="",
            show_graph=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )

        plot_gauge(1.6, "#0068C9", "", "Current Ratio", 3)
       
    with middle:
        plot_metric(
            most_value_name,
            most_value,
            prefix="VND",
            suffix="",
            show_graph=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )

        plot_gauge(10, "#FF8700", " days", "In Stock", 31)
       

    with right:
        
        plot_metric(
            "Average Rating",
            average_rating,
            prefix="",
            suffix="/5",
            show_graph=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )

        plot_gauge(28, "#29B09D", " days", "Delay", 31)
      
        
        
    st.markdown("-------")

    organic_data = sales_data[(sales_data['type'] == 'organic') & (sales_data['year'] >= 2017) & (sales_data['region'] != 'TotalUS')]
    region_stats = organic_data.groupby('region')['Total Volume'].agg(['sum', 'median', 'std'])


    # Get the 5 regions with the highest Total Volume and extract their data.
    top_regions = region_stats.nlargest(5, 'sum').index
    top_data = organic_data[organic_data['region'].isin(top_regions)]

    # Create a bar plot showing the mean, median, and standard deviation of the Total Volume 
    top_data_stats = top_data.groupby('region')['Total Volume'].agg(['mean', 'median', 'std'])
    fig_product_sales = px.bar(top_data_stats,y =['mean', 'median', 'std']  )
    
    #Pie chart 
    bags_data = sales_data[sales_data["region"] == "Albany"]
    total_small_bags = bags_data["Small Bags"].sum()
    total_large_bags = bags_data["Large Bags"].sum()
    fig_stock_sold = px.pie(bags_data, values=[total_small_bags, total_large_bags], names=["small bags", "large bags"])

    #BOTTOM ROW
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(fig_product_sales, use_container_width=True)
    with right_column:

        st.plotly_chart(fig_stock_sold)

    

analyse_data()