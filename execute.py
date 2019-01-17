from analytics import create_df, csv_to_df, df_to_csv, append_memories

""" GET FROM CSV FILE 
phones = csv_to_df("phones_bkp.csv")
phones = append_memories(phones)
df_to_csv(phones, "phones.csv")
#print(phones.info())
phones.describe()
"""
phones = csv_to_df("phones_bkp.csv")
phones = append_memories(phones)

y = []
for x in phones.current_price:
    y.append(x.replace('.', ''))

phones['current_price'] = y
df_to_csv(phones, "phones.csv")



