import pandas as pd

df_drr = pd.read_excel(r"DRR-Portal 7Jan2019.xlsx", "2018-2019")
df_des = pd.read_excel(r"DesInventar-2018-2019.xlsx", "Worksheet")
df_matched_dist = pd.read_excel(r"match_districts_DRR_to_DES.xlsx", "Sheet1")

df_des_localbodies = pd.read_excel(r"localbodies.xlsx", "localbodies")


def drr2des_dist(drr_dist):
    df = df_matched_dist[
        (df_matched_dist['DRR_District'] == drr_dist)
        &(df_matched_dist['DES_District'].notnull())
        ]
    des_dist =df.iloc[0]['DES_District'] if (df.shape[0]>0 )else None
    return des_dist


#Create a DataFrame object
dfObj = pd.DataFrame([], columns = ['DRR_District', 'DRR_Muni', 'DES_District', 'DES_muni'])


matched = []
not_matched = []

groups = ['District','VDC/Municipality']
df_drr_grouped= df_drr.groupby(['District','VDC/Municipality'])
# iterate over each group
for group_names, df_group in df_drr_grouped:
    drr_dist = group_names[groups.index('District')]
    drr_muni = group_names[groups.index('VDC/Municipality')]
    #print ("DISTRICT: %s\nMunicipality: %s" %(dist, muni))
    drr_des_dist = drr2des_dist(drr_dist)
    drr_des_muni_stripped = str(drr_muni).replace('Metropolitan City','').replace('Submetropolitan City','').replace('Rural Municipality','').replace('Municipality','').replace('Submetropolitan City','').strip()
    
    df_des_localbodies_filtered = df_des_localbodies[
        (df_des_localbodies['local_bodies'].str.contains(str(drr_des_muni_stripped), na=False))
        &(df_des_localbodies['district']==drr_des_dist)
        ]
    if df_des_localbodies_filtered.shape[0] > 0:
        print ("Matched - %s " % (drr_muni))
        matched.append(drr_muni)
        des_dist = df_des_localbodies_filtered.iloc[0]['district']
        des_muni = df_des_localbodies_filtered.iloc[0]['local_bodies']
        dfObj = dfObj.append({'DRR_District':drr_dist,'DRR_Muni':drr_muni, 'DES_District':des_dist, 'DES_muni':des_muni} , ignore_index=True)
        
    else:
        print ("Not Matched")
        not_matched.append(drr_muni)
        dfObj = dfObj.append({'DRR_District':drr_dist,'DRR_Muni':drr_muni} , ignore_index=True)
        


print ("Matched")
print (matched)
print ("Not Matched")
print (not_matched)
print ("Remaining To be matched from DRR")
print ([x for x in df_drr['District'].unique() if x not in matched])

dfObj.to_excel('match_muni_DRR_to_DES.xlsx')
