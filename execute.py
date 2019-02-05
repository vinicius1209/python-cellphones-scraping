from analytics import create_df, csv_to_df, df_to_csv, append_memories, clear_data, chart, new_info

phones = create_df()
phones = append_memories(phones)
phones = clear_data(phones)
phones = new_info(phones)
df_to_csv(phones, "phones.csv")
