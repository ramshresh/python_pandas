import pandas as pd
import re

excel_file_drr = r"C:\learn2code\desinventar\DRR-Portal 7Jan2019.xlsx"
excel_file_des = r"C:\learn2code\desinventar\DesInventar-2018-2019.xlsx"

drr = pd.read_excel(excel_file_drr, "2018-2019")
des = pd.read_excel(excel_file_des, "Worksheet")

drr_dist_list = drr['VDC/Municipality'].unique()
des_dist_list = des['Localbody'].unique()

print (drr['VDC/Municipality'].unique())
print (des['Localbody'].unique())

matched = []
not_matched = []

#Create a DataFrame object
dfObj = pd.DataFrame([], columns = ['VDC/Municipality' , 'Localbody'], index=['a', 'b'])

for des_dist in des_dist_list:
    df_drr = drr[(drr['VDC/Municipality'].str.contains(str(des_dist), na=False))]
    if  df_drr.shape[0] > 0:
        print ("Matched - %s " % (des_dist))
        print (df_drr['VDC/Municipality'].unique())
        matched.append(des_dist)
        for row  in df_drr['VDC/Municipality'].unique():
            # Pass the row elements as key value pairs to append() function 
            dfObj = dfObj.append({'VDC/Municipality' : row , 'Localbody' : des_dist} , ignore_index=True)
    else:
        print ("Not Matched")
        not_matched.append(des_dist)
        dfObj = dfObj.append({ 'Localbody' : des_dist} , ignore_index=True)

print ("Matched %d/%d " % (len(not_matched), len(des_dist_list)))

print ("Not Matched %d/%d " % (len(not_matched), len(des_dist_list)))
dfObj.to_csv('LocalBody_VDC_MUNICIPALITY.csv')
