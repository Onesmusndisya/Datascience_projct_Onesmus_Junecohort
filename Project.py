##Required libraries
import time
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

## The project name
st.title("Site Build Acceptance Predictions-SBAP")

##Problem defination

st.header("Problem Defination")
st.write("In today’s competitive Telecommunication industry, implementing a new project is a significant investment for any contractor. However, predicting how well the project will be accepted by customer remains a challenge. Several factors—ranging from quality, Security, Community concerns, Poor Weather conditions—contribute to the delay in the project acceptance. Accurately predicting project acceptance timelines based on historic data can help companies fine-tune their strategies and make informed decisions before, during and after actual implementation, ultimately saving costs and continuously improving customer satisfaction.")

##Objective of the project
st.header("Objective")
st.write("The objective of this project is to develop a predictive model to assess the likelihood of contractor scope acceptance by the customer within the contracted timelines leveraging on historical data from previous projects, customer feedback and market trends, the goal is to provide visibility of how long it will take from allocation to final acceptance and highlight key factors that may cause delayed acceptance.")

##Key milestone Flow Chart
st.subheader("Key Milestones:")
st.image("Key_Milestones_flowchart.png",use_column_width=True)


##Project Manager details
name=st.text_input("Enter name of the project  Manager:","Type here")
    ##Read the Excel file
df = pd.read_excel('Historic_details.xlsx')

    ## Display some data
st.write("Historic_details.xlsx", df.head())



    ##Format date column to datetime.
df['Start Date'] = pd.to_datetime(df['Start Date'])
df['FAC Date'] = pd.to_datetime(df['FAC Date'])

    ##Project life span
if 'Project life-days' not in df.columns:
        df['Project life-days'] = (df['FAC Date'] - df['Start Date']).dt.days
    
    ##Group the data by Client and Project Scope to find the average project life
grouped_df = df.groupby(['Client', 'Project Scope Description','Region'])['Project life-days'].mean().reset_index()

    ##User Input to allow predictions
st.subheader("New Projects Prediction")

    ##Select Client from the selection box.
client = st.selectbox("Select Client", df['Client'].unique())

    ##Select Region from the selection box.
Region = st.selectbox("Select Region", df['Region'].unique())

    ##Select New Scope allocated by main Client.
scope = st.selectbox("Select Project Scope Description", df['Project Scope Description'].unique())

    ##Select New project start date.
start_date = st.date_input("Select Start Date for the New Project")

if client and scope and start_date and Region:
        ##Filter the historical data to get the average project life
        filtered_df = df[(df['Client'] == client) & (df['Project Scope Description'] == scope) & (df['Region'] == Region)]
        filtered_row = grouped_df[(grouped_df['Client'] == client) & 
                                  (grouped_df['Project Scope Description'] == scope) & (grouped_df['Region'] == Region)]
        
        if not filtered_row.empty:
            avg_project_life = filtered_row['Project life-days'].values[0]
            
            ##Predict the FAC Date
            predicted_fac_date = pd.to_datetime(start_date) + pd.Timedelta(days=avg_project_life)
  
st.subheader("Progress Bar")
progress=st.progress(0)
for i in range(100):
 progress.progress(i+1)
time.sleep(0.1)
           
 ##Display the results
st.write(f"Predicted Project Life: {avg_project_life:.2f} days")
st.write(f"Predicted FAC Date: {predicted_fac_date.date()}")
            
##Historic data trend for the selected Scope,Client and Region
##Project Life Historic Trend using matplotlib
st.header("Project Life Historic Trend")

##The data
chart_data = filtered_df[['Start Date', 'Project life-days']].set_index('Start Date')

## Create a bar chart using matplotlib
fig, ax = plt.subplots()
chart_data.plot(kind='bar', ax=ax)

##Label the axes
ax.set_xlabel("Start Date")
ax.set_ylabel("Project Life (Days)")
ax.set_title("Project Life Historic Trend")

##Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

##Display the plot in Streamlit
st.pyplot(fig)

##Violin Visualisation
st.write("Violin Plot of Project life-days")
plt.figure(figsize=(10, 6))
sns.violinplot(x=filtered_df['Project life-days'])
plt.title('Violin Plot of Project life-days')
plt.xlabel('Project life-days')
st.pyplot(plt)


st.header("The Conclusion & Recommendations")

st.write(f"1. The newly allocated scope by the customer as detailed above will take  {avg_project_life:.2f} days from start to Final acceptance.") 
st.write(f"2. The Final project invoicing will be done on: {predicted_fac_date.date()}")
st.write(" 3. Executive approval/guidance is  required  before the project  kick off with the above consinderations in mind")
st.write(" 4. This Report should be printed and submitted to the board/Executive team for Strategic guidance.")

st.header("Project Owner")
st.write("Name:        Onesmus Ndisya")
st.write("Designation: Group Finance and Cost Control Manager")
st.write("Email:       Onesmusndisya@gmail.com")
st.write("Contact:     254701122723")