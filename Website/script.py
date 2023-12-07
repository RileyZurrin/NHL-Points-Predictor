import xgboost as xgb
import streamlit as st
import pandas as pd
import numpy as np
from clean_data import prepare_X

def main():

    # Read CSV
    df = pd.read_csv("data.csv")

    # Extract names and set index
    names = df.Name.values
    df.set_index("Name")

    # prepare data; first row is names
    X_pred = prepare_X(df)[:, 1:]

    # Load xgboost model
    gb = xgb.Booster({'nthread': 8})  # init model
    gb.load_model('model1')  # load data

    # Make predictions
    dpred = xgb.DMatrix(X_pred)
    ypred = np.round(gb.predict(dpred)).astype(int)

    # Create final DataFrame
    data_final = {"Player": names, "Projected Points": ypred}
    df_final = pd.DataFrame(data_final).sort_values("Projected Points", ascending=False)
    df_final.reset_index(drop=True, inplace=True)
    df_final.index += 1

    # Generate streamlit features
    st.title("NHL Points Predictions")

    # Display matching names in a selectbox
    selected_names = st.multiselect('Players:', names)

    # Create two columns
    col1, col2 = st.columns([4, 1])

    # Search Button
    if col1.button("Search"):
        filtered_df = df_final[df_final['Player'].isin(selected_names)]
    else:
        filtered_df = df_final

    col2.write("[Model Information](https://github.com/RileyZurrin/NHL-Points-Predictor/tree/main)")

    # Display the filtered DataFrame as a table
    st.table(filtered_df)

if __name__ == "__main__":
    main()







