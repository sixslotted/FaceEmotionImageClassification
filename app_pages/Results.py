import streamlit as st
import plotly.express as px
import pandas as pd

df = st.session_state.df

def Results():
    st.title("Results📊")
    st.write("Here we will display and discuss model performance.")

    # Result set selection
    ResultSet = ['Resized Images', 'Resized + Padded Images','Greyscale Resized Images']
    selected_result_set = st.selectbox(
        "Select a result set to view:",
        ResultSet,
    )

    #mappings
    imagePaths = {
        'Resized Images': 'Data/DashboardImages/ConfusionMatrixResized.png',
        'Resized + Padded Images': 'Data/DashboardImages/ConfusionMatrixResized+Padded.png',
        'Greyscale Resized Images': 'Data/DashboardImages/ConfusionMatrixGreyscale.png'
    }

    columnNames = {
        'Resized Images': 'ResizedPred',
        'Resized + Padded Images': 'PaddedPred',
        'Greyscale Resized Images': 'GreyPred'
    }

    col1, col2 = st.columns([1, 1])
    with col1:
        if selected_result_set:
            st.write("Confusion Matrix shows how well the model classified each emotion.")
            # Show confusion matrix
            st.image(imagePaths[selected_result_set], caption=selected_result_set)
            
    with col2:
        st.write("Sunburst chart shows distribution of predictions and misclassifications.Predictions in centre and correct category for misclassifications in outer ring.")
        # guard: ensure df and selected column exist
        pred_col = columnNames.get(selected_result_set)
        if pred_col not in df.columns:
            st.error(f"Predicted column '{pred_col}' not found in dataframe.")
            return

        # mapping ints -> readable names
        label_map = {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'pain', 5: 'sad'}

        # inner ring: total counts per predicted label
        pred_counts = df[pred_col].value_counts().sort_index()  # index = encoded label
        # build nodes for sunburst
        ids = []
        labels = []
        parents = []
        values = []

        # add predicted-label nodes (top-level)
        for label_int, cnt in pred_counts.items():
            pid = f"pred_{int(label_int)}"
            ids.append(pid)
            labels.append(label_map.get(int(label_int), str(label_int)))
            parents.append("")            # top-level
            values.append(int(cnt))

        # outer ring: misclassifications only -> for each predicted label, show true labels that produced that prediction
        df_incorrect = df.loc[df[pred_col] != df['True']]
        mis_group = df_incorrect.groupby([pred_col, 'True']).size().reset_index(name='count')

        for _, row in mis_group.iterrows():
            pred_v = int(row[pred_col])
            true_v = int(row['True'])
            cnt = int(row['count'])
            parent_id = f"pred_{pred_v}"
            child_id = f"mis_{pred_v}_{true_v}"
            ids.append(child_id)
            labels.append(label_map.get(true_v, str(true_v)))
            parents.append(parent_id)
            values.append(cnt)

        sun_df = pd.DataFrame({
            'id': ids,
            'label': labels,
            'parent': parents,
            'value': values
        })

        if sun_df.empty:
            st.info("No data available to plot.")
        else:
            fig = px.sunburst(
                sun_df,
                ids='id',
                names='label',
                parents='parent',
                values='value',
                branchvalues='total',
                title='Prediction Distribution and Misclassifications'
            )
            fig.update_layout(height=900)
            st.plotly_chart(fig, use_container_width=True)
