import pandas as pd

df_drr = pd.read_excel(r"DRR-Portal 7Jan2019.xlsx", "2018-2019")
df_des = pd.read_excel(r"DesInventar-2018-2019.xlsx", "Worksheet")
df_des_districts = pd.read_excel(r"des_districts.xlsx", "des_districts")

drr_dist_list = df_drr['District'].unique()
des_dist_list = df_des_districts['district'].unique()

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

#Create a DataFrame object
dfObj = pd.DataFrame([], columns = ['DRR_District', 'DES_District'], index=['a', 'b'])

matched = []
not_matched = []
for drr_dist in drr_dist_list:
    drr_des_dist = str(drr2des_District(drr_dist)).upper()
    if drr_des_dist in des_dist_list:
        matched.append(drr_dist)
        print ("%s Matched \n" % (drr_dist))
        dfObj = dfObj.append({'DRR_District':drr_dist,'DES_District':drr_des_dist} , ignore_index=True)
        
    else:
        not_matched.append(drr_dist)
        print ("%s Not Matched and could not be mapped to DesINVENTAR Database\n" % (drr_dist))
        dfObj = dfObj.append({'DRR_District':drr_dist} , ignore_index=True)

print ("Matched")
print (matched)
print ("Not Matched")
print (not_matched)
print ("Remaining To be matched from DRR")
print ([x for x in drr_dist_list if x not in matched])

dfObj.to_excel('match_districts_DRR_to_DES.xlsx')



