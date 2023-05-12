import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
st.set_option("deprecation.showPyplotGlobalUse", False)

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above. 

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required 

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

st.title("Census Data Visualisation Web App")
st.sidebar.title("Exploratory Data Analysis")

if st.sidebar.checkbox("Show Raw Data"):
	st.subheader("Census Data Set")
	st.dataframe(census_df)
	st.write(f"Number of Rows: {census_df.shape[0]}")
	st.write(f"Number of Columns: {census_df.shape[1]}")
st.sidebar.title("Visulaisation Section")
selection = st.sidebar.multiselect("Visualisation selection", ("income", "gender", "workclass"))
plot_list = st.sidebar.multiselect("Select the Charts/Plots", ("Pie", "Box Plot", "Count Plot"))
for i in plot_list:
	for j in selection:
		if "Pie" in i:
			gender_label = ["Male", "Female"]
			gender_exp = [0.08, 0.08]
			workclass_label = ["Private", "Self-emp-not-inc", "Local-gov", "State-gov", "Self-emp-inc", "Federal-gov", "Without-pay"]
			workclass_exp = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
			income_label = ["<=50k", ">=50k"]
			income_exp = [0.08, 0.08]
			if j == "workclass":
				st.subheader("Pie Chart")
				st.title(f"Distribution of records for different {j} groups")
				plt.figure(figsize = (10,7))
				plt.pie(census_df[j].value_counts(), labels = workclass_label, explode = workclass_exp, autopct = "%.2f%%")
				st.pyplot()
			elif j == "income":
				st.subheader("Pie Chart")
				st.title(f"Distribution of records for different {j} groups")
				plt.figure(figsize = (10,7))
				plt.pie(census_df[j].value_counts(), labels = income_label, explode = income_exp, autopct = "%.2f%%")
				st.pyplot()
			else:
				st.subheader("Pie Chart")
				st.title(f"Distribution of records for different {j} groups")
				plt.figure(figsize = (10,7))
				plt.pie(census_df[j].value_counts(), labels = gender_label, explode = gender_exp, autopct = "%.2f%%")
				st.pyplot()
		elif "Box Plot" in i:
			st.title(f"Box Plot for the hours worked per week by {j}")
			plt.figure(figsize = (10,7))
			sns.boxplot(x = census_df["hours-per-week"], y = census_df[j])
			st.pyplot()
		else:
			st.title(f"Count plot for distribution of records for unique workclass groups and {j} groups")
			plt.figure(figsize = (10,7))
			sns.countplot(x = census_df["workclass"], hue = census_df[j])
			st.pyplot()