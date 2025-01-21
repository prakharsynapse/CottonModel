import pandas as pd

# Load the CSV file
data = pd.read_csv('agmarknet_data.csv')

# Add a new column 'State' with value 'Andhra Pradesh'
data['State'] = 'Andhra Pradesh'

# Rename columns
data.rename(columns={
    'District Name': 'District',
    'Market Name': 'Market',
    'Max Price (Rs./Quintal)': 'Max Price',
    'Min Price (Rs./Quintal)': 'Min Price',
    'Modal Price (Rs./Quintal)': 'Modal Price',
    'Price Date': 'Arrival_Date'
}, inplace=True)

data['Variety'] = 'Kapas (Adoni)'

# Drop unnecessary columns
data.drop(columns=['Sl no.', 'Grade'], inplace=True)

# Reorder columns: Place 'State' first and 'Arrival_Date' after 'Variety'
columns_order = ['State', 'District', 'Market', 'Commodity', 'Variety', 'Arrival_Date', 'Min Price', 'Max Price', 'Modal Price']
data = data[columns_order]
# Display the first few rows to verify the changes
print(data.head())

# Save the modified data to a new CSV file
data.to_csv('modified_agmarknet_data.csv', index=False)
