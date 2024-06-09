    # api_key = 'AIzaSyC5suuO0lxDNu9vgMq9YXENm0-sEO_Btz0'  # Replace with your Google Places API key
import requests
import pandas as pd
import os
import urllib.parse
from colorama import init, Fore, Style

# Initialize colorama
init()

# Expanded location types with translations
LOCATION_TYPES = {
    '1': {'en': 'real estate', 'ar': 'عقارات'},
    '2': {'en': 'supermarket', 'ar': 'سوبر ماركت'},
    '3': {'en': 'gas station', 'ar': 'محطة بنزين'},
    '4': {'en': 'restaurant', 'ar': 'مطعم'},
    '5': {'en': 'hospital', 'ar': 'مستشفى'},
    '6': {'en': 'school', 'ar': 'مدرسة'},
    '7': {'en': 'pharmacy', 'ar': 'صيدلية'},
    '8': {'en': 'bank', 'ar': 'بنك'},
    '9': {'en': 'hotel', 'ar': 'فندق'},
    '10': {'en': 'gym', 'ar': 'نادي رياضي'},
    '11': {'en': 'bar', 'ar': 'بار'},
    '12': {'en': 'book store', 'ar': 'مكتبة'},
    '13': {'en': 'bus station', 'ar': 'محطة حافلات'},
    '14': {'en': 'cafe', 'ar': 'مقهى'},
    '15': {'en': 'car repair', 'ar': 'تصليح سيارات'},
    '16': {'en': 'car wash', 'ar': 'غسيل سيارات'},
    '17': {'en': 'church', 'ar': 'كنيسة'},
    '18': {'en': 'clothing store', 'ar': 'محل ملابس'},
    '19': {'en': 'dentist', 'ar': 'طبيب أسنان'},
    '20': {'en': 'doctor', 'ar': 'طبيب'},
    '21': {'en': 'electronics store', 'ar': 'محل إلكترونيات'},
    '22': {'en': 'fire station', 'ar': 'محطة إطفاء'},
    '23': {'en': 'furniture store', 'ar': 'محل أثاث'},
    '24': {'en': 'hair salon', 'ar': 'صالون حلاقة'},
    '25': {'en': 'hardware store', 'ar': 'محل أجهزة'},
    '26': {'en': 'home goods store', 'ar': 'محل سلع منزلية'},
    '27': {'en': 'insurance agency', 'ar': 'وكالة تأمين'},
    '28': {'en': 'jewelry store', 'ar': 'محل مجوهرات'},
    '29': {'en': 'laundry', 'ar': 'مغسلة'},
    '30': {'en': 'library', 'ar': 'مكتبة'},
    '31': {'en': 'liquor store', 'ar': 'محل مشروبات كحولية'},
    '32': {'en': 'mosque', 'ar': 'مسجد'},
    '33': {'en': 'movie theater', 'ar': 'دار سينما'},
    '34': {'en': 'museum', 'ar': 'متحف'},
    '35': {'en': 'night club', 'ar': 'نادي ليلي'},
    '36': {'en': 'park', 'ar': 'حديقة'},
    '37': {'en': 'parking', 'ar': 'موقف سيارات'},
    '38': {'en': 'pet store', 'ar': 'محل حيوانات أليفة'},
    '39': {'en': 'police', 'ar': 'شرطة'},
    '40': {'en': 'post office', 'ar': 'مكتب بريد'},
    '41': {'en': 'real estate agency', 'ar': 'وكالة عقارية'},
    '42': {'en': 'school', 'ar': 'مدرسة'},
    '43': {'en': 'shopping mall', 'ar': 'مركز تسوق'},
    '44': {'en': 'spa', 'ar': 'منتجع صحي'},
    '45': {'en': 'stadium', 'ar': 'ملعب'},
    '46': {'en': 'store', 'ar': 'متجر'},
    '47': {'en': 'subway station', 'ar': 'محطة مترو'},
    '48': {'en': 'taxi stand', 'ar': 'موقف سيارات أجرة'},
    '49': {'en': 'train station', 'ar': 'محطة قطار'},
    '50': {'en': 'travel agency', 'ar': 'وكالة سفر'},
    '51': {'en': 'university', 'ar': 'جامعة'},
    '52': {'en': 'veterinary care', 'ar': 'رعاية بيطرية'},
    '53': {'en': 'zoo', 'ar': 'حديقة حيوان'}
}

# Prompts and messages in both languages
PROMPTS = {
    'en': {
        'select_language': "Select your language (1: English, 2: Arabic): ",
        'enter_city': "Enter the city name: ",
        'select_type': "Select the type of location you are looking for:",
        'invalid_choice': "Invalid choice. Please enter a valid number from the list.",
        'enter_type_number': "Enter the number corresponding to the location type: ",
        'no_locations': "No locations found.",
        'data_saved': "Data saved to"
    },
    'ar': {
        'select_language': "اختر لغتك (1: الإنجليزية، 2: العربية): ",
        'enter_city': "أدخل اسم المدينة: ",
        'select_type': "اختر نوع الموقع الذي تبحث عنه:",
        'invalid_choice': "خيار غير صالح. يرجى إدخال رقم صالح من القائمة.",
        'enter_type_number': "أدخل الرقم المقابل لنوع الموقع: ",
        'no_locations': "لم يتم العثور على مواقع.",
        'data_saved': "تم حفظ البيانات في"
    }
}

def get_language_choice():
    while True:
        choice = input(PROMPTS['en']['select_language']).strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'ar'
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")

