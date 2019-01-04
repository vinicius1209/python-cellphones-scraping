from analytics import create_df, csv_to_df, df_to_csv

#phones = csv_to_df("phones.csv")
phones = csv_to_df("phones.csv")
df_to_csv(phones)
print(phones.info())
print('######################################')
print(phones.phone_title)
