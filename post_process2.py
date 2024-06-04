import pandas as pd

# Create DataFrame
df = pd.read_csv('example3.csv')
# Combine Date and Time into a single datetime column
df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Group by the 'Timestamp' and 'UNIT ID' columns, keeping only the first occurrence of each combination
df_unique = df.drop_duplicates(subset=['Timestamp', 'UNIT ID'])



# Debug print: check the DataFrame after dropping duplicates
print("\nDataFrame after dropping duplicates:")

print(df_unique)
# Group by 'Timestamp' and filter out groups that don't have exactly four unique UNIT IDs (A, B, C, D)
# Create an empty DataFrame to collect valid groups
valid_groups = pd.DataFrame()
# Initialize the list of column names
column_names = ['datetime']
columns = ['Temp', 'Flow', 'SetPt']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rows = [0,1,2,3,4,5,6]
cols = [4, 6, 7]
# Generate the column names
for letter in letters:
    for col in columns:
        column_names.append(f'{col}{letter}')

df2 = pd.DataFrame(columns=column_names)
# Iterate over each group and check for valid UNIT ID sets
for timestamp, group in df_unique.groupby('Timestamp'):
    unit_ids = set(group['UNIT ID'])
    #print(f"\nTimestamp: {timestamp}")  # Debug print
    #print(f"UNIT IDs in group: {unit_ids}")  # Debug print of UNIT IDs in the group
    if {'A', 'B', 'C', 'D', 'E', 'F', 'G'}.issubset(unit_ids):
        # Sort the group by 'UNIT ID' before concatenating
        sorted_group = group.sort_values(by='UNIT ID')
        #print(sorted_group)
        timestamp = str(sorted_group.iloc[0]['Timestamp'])
        row_data = [timestamp]
        #print(row_data)
        for num in rows:
            for col in cols:
                #print(sorted_group.iloc[num][col])
                row_data.append(sorted_group.iloc[num][col])
        row_data_df = pd.DataFrame([row_data], columns=df2.columns)
        df2 = pd.concat([df2, row_data_df], ignore_index=True)   
        #print(df2)        
        #valid_groups = pd.concat([valid_groups, sorted_group])

# Reset the index for a clean output
df2 = df2.reset_index(drop=True)
#df2.drop(columns=['Timestamp'])
# Print the final filtered DataFrame
#print("\nFinal filtered DataFrame:")
#print(valid_groups)
df2.to_csv('First_Run.csv')