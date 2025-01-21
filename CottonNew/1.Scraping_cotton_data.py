import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
url = "https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=15&Tx_State=AP&Tx_District=17&Tx_Market=863&DateFrom=01-Jan-2020&DateTo=21-Jan-2025&Fr_Date=01-Jan-2020&To_Date=21-Jan-2025&Tx_Trend=0&Tx_CommodityHead=Cotton&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=Kurnool&Tx_MarketHead=Adoni"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
}

# Send a GET request
response = requests.get(url, headers=headers)
response.raise_for_status()  # Check for request errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table by ID
table = soup.find("table", {"id": "cphBody_GridPriceData"})

# Check if the table exists
if not table:
    print("Table not found on the page.")
    exit()

# Extract table headers
headers = [header.text.strip() for header in table.find_all("th")]

# Extract table rows
data = []
rows = table.find_all("tr")[1:]  # Skip the header row
for row in rows:
    columns = row.find_all("td")
    row_data = [col.text.strip() for col in columns]
    data.append(row_data)

# Save data to a CSV file
output_file = "agmarknet_data.csv"
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write headers
    csvwriter.writerow(headers)
    # Write rows
    csvwriter.writerows(data)

print(f"Data successfully scraped and saved to {output_file}")
