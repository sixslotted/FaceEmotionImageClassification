import streamlit as st
import plotly.express as px

df = st.session_state.df
#df_byBrand = df_CarPriceCSV[['carBrand', 'price']].groupby('carBrand').mean().astype(int).reset_index()
#df_byBrand = df_byBrand.sort_values(by='price', ascending=False)

def Results():
    st.title("Results📊")
    st.write("Here we will display and discuss model performance.")

    # Result set selection
    ResultSet = ['Resized Images', 'Resized + Padded Images','Greyscale Resized Images']
    selected_result_set = st.selectbox(
        "Select a result set to view:",
        ResultSet,
    )

    # Standardize histogram bins and range

    col1, col2 = st.columns([1, 1])
    with col1:
        if selected_result_set:

            imagePaths = {
                'Resized Images': 'Data/DashboardImages/ConfusionMatrixResized.png',
                'Resized + Padded Images': 'Data/DashboardImages/ConfusionMatrixResized+Padded.png',
                'Greyscale Resized Images': 'Data/DashboardImages/ConfusionMatrixGreyscale.png'
            }

            img_path = imagePaths[selected_result_set]
            st.write("Confusion Matrix shows how well the model classified each emotion.")
            # Show confusion matrix
            st.image(img_path, caption=selected_result_set)
            
    with col2:
        st.write('placeholder')
