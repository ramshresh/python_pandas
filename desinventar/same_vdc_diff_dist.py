import pandas as pd
import re, math


df_drr = pd.read_excel(r"DRR-Portal 7Jan2019.xlsx", "2018-2019")
df_des = pd.read_excel(r"C:\learn2code\desinventar\localbodies.xlsx", "localbodies")
df_matched_muni = pd.read_excel(r"DRR_Municipality_2_DES_Manually_matched.xlsx", "manually_matched")

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

def drr2des_muni(drr_vdc):
    df_drr_des_vdc = df_matched_muni[
        (df_matched_muni['VDC/Municipality'].str.contains(drr_vdc, na=False))
        &(df_matched_muni['Localbody'].notnull())
        ]
    vdc =df_drr_des_vdc.iloc[0]['Localbody'] if (df_drr_des_vdc.shape[0]>0 )else None
    if vdc is None:
        print ("None %s"%(vdc))
    else:
         print ("Not None but %s"%(df_drr_des_vdc.iloc[0]['Localbody']))
    return vdc



groups = ['District','VDC/Municipality']
df_drr_grouped= df_drr.groupby(['District','VDC/Municipality'])
# iterate over each group
for group_names, df_group in df_drr_grouped:
    drr_dist = group_names[groups.index('District')]
    drr_muni = group_names[groups.index('VDC/Municipality')]
    #print ("DISTRICT: %s\nMunicipality: %s" %(dist, muni))
    
    for row_index, row in df_group.iterrows():
        dist_drr = row['District']
        muni_drr = row['VDC/Municipality']

        drr_muni_stripped = str(drr_muni).replace('Metropolitan City','').replace('Submetropolitan City','').replace('Rural Municipality','').replace('Municipality','').replace('Submetropolitan City','').strip()
        df_des_filtered = df_des[
            (df_des['local_bodies'].str.contains(drr2des_VDC_MUNICIPALITY(drr_vdc_stripped), na=False))] 
            &(df_des['district'] == (drr2des_VDC_MUNICIPALITY(drr_vdc_stripped), na=False))
            
    
    drr2des_dist =  drr2des_District(drr_dist)
    #print ( drr2des_dist.upper())
    
    
    df_des = des[
            (des['local_bodies'].str.contains(drr2des_VDC_MUNICIPALITY(drr_vdc_stripped), na=False))] 
            &(des['district'] = (drr2des_VDC_MUNICIPALITY(drr_vdc_stripped), na=False))
            
    

    