def display_location_types(language):
    print(PROMPTS[language]['select_type'])
    for key, value in LOCATION_TYPES.items():
        print(f"{key}: {value[language]}")

# Function to get places from Google Places API using text search
def get_places(api_key, city_name, location_type):
    places = []
    try:
        encoded_location_type = urllib.parse.quote_plus(location_type.strip())
        encoded_city_name = urllib.parse.quote_plus(city_name.strip())
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_location_type}+in+{encoded_city_name}&key={api_key}"
        print(f"Requesting URL: {url}")  # Debugging line to print the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        if data.get('status') == 'OK':
            places.extend(data.get('results', []))
            while 'next_page_token' in data:
                next_page_token = data['next_page_token']
                url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={api_key}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                if data.get('status') == 'OK':
                    places.extend(data.get('results', []))
                else:
                    print(f"{Fore.RED}API response error: {data.get('status')} - {data.get('error_message')}{Style.RESET_ALL}")
                    break
        else:
            print(f"{Fore.RED}API response error: {data.get('status')} - {data.get('error_message')}{Style.RESET_ALL}")
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching data from Google Places API: {e}{Style.RESET_ALL}")
    
    return places
    
# Function to get detailed place information
def get_place_details(api_key, place_id):
    try:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'OK':
            return data.get('result', {})
        else:
            print(f"{Fore.RED}Place details API response error: {data.get('status')} - {data.get('error_message')}{Style.RESET_ALL}")
            return {}
    except requests.RequestException as e:
        print(f"{Fore.RED}Error fetching place details from Google Places API: {e}{Style.RESET_ALL}")
        return {}

# Function to collect and save places to Excel
def collect_places(api_key, city_name, location_type, output_file, language):
    places = get_places(api_key, city_name, location_type)
    
    if not places:
        print(f"{Fore.YELLOW}{PROMPTS[language]['no_locations']}{Style.RESET_ALL}")
        return

    locations = []
    for place in places:
        if place.get('business_status') != 'CLOSED_PERMANENTLY':
            details = get_place_details(api_key, place['place_id'])
            phone_number = details.get('formatted_phone_number', 'N/A')
            whatsapp_link = f"https://wa.me/{phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}" if phone_number != 'N/A' else 'N/A'
            location = {
                'Name': place.get('name', 'N/A'),
                'Phone Number': phone_number,
                'WhatsApp Link': whatsapp_link,
                'Google Maps Link': f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}",
                'Status': place.get('business_status', 'N/A')
            }
            locations.append(location)

    if not locations:
        print(f"{Fore.YELLOW}{PROMPTS[language]['no_locations']}{Style.RESET_ALL}")
        return

    df = pd.DataFrame(locations)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a format for the clickable links.
    link_format = workbook.add_format({'color': 'blue', 'underline': 1})

    # Write the WhatsApp links with the link format.
    for row in range(1, max_row + 1):
        worksheet.write_url(row, 2, df.at[row - 1, 'WhatsApp Link'], link_format, df.at[row - 1, 'WhatsApp Link'])

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

    print(f"{Fore.GREEN}{PROMPTS[language]['data_saved']} {output_file}{Style.RESET_ALL}")
    
    # Function to collect and save places to Excel
def collect_places(api_key, city_name, location_type, output_file, language):
    places = get_places(api_key, city_name, location_type)
    
    if not places:
        print(f"{Fore.YELLOW}{PROMPTS[language]['no_locations']}{Style.RESET_ALL}")
        return

    locations = []
    for place in places:
        if place.get('business_status') != 'CLOSED_PERMANENTLY':
            details = get_place_details(api_key, place['place_id'])
            phone_number = details.get('formatted_phone_number', 'N/A')
            whatsapp_link = f"https://wa.me/{phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')}" if phone_number != 'N/A' else 'N/A'
            location = {
                'Name': place.get('name', 'N/A'),
                'Phone Number': phone_number,
                'WhatsApp Link': whatsapp_link,
                'Google Maps Link': f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}",
                'Status': place.get('business_status', 'N/A')
            }
            locations.append(location)

    if not locations:
        print(f"{Fore.YELLOW}{PROMPTS[language]['no_locations']}{Style.RESET_ALL}")
        return

    df = pd.DataFrame(locations)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sheet1']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Create a format for the clickable links.
    link_format = workbook.add_format({'color': 'blue', 'underline': 1})

    # Write the WhatsApp links with the link format.
    for row in range(1, max_row + 1):
        worksheet.write_url(row, 2, df.at[row - 1, 'WhatsApp Link'], link_format, df.at[row - 1, 'WhatsApp Link'])

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

    print(f"{Fore.GREEN}{PROMPTS[language]['data_saved']} {output_file}{Style.RESET_ALL}")

# Main code
if __name__ == '__main__':
    api_key = 'YOUR_GOOGLE_PLACES_API_KEY'  # Replace with your Google Places API key
    
    language = get_language_choice()
    city_name = input(PROMPTS[language]['enter_city']).strip()
    
    display_location_types(language)
    
    while True:
        location_type_choice = input(PROMPTS[language]['enter_type_number']).strip()
        if location_type_choice in LOCATION_TYPES:
            location_type = LOCATION_TYPES[location_type_choice][language]
            break
        else:
            print(f"{Fore.RED}{PROMPTS[language]['invalid_choice']}{Style.RESET_ALL}")

    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, 'places_data.xlsx')

    collect_places(api_key, city_name, location_type, output_file, language)