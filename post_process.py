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

# Iterate over each group and check for valid UNIT ID sets
for timestamp, group in df_unique.groupby('Timestamp'):
    unit_ids = set(group['UNIT ID'])
    #print(f"\nTimestamp: {timestamp}")  # Debug print
    #print(group)  # Debug print of the group
    #print(f"UNIT IDs in group: {unit_ids}")  # Debug print of UNIT IDs in the group
    if {'A', 'B', 'C', 'D', 'E', 'F', 'G'}.issubset(unit_ids):
        # Sort the group by 'UNIT ID' before concatenating
        sorted_group = group.sort_values(by='UNIT ID')
        valid_groups = pd.concat([valid_groups, sorted_group])

# Reset the index for a clean output
valid_groups = valid_groups.reset_index(drop=True)
valid_groups.drop(columns=['Timestamp'])
# Print the final filtered DataFrame
#print("\nFinal filtered DataFrame:")
#print(valid_groups)
valid_groups.to_csv('First_Run.csv')