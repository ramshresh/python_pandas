import pandas as pd


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






drr_dist_list = drr['District'].unique()
des_dist_list = des['District'].unique()

print (drr['District'].unique())
print (des['District'].unique())

matched = []
not_matched = []
for drr_dist in drr_dist_list:
    if str(drr2des_District(drr_dist)).upper() in des_dist_list:
        matched.append(drr_dist)
        print ("%s Matched \n" % (drr_dist))
    else:
        not_matched.append(drr_dist)
        print ("%s Not Matched and could not be mapped to DesINVENTAR Database\n" % (drr_dist))


print ("Matched")
print (matched)
print ("Not Matched")
print (not_matched)
print ("Remaining To be matched from DRR")
print ([x for x in drr_dist_list if x not in matched])
print ("Remaining To be matched from DES")

print ([x for x in des_dist_list if x.upper() not in [m.upper() for m in matched]])

