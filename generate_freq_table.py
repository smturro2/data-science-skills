import numpy as np
import pandas as pd

def create_freq_table(desc):
    desc = desc.lower().replace("\n", " ").replace(")","").replace("(","").replace(",","").replace(".","")
    desc = desc.replace("!", "").replace("?","").replace("  "," ")
    list_of_words = desc.replace("\n","").split(" ")
    dict_of_words = pd.Series(list_of_words).value_counts()
    return pd.DataFrame(dict_of_words).T

if __name__ == "__main__":
    df_raw = pd.read_csv("raw.txt", sep="}")

    list_of_frames = [create_freq_table(d) for d in df_raw["desc"]]
    df_freq = pd.concat(list_of_frames)
    df_freq = df_freq.reset_index(drop=True).fillna(0)
    df_freq.to_csv("freq_table.csv",index=False)