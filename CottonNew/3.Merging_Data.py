import pandas as pd

# Specify the engine for reading .xls files
adoni_market = pd.read_csv('adoni_market.xls')
print("adoni_market",adoni_market.head)
# Load the modified CSV file
modified_data = pd.read_csv('modified_agmarknet_data.csv')

# Merge the two datasets by concatenating them
merged_data = pd.concat([modified_data, adoni_market], ignore_index=True)

merged_data.to_csv('merged_agmarknet_adoni_market.csv', index=False)

print("The files have been successfully merged and saved as 'merged_agmarknet_adoni_market.xls'.")
