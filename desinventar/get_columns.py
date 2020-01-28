import pandas as pd

df_drr_in_des = pd.read_excel(r"Final for DesIn.xlsx","drr_not_in_desinventar_final_di")

print (list(df_drr_in_des))

df_dist = pd.read_excel(r"match_districts_DRR_to_DES.xlsx","Sheet1")

print (list(df_dist))
