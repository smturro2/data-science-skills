import pandas as pd
import boto3

df_raw = pd.read_csv("raw.txt", sep="}",dtype=str)
df_raw = df_raw.drop(columns=["salary","desc","link"])
df_raw.columns = "job_info__" + df_raw.columns
df_raw = df_raw.fillna("")
df_freq_table = pd.read_csv("freq_table.csv",dtype=int)
# Filter freq_table
common_words = pd.read_csv("list_of_common_words.txt",header=None)
common_words = list(common_words.T[0].dropna().unique())
common_words = [x.lower() for x in common_words]
common_words = list(set(common_words).intersection(set(df_freq_table.columns)))
df_freq_table = df_freq_table.drop(columns=common_words)
common_words = []
for c in df_freq_table.columns:
    try:
        c_num = float(c)
        common_words.append(c)
    except:
        if "$" in c \
                or "@" in c \
                or "®" in c \
                or "http:" in c \
                or "www" in c:
            common_words.append(c)
        else:
            try:
                c_date = pd.to_datetime(c)
                common_words.append(c)
            except:
                pass
df_freq_table = df_freq_table.drop(columns=common_words)

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
dynamo_table = dynamodb.Table('data-science-skills-2')

df_combined = pd.concat([df_raw,df_freq_table],axis=1)
for index, row in df_combined.iterrows():
    if index >=0:
        row = row.dropna()
        row = row[row != ""]
        row = row[row != 0]
        chunk = row.to_dict()
        chunk["job_id"] = str(index)
        dynamo_table.put_item(Item=chunk)
        print(f"inputted job_id: {index}")