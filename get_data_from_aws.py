import pandas as pd
import boto3
import numpy as np

num_rows = 1100
max_columns = 16000

# client = boto3.client('dynamodb')
# dynamodb = boto3.resource('dynamodb')
# dynamo_table = dynamodb.Table('data-science-skills-2')
#
#
# dfs = []
# for i in range(num_rows):
#     response = dynamo_table.get_item(Key={'job_id': str(i)})
#     dfs.append(pd.DataFrame(response["Item"], index=[i]))
#     print(f"Got {len(dfs)} items")
#
# print("Saving ",end="")
# df = pd.concat(dfs)


df = pd.read_csv("loaded_data.csv")

df = df.loc[:,["job_info__" not in c for c in df.columns]]
df = df.select_dtypes(include=np.number)
col_sums = df.sum(axis=0)
col_sums = col_sums.sort_values(ascending=False)

col_sums = col_sums[col_sums>50]
df = df[list(col_sums.index)]

columns_to_keep = ['python','data','sql','sql:','r','excel','java','sas','javascript','c++','matlab', 'linux', 'pandas', 'c#','c','experience','analysis','analyzing', 'analytic',
                   'analysts','analytics','analyst','analytical','analyze','analyses','statistics','statistical','mathematics','math','mathematical','physics','technical','technology',
                   'technologies','quantitative','research','development','solutions','software','engineering','design','designed', 'management','operations','scientific','intellectual',
                   'smart','presenting','algorithms','database','databases', 'datasets','model','models','modeling','predictive','pipelines','pipeline', 'trends','functions',
                   'visualization','visualizations','reporting','reports', 'dashboards','automate','automation','optimization','documentation', 'coding','patterns','ai', 'artificial',
                   'scripting','scripts','computing','computational','queries','structures','ml','frameworks', 'regression','validation','validate','apis','api','forecasting',
                   'classification','transforming','storage','workflows','tables','framework', 'libraries','self-motivated','debugging','querying','professional','team','communication',
                   'communicate', 'communications', 'communicating','create','creative','creativity','competitive','independently', 'independent','successful','unique','collaborative',
                   'collaboration','verbal','problem-solving','solving', 'leadership', 'ideas','strategic','strategies','actionable','organizational','interpersonal','data-driven',
                   'accuracy', 'integrity','operational','functional','flexibility', 'presentation', 'cross-functional','curious', 'empower','cutting-edge','details',
                   'rigorous','cloud','cloud-based', 'tableau','aws', 'microsoft','ms','google','azure', 'ibm','amazon','hadoop','git','apple','snowflake','powerbi','spss','powerpoint',
                   'stakeholders','financial','risk','economic','economics','finance','trading', 'portfolio', 'consulting','compliance', 'options','fraud','capital','bank','stock',
                   'bachelor’s',"bachelor's",'bachelors', 'bs', 'master’s',"master's",'graduate','phd','401k','dental', 'healthcare','tuition', 'religious','reimbursement','retirement',
                   'pregnancy','tuition', 'vacation','pto','pricing','qualifications','qualifications:', 'experiences', 'pay', 'compensation','experience:', 'salary', 'benefits:','pay:',
                   'requirements:','education:','skills:','remotely','remote','vaccination','vaccine','vaccinated','covid-19', 'covid','criminal','francisco','tiktok','colorado','boston',
                   'washington','apprenticeship','contractor','startup','insurance',"medical","law",'york',"investment","spark","nike","california",'manufacturing',"weather"]

# Combine columns
df = df[columns_to_keep]
df["sql"] = df["sql"] + df["sql:"]
df = df.drop(columns=["sql:"])
df["analytics"] = df['analysis']+df['analyzing']+df['analytic']+df['analysts']+df['analytics']+df['analyst']+df['analytical']+df['analyze']+df['analyses']
df = df.drop(columns=['analysis','analyzing', 'analytic','analysts','analyst','analytical','analyze','analyses',])
df["statistics"] = df["statistics"] + df["statistical"]
df["Statistics"] = df["statistics"]
df["mathematics"] = df["mathematics"] + df["math"] + df["mathematical"]
df["Mathematics"] = df["mathematics"]
df["Physics"] = df["physics"]
df["Engineering"] = df["engineering"]
df["technology"] = df["technology"] + df["technologies"]
df["design"] = df["design"] + df["designed"]
df["presentation"] = df["presentation"] + df["presenting"]
df["databases"] = df["databases"] + df["database"] + df["structures"] + df["storage"]
df["modeling"] = df["modeling"] + df["model"] + df["models"]
df["pipelines"] = df["pipelines"] + df["pipeline"]
df["visualization"] = df["visualization"] + df["visualizations"]
df["reporting"] = df["reporting"] + df["reports"]
df["ai"] = df["ai"] + df["artificial"]
df["scripting"] = df["scripting"] + df["scripts"] + df["automate"] + df["automation"]
df["computing"] = df["computing"] + df["computational"]
df["validation"] = df["validation"] + df["validate"]
df["apis"] = df["apis"] + df["api"]
df["frameworks"] = df["frameworks"] + df["framework"] + df["libraries"]
df["queries"] = df["queries"] + df["querying"]
df["new-york"] = df["york"]
df = df.drop(columns=["statistical",'math',"mathematical","technologies","designed","presenting","database","structures",'storage',"model","models","pipeline","visualizations",
                      "reports","artificial","automation","scripts","automate","computational","validate","api","framework","libraries","querying",'york'])

