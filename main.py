import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 


st.title("My EDA Dashboard")
st.write("Upload a CSV file to begin.")
uploaded_file = st.file_uploader("Choose a CSV file", type = "csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!.")  #st.success is used in streamlit while print() is useless in it. st.success is shown by green box
    
    st.subheader("First 10 Rows.")   
    st.dataframe(df.head(10))
    
    st.subheader("Statistics")
    numeric_cols = df.select_dtypes(include = 'number').columns.tolist()
    
    if len(numeric_cols) > 0:
        st.dataframe(df[numeric_cols].describe())
    else:
        st.warning("No numeric columns found.")

    st.subheader("Visualizations")
    if numeric_cols:
        selected_col = st.selectbox("Select column for histogram", numeric_cols)

        fig, ax = plt.subplots(figsize = (8,4))
        ax.hist(df[selected_col].dropna(), bins=20, color='steelblue', edgecolor='black')
        ax.set_title(f'Distribution of {selected_col}')
        st.pyplot(fig)

    else:
        st.warning("No numeric columns found in this dataset.") 
            

    st.subheader("Boxplot")
    if numeric_cols:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df[numeric_cols], ax=ax)
        ax.set_title("Boxplot of Numeric Columns")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found in this dataset.")

    st.subheader("Correlation Heatmap")
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
    
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)
    else:
        st.warning("Need at least 2 numeric columns for heatmap.") 

    st.subheader("Scatter Plot")
    if len(numeric_cols)>1:
        col_x = st.selectbox("X-Axis column",numeric_cols, key = "scatter_x")
        col_y = st.selectbox("Y-Axis column", numeric_cols, key = "scatter_y")
        fig, ax = plt.subplots(figsize=(8,4))
        ax.scatter(df[col_x], df[col_y], alpha =0.6, color = 'coral')
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.set_title(f"{col_x} vs {col_y}")
        st.pyplot(fig)
    else:
        st.warning("Need at least 2 numeric columns for scatter plot.")

    st.subheader("Bar Chart")
    cat_col = df.select_dtypes(include = 'object').columns.tolist()
    
    if len(cat_col)>0:
        selected = st.selectbox("Select categorical column", cat_col, key= "bar_col")
        counts = df[selected].value_counts().head(10)
        fig,ax = plt.subplots(figsize = (8,4))
        counts.plot(kind = 'bar', color = 'mediumseagreen', ax=ax)
        ax.set_title(f"Top 10 values in {selected}")
        plt.xticks(rotation = 45)
        st.pyplot(fig)

    else:
        st.warning("No categorical columns found.")

    st.subheader("Auto Insights")
    # Insight 1 
    missing = df.isnull().sum()
    if missing.sum() >0:
        top_missing = missing.idxmax() #Index of maximum number
        st.write(f"⚠️ Column **{top_missing}** has the most missing values ({missing.max()}).")
    else:
        st.write("✅ No missing values in the dataset.")

    if len(numeric_cols) > 1:
        
        corr_matrix = df[numeric_cols].corr().abs()
        corr_array = corr_matrix.to_numpy().copy()           # ← copy banao
        np.fill_diagonal(corr_array, 0)                       # ← copy pe kaam karo
        corr_matrix = pd.DataFrame(corr_array, index=corr_matrix.index, columns=corr_matrix.columns)  # ← naya DataFrame
                            
        max_pair = corr_matrix.unstack().idxmax()
        max_val = corr_matrix.unstack().max()
        
        st.write(f"📈 Strongest correlation: **{max_pair[0]}** and **{max_pair[1]}** ({max_val:.2f}).")
    else:
        st.write("⏭️ Skipping correlation (need at least 2 numeric columns).")
      

    if numeric_cols:
        Q1 = df[numeric_cols].quantile(0.25)
        Q3 = df[numeric_cols].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[numeric_cols] < (Q1 - 1.5 * IQR)) | (df[numeric_cols] > (Q3 + 1.5 * IQR))).sum().sum()
        st.write(f"🔍 Total outliers detected: **{outliers}** (using IQR method).")
    else:
        st.write("⏭️ Skipping correlation (need at least 2 numeric columns).")
 
 
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}") # [0]axis --> Rows, [1]axis ---> Columns
else:
    st.info("File is not available.")  #st.info is shown by blue box , st.warning() --> yellow box, st.error() --> red box