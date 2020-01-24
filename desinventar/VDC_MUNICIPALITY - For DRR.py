import pandas as pd
import re, math

excel_file_drr = r"C:\learn2code\desinventar\DRR-Portal 7Jan2019.xlsx"
excel_file_des = r"C:\learn2code\desinventar\localbodies.xlsx"
excel_file_drr_des = r"C:\learn2code\desinventar\LocalBody_VDC_MUNICIPALITY_for_drr_EDITED.xlsx"

drr = pd.read_excel(excel_file_drr, "2018-2019")
des = pd.read_excel(excel_file_des, "localbodies")
drr_des_vdc = pd.read_excel(excel_file_drr_des, "DRR_2_DES")

drr_vdc_list = drr['VDC/Municipality'].unique()
des_vdc_list = des['local_bodies'].unique()

print (drr['VDC/Municipality'].unique())
print (des['local_bodies'].unique())

def drr2des_VDC_MUNICIPALITY(drr_vdc):
    df_drr_des_vdc = drr_des_vdc[
        (drr_des_vdc['VDC/Municipality'].str.contains(drr_vdc, na=False))
        &(drr_des_vdc['Localbody'].notnull())
        ]
    vdc =df_drr_des_vdc.iloc[0]['Localbody'] if (df_drr_des_vdc.shape[0]>0 )else None
    if vdc is None:
        print ("None %s"%(vdc))
    else:
         print ("Not None but %s"%(df_drr_des_vdc.iloc[0]['Localbody']))
    return vdc
matched = []
not_matched = []

#Create a DataFrame object
dfObj = pd.DataFrame([], columns = ['S.No.', 'District', 'VDC/Municipality' , 'Localbody'], index=['a', 'b'])

for drr_vdc in drr_vdc_list:
    drr_vdc_stripped = str(drr_vdc).replace('Metropolitan City','').replace('Submetropolitan City','').replace('Rural Municipality','').replace('Municipality','').replace('Submetropolitan City','').strip()

    print (drr_vdc_stripped)
        
    df_drr = drr[(drr['VDC/Municipality']==drr_vdc)]
    district = df_drr.iloc[0]['District'] if   df_drr.shape[0]>0 else ""
    sn = df_drr.iloc[0]['S.No.'] if   df_drr.shape[0]>0 else ""

    if(drr2des_VDC_MUNICIPALITY(drr_vdc_stripped) is not None and drr2des_VDC_MUNICIPALITY(drr_vdc_stripped) !=''):
        df_des = des[
            (des['local_bodies'].str.contains(drr2des_VDC_MUNICIPALITY(drr_vdc_stripped), na=False))] 
        if  df_des.shape[0] > 0:
            print ("Matched - %s " % (drr_vdc))
            print (df_des['local_bodies'].unique())
            matched.append(drr_vdc)
            for index_des, row_des  in df_des.iterrows():
                # Pass the row elements as key value pairs to append() function 
                dfObj = dfObj.append({'S.No.':sn,'District':district, 'VDC/Municipality_Stripped' : drr_vdc_stripped ,  'VDC/Municipality' : drr_vdc , 'Localbody' : row_des['local_bodies']} , ignore_index=True)
            """  
            for row  in df_des['Localbody'].unique():
                # Pass the row elements as key value pairs to append() function 
                dfObj = dfObj.append({'District':,'VDC/Municipality' : drr_vdc , 'Localbody' : row} , ignore_index=True)
            """
        else:
            print ("Not Matched")
            not_matched.append(drr_vdc)
            dfObj = dfObj.append({ 'S.No.':sn,'District':district,'VDC/Municipality_Stripped' : drr_vdc_stripped , 'VDC/Municipality' : drr_vdc} , ignore_index=True)
    else:
            print ("Not Matched")
            not_matched.append(drr_vdc)
            dfObj = dfObj.append({ 'S.No.':sn,'District':district,'VDC/Municipality_Stripped' : drr_vdc_stripped , 'VDC/Municipality' : drr_vdc} , ignore_index=True)

print ("Matched %d/%d " % (len(not_matched), len(drr_vdc_list)))

print ("Not Matched %d/%d " % (len(not_matched), len(drr_vdc_list)))
dfObj.to_csv('LocalBody_VDC_MUNICIPALITY_for_drr-1111.csv')
