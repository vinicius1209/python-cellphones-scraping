from analytics import create_df, csv_to_df, df_to_csv, append_memories, clear_data, chart

""" GET FROM CSV FILE 
phones = csv_to_df("phones_bkp.csv")
phones = append_memories(phones)
df_to_csv(phones, "phones.csv")
#print(phones.info())
phones.describe()
"""
phones = csv_to_df("phones_bkp.csv")
phones = append_memories(phones)
phones = clear_data(phones)
print(phones.info())
chart(phones)
#df_to_csv(phones, "phones.csv")



