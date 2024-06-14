# DPLocator

DPLocator is a Python script designed to fetch location data from the Google Places API based on user-defined parameters. The script allows users to search for various types of places within a specified city and export the results to an Excel file.

## Features

- Supports both English and Arabic languages.
- Fetches detailed information about places including name, phone number, WhatsApp link, Google Maps link, status, city, district, and overall rating.
- Utilizes Google Places API for data retrieval and Google Geocoding API for fetching city coordinates.
- Handles pagination to retrieve more than the default limit of 60 results.
- Outputs results to a styled Excel file with centralized text.

## Requirements

- Python 3.x
- `requests` library
- `pandas` library
- `xlsxwriter` library
- Google Places API key
- Google Geocoding -> install it from project's library of google console

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DangerousPixel/DPLocator.git
   cd DPLocator
   ```
2.	Install the required Python libraries:
       ```bash
          pip install requests pandas xlsxwriter
    ```
## Usage

1. Run the script:
   ```bash
       python dplocator.py
   
2. Follow the prompts:
   
	•	Select the language (1 for English, 2 for Arabic).

	•	Enter the city name.

	•	Select the type of location from the provided list.

	•	The script will fetch the data and save it to an Excel file in the current directory.

## Example

   ```bash
    Select your language (1: English, 2: Arabic): 1
    Enter the city name: Riyadh
    Fetching coordinates for the city...
    Coordinates fetched: {'lat': 24.7135517, 'lng': 46.6752957}
    Fetching places...
    Data saved to /path/to/your/directory/places_data.xlsx
```
## Notes

•	Ensure your Google API keys have the necessary permissions enabled.

•	The script handles pagination to fetch more results but adheres to API usage limits.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

