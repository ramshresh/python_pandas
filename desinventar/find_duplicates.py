
import pandas as pd
import pandasql as pdsql
from datetime import datetime

"""
drr_types =['Fire', 'Other', 'Epidemic', 'Cold Wave', 'Wind storm', 'High Altitude',
 'Landslide', 'Thunderbolt', 'Heavy Rainfall', 'Boat Capsize', 'Flood',
 'Hailstone', 'Snow Storm', 'Animal Incidents', 'Snake Bite', 'Avalanche',
 'Sinkhole', 'Air Crash', 'Hail Storm', 'Forest Fire' ]
des_types = ['Fire', 'Epidemic', 'Cold Wave', 'Accident', 'Thunderstorm', 'Forest Fire',
 'Famine', 'Structural Collapse', 'Strong Wind', 'Flood', 'Landslide',
 'Avalanche' ,'Earthquake', 'Rains', 'Boat Capsize', 'Hailstorm', 'Snow Storm',
 'Explosion', 'Storm', 'Heat Wave']
"""

"""
Remaining To be matched from DRR
['Shyanja', 'Nawalparasi (Bardghat Susta East)', 'Shankhuwasabha', 'Sindhupalchowk', 'Rukum', 'Rukum East', 'Kavrepalanchowk', 'Achhaam', 'Rukum West', 'Nawalparasi (Bardghat Susta West)', 'Surkhet', nan]
Remaining To be matched from DES
['SANKHUWASABHA', 'RUKUM_W', 'RUKUM_E', 'SINDHUPALCHOK', 'SYANGJA', 'NAWALPARASI_E', 'ACHHAM', 'NAWALPARASI_W', 'KABHREPALANCHOK']

S.No.,	drr_id,	District,	VDC/Municipality,	Ward No.,	Incident Place,	Incident Date,	Incident,

11858,	131,	Rukum,	Others,		Uttarganga-8,	12/01/2018,	Fire
to
11858,	131,	Rukum East,	Putha Uttarganga,	8,	Uttarganga-8,	12/01/2018,	Fire
"""

def drr2des_EventType(drr_incident):
    dict_drr2des = {
        "Thunderbolt": "Thunderstorm",
        "Wind storm": "Strong Wind",
        "Heavy Rainfall":"Rains",
        "Hailstone":"Hailstorm",
        "Hail Storm":"Hailstorm",

        "Fire":"Fire", 
        "Epidemic":"Epidemic", 
        "Cold Wave":"Cold Wave", 
        "Landslide":"Landslide", 
        "Boat Capsize":"Boat Capsize", 
        "Flood":"Flood", 
        "Snow Storm":"Snow Storm",
        "Avalanche":"Avalanche", 
        "Forest Fire":"Forest Fire"

        }
    if drr_incident in dict_drr2des.keys():
        return dict_drr2des[drr_incident]
    return None

def drr2des_District(drr_district):
    dict_drr2des = {
        "Achhaam":"ACHHAM",
        "Kavrepalanchowk":"KABHREPALANCHOK",
        "Nawalparasi (Bardghat Susta East)": "NAWALPARASI_E",
        "Nawalparasi (Bardghat Susta West)":"NAWALPARASI_W", 
        "Rukum East":"RUKUM_E",
        "Rukum West":"RUKUM_W",
        "Sindhupalchowk":"SINDHUPALCHOK",
        "Shankhuwasabha":"SANKHUWASABHA",
        "Shyanja": "SYANGJA",
        "Surkhet":"SURKHET"
        }
    if drr_district in dict_drr2des.keys():
        return dict_drr2des[drr_district]
    return drr_district


excel_file_drr = r"C:\learn2code\desinventar\DRR-Portal 7Jan2019.xlsx"
excel_file_des = r"C:\learn2code\desinventar\DesInventar-2018-2019.xlsx"

drr = pd.read_excel(excel_file_drr, "2018-2019")
des = pd.read_excel(excel_file_des, "Worksheet")

#print (drr.columns)
print (drr['Incident'].unique())
print (des['Event Type'].unique())
pysql = lambda q: pdsql.sqldf(q, globals())

not_date_district_incident_list = []
dup_date_district_incident_list = []

"""
for index, row  in des.iterrows():
    print("sample record of Desinventar)")
    print (row)# Event Date, Event Type ,District, Localbody, Dead T, des_id , Data Card No  , Placename
    print (row["Event Date"])
    break
"""


for index, row  in drr.iterrows():
    #print (row)# Incident , Total Death , drr_id, S.No. , District , VDC/Municipality, Ward No. , Incident Place  , Incident Date   
    #print (row['District'])
    #print (str(row['Incident Date']))
    #print (row['Incident'])
    
    #print (datetimeObj.date())
    try:
        datetimeObj = datetime.strptime(str(row['Incident Date']),'%Y-%m-%d %H:%M:%S')
        df_des = des[
        (des['District'].str.contains(drr2des_District(row['District']).upper()))
        #(des['District'].str.contains(row['District'].upper()))
        &(des['Event Date']==str(datetimeObj.date()))
        &(des['Event Type'] == drr2des_EventType(row['Incident']))
        ]
        if  df_des.shape[0] >0:
            dup_date_district_incident_list.append(row['S.No.'])
            print ("for DRR record SN. %d Found %d records of %s incidents in Desinventar in %s district in Date: %s" %(row['S.No.'], df_des.shape[0],row['Incident'], row['District'], str(datetimeObj.date())))
            for index_des, row_des  in df_des.iterrows(): 
                print (row_des)
        else:
            not_date_district_incident_list.append(row['S.No.'])
        
    except:
        pass        
        
   
print (not_date_district_incident_list)

#dfs = pd.DataFrame(not_date_district_list, columns=['S.No.'])
#dfs.to_csv('not_date_district_list.csv', index=False)



print (len(not_date_district_incident_list))
print (len(dup_date_district_incident_list))

mask1 = drr['S.No.'].isin(not_date_district_incident_list)
drr_not_in_desinventar = drr[mask1]
drr_not_in_desinventar.to_csv('drr_not_in_desinventar.csv', index=False)


mask2 = drr['S.No.'].isin(dup_date_district_incident_list)
drr_maybe_in_desinventar = drr[mask2]
drr_maybe_in_desinventar.to_csv('drr_maybe_in_desinventar.csv', index=False)


#df_not_date_district_list = pd.DataFrame({'S.No.':not_date_district_incident_list})
#df_not_date_district_list.to_csv('drr_not_date_district_list.csv', index=False)

#df_dup_date_district_list = pd.DataFrame({'S.No.':dup_date_district_incident_list})
#df_dup_date_district_list.to_csv('drr_dup_date_district_list.csv', index=False)
