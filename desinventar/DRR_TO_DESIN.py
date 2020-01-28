import pandas as pd
from datetime import datetime


df_drr_in_des = pd.read_excel(r"Final for DesIn.xlsx","2018")
df_dist = pd.read_excel(r"match_districts_DRR_to_DES.xlsx","Sheet1")
df_muni = pd.read_excel(r"match_muni_DRR_to_DES_edited_manually.xlsx","Sheet1")

df_locb = pd.read_excel(r"localbodies.xlsx","localbodies")
df_regions = pd.read_excel(r"des_districts.xlsx","des_districts")
df_event_types = pd.read_excel(r"EventTypes.xlsx","Sheet1")


matched = []
not_matched = []

#Create a DataFrame object
dfObj = pd.DataFrame([], columns = ['S.No.', 'District', 'VDC/Municipality' , 'Localbody'], index=['a', 'b'])

# S.No.,  Affected Family, Death Unknown, No. of Displaced Family, Govt. Houses Fully Damaged, Govt. Houses Partially Damaged, Private House Fully Damaged, Private House Partially Damaged, Displaced Male(N/A), Displaced Female(N/A)
# No. of Displaced Family

cols_drr  = ['S.No.', 'drr_id', 'District', 'VDC/Municipality', 'Ward No.', 'Incident Place',
             'Incident Date', 'Incident', 'Death Male', 'Death Female', 'Death Unknown', 'Total Death',
             'Missing People', 'Affected Family', 'Estimated Loss', 'Injured',
             'Govt. Houses Fully Damaged', 'Govt. Houses Partially Damaged', 'Private House Fully Damaged',
             'Private House Partially Damaged', 'Displaced Male(N/A)', 'Displaced Female(N/A)', 'Property Loss',
             'No. of Displaced Family', 'Cattles Loss', 'Displaced Shed', 'Source', 'Remarks']
col_des = ['S.No.', 'drr_id', 'District', 'VDC/Municipality', 'Ward No.', 'Incident Place', 'Incident Date',
           'Incident', 'Death Male', 'Death Female', 'Death Unknown', 'Total Death', 'Missing People',
           'Affected Family', 'Estimated Loss', 'Injured', 'Govt. Houses Fully Damaged',
           'Govt. Houses Partially Damaged', 'Private House Fully Damaged', 'Private House Partially Damaged',
           'Displaced Male(N/A)', 'Displaced Female(N/A)', 'Property Loss', 'No. of Displaced Family',
           'Cattles Loss', 'Displaced Shed', 'Source', 'Remarks']

col_des_drr = {
    #"Event Date":"Incident Date",
    #"Event Type":"Incident",
    #"District":"District",
    #"Localbody":"VDC/Municipality",
    "Wardno": "Ward No.",
    "Placename":"Incident Place",
    "Dead M": "Death Male",
    "Dead F": "Death Female",
    "Dead T": "Total Death",
    "Injured T":"Injured",
    "Missing T": "Missing People",
    "Relocated M":"Displaced Male(N/A)",
    "Relocated F":"Displaced Female(N/A)",
    "Destroyed Building" : ["Govt. Houses Fully Damaged", "Private House Fully Damaged" ],
    "Affected Building" : ["Govt. Houses Partially Damaged", "Private House Partially Damaged"],
    "Affected Shed": "Displaced Shed",
    "Total Loss Value Rs":"Estimated Loss", 
    "Comment":"Remarks",
    "Source":"Source",	
    "Loss Livestock Quantity":"Cattles Loss"
}
	

cols_drr.extend([
    "DES_District", "DES_Muni", "DES_Ecology", "DES_Region", "DES_Zone", "DES_State", "Event Type", "Event Date"])

cols_drr.extend(col_des_drr.keys())

    
    

dfObj = pd.DataFrame([], columns=cols_drr)
#print (list(cols_drr))
print ("----------START----------------")
for index, row  in df_drr_in_des.iterrows():
    
    mask = (df_muni['DRR_District'] == row['District'])&(df_muni['DRR_Muni'] == row['VDC/Municipality'])
    df_muni_sel = df_muni[mask]
    
    if df_muni_sel.shape[0]>0:
        row['DES_District'] = df_muni_sel.iloc[0]['DES_District'] if pd.notna(df_muni_sel.iloc[0]['DES_District']) else ""
        row['DES_Muni'] = df_muni_sel.iloc[0]['DES_muni'] if pd.notna(df_muni_sel.iloc[0]['DES_muni']) else ""

        mask_regions_sel = (df_regions['district'] == df_muni_sel.iloc[0]['DES_District'])
        df_regions_sel = df_regions[mask_regions_sel]
        if(df_regions_sel.shape[0]>0):                        
            #print (row['DES_District'] if pd.notna(row['DES_District']) else "ERROR ")
            #print (df_regions_sel)
            row['DES_Ecology'] = df_regions_sel.iloc[0]['ecology'] if pd.notna(df_regions_sel.iloc[0]['ecology']) else ""
            row['DES_Region'] = df_regions_sel.iloc[0]['region'] if pd.notna(df_regions_sel.iloc[0]['region']) else ""
            row['DES_Zone'] = df_regions_sel.iloc[0]['zone'] if pd.notna(df_regions_sel.iloc[0]['zone']) else ""
            row['DES_State'] = df_regions_sel.iloc[0]['state'] if pd.notna(df_regions_sel.iloc[0]['state']) else ""
            

    mask_et_sel = (df_event_types['DRR_Incident'] == row['Incident'])
    df_event_types_sel = df_event_types[mask_et_sel]    
    if(df_regions_sel.shape[0]>0):
        row['Event Type'] = df_event_types_sel.iloc[0]['DES_Event_Type']

    datetimeObj = datetime.strptime(str(row['Incident Date']),'%Y-%m-%d %H:%M:%S')
    row['Event Date'] = str(datetimeObj.date())


    for des_col in col_des_drr.keys():
        drr_col = col_des_drr[des_col]
        if isinstance(drr_col, list):
            sum = 0
            for i in row[drr_col]:
                sum = sum+float(i)
            row[des_col] = sum    
        else:
            row[des_col] = row[drr_col]

    
    else:
        # Not Matched
        #print  ("dist: %s    |    muni: %s"% (row['District'], row['VDC/Municipality']) )
        pass
    dfObj = dfObj.append(row)
    #print (row)
print ("----------END----------------")
print("Saving to file")
dfObj.to_excel('Final for DesIn with_ecology_region_zone_state-2018------test.xlsx')
    
