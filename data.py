

##################################################Data Concatation##############################################################

import pandas as pd
import glob

path = r'F:\project\projectfinal\Project' # use your path

#featch the csv files
all_files = glob.glob(path + "/*.csv")

li = []

#concate the files
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)
   

frame = pd.concat(li, axis=0, ignore_index=True,sort=False)
frame=frame.iloc[:,0:13]
frame1=frame.to_csv(r"F:\project\projectfinal\Project\final_data1year.csv")


##################################################extract companiwise data##########################################################
# loading 1 year data of all the commpanies

frame=pd.read_csv(r"F:\project\projectfinal\Project\final_data1year.csv")
frame=frame.iloc[:,1:14]

col=[]
for i in frame:
    col.append(i)

#seperate out the companies names
companies=[]
for j in frame['SYMBOL']:
    if j not in companies:
        companies.append(j)
        
length=len(companies) 

path1 = 'F:\project\projectfinal\Project'
    
lst=[]

#create company wise csv file
for j in range(0,length):
    for i in frame.index:
          
        if frame['SYMBOL'][i] == companies[j]:
            a=frame['SYMBOL'][i],frame['SERIES'][i],frame['OPEN'][i],frame['HIGH'][i],frame['LOW'][i],frame['CLOSE'][i],frame['LAST'][i],frame['PREVCLOSE'][i],frame['TOTTRDQTY'][i],frame['TOTTRDVAL'][i],frame['TIMESTAMP'][i],frame['TOTALTRADES'][i],frame['ISIN'][i]
            lst.append(a)
            data = pd.DataFrame(lst,columns=col)
            #data[order(as.Date(data['TIMESTAMP'], format="%d/%m/%Y")),]
            data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], infer_datetime_format=True,format="%d/%m/%Y")
            data = data.sort_values(by='TIMESTAMP',ascending=True)
            data1=data.to_csv(path1 +f"{companies[j]}.csv")
            
    lst.clear()
   



