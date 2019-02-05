from app.analytics import create_df, df_to_csv, append_memories, clear_data, new_info

phones = create_df()
phones = append_memories(phones)
phones = clear_data(phones)
phones = new_info(phones)
df_to_csv(phones, "str\phones.csv")