df["communication"] = df['communication']+df['communicate']+df[ 'communications']+df['communicating'] + df['verbal']
df["creativity"] = df['creativity']+df['creative']+df['create']
df["independent"] = df["independent"] + df["independently"]
df["collaborative"] = df["collaborative"] + df["collaboration"]
df["problem-solving"] = df["problem-solving"] + df["solving"]
df["strategic"] = df["strategic"] + df["strategies"]
df["smart"] = df["smart"] + df["intellectual"]
df = df.drop(columns=['communicate', 'communications','communicating',"verbal",'create','creative','independently',
                      "solving","strategies","intellectual","collaboration"])

df["cloud"] = df["cloud"] + df["cloud-based"]
df["microsoft"] = df["microsoft"] + df["ms"]
df["economics"] = df["economics"] + df["economic"]
df["finance"] = df["finance"] + df["financial"]
df["Finance"] = df["finance"]
df["Economics"] = df["economics"]
df["bachelors"] = df['bachelor’s']+df["bachelor's"]+df['bachelors']+df['bs']
df["masters"] = df["master’s"] + df["master's"]
df["qualifications"] = df["qualifications"] + df["qualifications:"]
df["experience"] = df["experience"]+df["experience:"] + df["experiences"]
df["salary"] = df["salary"]+df["pay"] + df["pay:"]
df['benefits'] = df['benefits:']
df['requirements'] = df['requirements:']
df['education'] = df['education:'] + df['bachelor’s']+df["bachelor's"]+df['bachelors']+df[ 'bs']+df[ 'master’s']+df["master's"]+df['graduate']+df['phd']
df['skills'] = df['skills:']
df['remote'] = df['remote']+df['remotely']
df['san-francisco'] = df['francisco']
df = df.drop(columns=["cloud-based","ms","economic","financial",'bachelor’s',"bachelor's",'bs','master’s',"master's","qualifications:",'experiences','experience:','pay','pay:',
                      'benefits:','requirements:','education:','skills:','remotely',"francisco"])


df.to_csv("loaded_data_cleaned.csv",index=False)

df_condensed = pd.DataFrame()
df_condensed["total_references"] = df.sum(axis=0)
df_condensed["num_jobs"] = (df != 0).sum(axis=0)
df_condensed["percent_jobs"] = df_condensed["num_jobs"] / num_rows

# sort words into categories
df_condensed["category"] = ""
words = ['python','data']
category = "Main Search Terms"
df_condensed.loc[words,"category"] = category


words = ['sql','r','excel','java','sas','javascript','c++','matlab', 'linux', 'pandas', 'c#','c',]
category = "Programming languages"
df_condensed.loc[words,"category"] = category


words = ['experience','analytics','statistics','mathematics','physics','technical','quantitative',
         'research','development','solutions','software','engineering','design','management','operations',
         'scientific','smart','presentation']
category = "Hard Skills"
df_condensed.loc[words,"category"] = category


words = ['algorithms','databases','modeling','predictive','pipelines', "datasets",'trends','functions','visualization','reporting','dashboards',
         'optimization','documentation', 'coding','patterns','ai','scripting','computing','queries','ml','frameworks','regression',
         'validation','apis','forecasting','classification','transforming','workflows','tables','debugging','technology']
category = "Technical Skills"
df_condensed.loc[words,"category"] = category


words = ['professional','team','communication','creativity','competitive','independent','successful','unique','collaborative','problem-solving',
         'leadership', 'ideas','strategic','actionable','organizational','interpersonal','data-driven', 'accuracy', 'integrity','operational',
         'functional','flexibility','cross-functional','curious', 'empower','cutting-edge','details','self-motivated','rigorous']
category = "Soft Skills"
df_condensed.loc[words,"category"] = category


words = ['cloud', 'tableau','aws', 'microsoft','google','azure', 'ibm','amazon','hadoop','git','apple','snowflake','powerbi','spss','powerpoint','spark']
category = "Software Tools"
df_condensed.loc[words,"category"] = category


words = ['stakeholders','risk','economics','finance','trading', 'portfolio','consulting','compliance', 'options','fraud','capital','bank','stock','pricing',"investment"]
category = "Financial Terms"
df_condensed.loc[words,"category"] = category


words = ['bachelors', 'masters','graduate','phd']
category = "Degrees"
df_condensed.loc[words,"category"] = category


words = ['401k','dental', 'healthcare','tuition', 'religious','reimbursement','retirement','pregnancy','tuition', 'vacation','pto','compensation','insurance',"medical"]
category = "Job Benefits"
df_condensed.loc[words,"category"] = category


words = ['qualifications', 'experience','salary', 'benefits','requirements','education','skills']
category = "Job Requirements"
df_condensed.loc[words,"category"] = category


words = ['vaccination','vaccine','vaccinated','covid-19', 'covid']
category = "Covid References"
df_condensed.loc[words,"category"] = category


words = ['criminal','tiktok',"law","nike","weather"]
category = "Other Terms"
df_condensed.loc[words,"category"] = category

words = ['san-francisco','colorado','boston','washington',"california","new-york"]
category = "Locations"
df_condensed.loc[words,"category"] = category


words = ['apprenticeship','contractor','startup',"remote",'manufacturing']
category = "Job Type"
df_condensed.loc[words,"category"] = category


words = ["Statistics","Mathematics","Physics","Engineering","Economics","Finance"]
category = "Majors"
df_condensed.loc[words,"category"] = category


df_condensed.to_csv("condensed_data.csv",index=True)

