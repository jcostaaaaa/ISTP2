import pandas as pd

def sort():

    df = pd.read_csv("football_results.csv",on_bad_lines='skip')

    sorted_df = df.sort_values(by=["competition","home"], ascending=True)

    sorted_df.to_csv('football_resultsSort.csv', index=False)

