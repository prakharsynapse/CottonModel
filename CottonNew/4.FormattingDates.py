import pandas as pd

# Load the modified CSV file
modified_data = pd.read_csv('merged_agmarknet_adoni_market.csv')

# Define a function to convert the date format
def convert_date_format(date_str):
    try:
        # Attempt to parse the date in the format 'dd-Month-Name-yy' and convert to 'dd/mm/yyyy'
        return pd.to_datetime(date_str, format='%d-%b-%y').strftime('%d/%m/%Y')
    except Exception as e:
        # If an error occurs (invalid format), return the original date
        return date_str

# Apply the function to the 'Arrival_Date' column
modified_data['Arrival_Date'] = modified_data['Arrival_Date'].apply(convert_date_format)

# Save the updated data to a new CSV file
modified_data.to_csv('merged_agmarknet_adoni_market.csv', index=False)

print("The 'Arrival_Date' column has been successfully formatted to 'dd/mm/YYYY'.")
