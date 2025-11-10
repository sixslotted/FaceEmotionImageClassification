import streamlit as st

def CNN_info():
    st.write("Image classification - what approach?")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("In Multi layer perceptrons (MLPs) every neuron is connected to every neuron in the previous layer")
        st.image("Data/DashboardImages/mlp.png", caption="MLP Architecture")

    with col2:
        
        st.write("Convolutional Neural Networks (CNNs) are a class of deep learning models specifically designed for processing structured grid data, such as images. Each neuron is only connected to a small region of the previous layer allowing it to identify visual features wherever they are in the image making it more suitable for use in this project")
        st.image("Data/DashboardImages/cnn.png", caption="CNN Architecture")

