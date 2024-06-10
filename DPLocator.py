import requests
import pandas as pd
import os
import urllib.parse
from colorama import init, Fore, Style

# Initialize colorama
init()

# Expanded location types with translations
LOCATION_TYPES = {
    '1': {'en': 'accounting', 'ar': 'محاسبة'},
    '2': {'en': 'airport', 'ar': 'مطار'},
    '3': {'en': 'amusement park', 'ar': 'مدينة ملاهي'},
    '4': {'en': 'aquarium', 'ar': 'حوض سمك'},
    '5': {'en': 'art gallery', 'ar': 'معرض فني'},
    '6': {'en': 'atm', 'ar': 'صراف آلي'},
    '7': {'en': 'bakery', 'ar': 'مخبز'},
    '8': {'en': 'bank', 'ar': 'بنك'},
    '9': {'en': 'beauty salon', 'ar': 'صالون تجميل'},
    '10': {'en': 'bicycle store', 'ar': 'متجر دراجات'},
    '11': {'en': 'book store', 'ar': 'مكتبة'},
    '12': {'en': 'bowling alley', 'ar': 'صالة بولينغ'},
    '13': {'en': 'bus station', 'ar': 'محطة حافلات'},
    '14': {'en': 'cafe', 'ar': 'مقهى'},
    '15': {'en': 'campground', 'ar': 'موقع تخييم'},
    '16': {'en': 'car dealer', 'ar': 'تاجر سيارات'},
    '17': {'en': 'car rental', 'ar': 'تأجير سيارات'},
    '18': {'en': 'car repair', 'ar': 'تصليح سيارات'},
    '19': {'en': 'car wash', 'ar': 'غسيل سيارات'},
    '20': {'en': 'cemetery', 'ar': 'مقبرة'},
    '21': {'en': 'city hall', 'ar': 'قاعة المدينة'},
    '22': {'en': 'clothing store', 'ar': 'محل ملابس'},
    '23': {'en': 'convenience store', 'ar': 'متجر صغير'},
    '24': {'en': 'courthouse', 'ar': 'محكمة'},
    '25': {'en': 'dentist', 'ar': 'طبيب أسنان'},
    '26': {'en': 'department store', 'ar': 'متجر متعدد الأقسام'},
    '27': {'en': 'doctor', 'ar': 'طبيب'},
    '28': {'en': 'electrician', 'ar': 'كهربائي'},
    '29': {'en': 'electronics store', 'ar': 'محل إلكترونيات'},
    '30': {'en': 'embassy', 'ar': 'سفارة'},
    '31': {'en': 'fire station', 'ar': 'محطة إطفاء'},
    '32': {'en': 'florist', 'ar': 'محل زهور'},
    '33': {'en': 'funeral home', 'ar': 'دار جنازة'},
    '34': {'en': 'furniture store', 'ar': 'محل أثاث'},
    '35': {'en': 'gas station', 'ar': 'محطة بنزين'},
    '36': {'en': 'gym', 'ar': 'نادي رياضي'},
    '37': {'en': 'hair care', 'ar': 'عناية بالشعر'},
    '38': {'en': 'hardware store', 'ar': 'محل أجهزة'},
    '39': {'en': 'home goods store', 'ar': 'محل سلع منزلية'},
    '40': {'en': 'hospital', 'ar': 'مستشفى'},
    '41': {'en': 'insurance agency', 'ar': 'وكالة تأمين'},
    '42': {'en': 'jewelry store', 'ar': 'محل مجوهرات'},
    '43': {'en': 'laundry', 'ar': 'مغسلة'},
    '44': {'en': 'lawyer', 'ar': 'محامي'},
    '45': {'en': 'library', 'ar': 'مكتبة'},
    '46': {'en': 'light rail station', 'ar': 'محطة قطار خفيف'},
    '47': {'en': 'local government office', 'ar': 'مكتب حكومة محلية'},
    '48': {'en': 'locksmith', 'ar': 'صانع أقفال'},
    '49': {'en': 'lodging', 'ar': 'إقامة'},
    '50': {'en': 'meal delivery', 'ar': 'توصيل وجبات'},
    '51': {'en': 'meal takeaway', 'ar': 'وجبات سريعة'},
    '52': {'en': 'mosque', 'ar': 'مسجد'},
    '53': {'en': 'movie rental', 'ar': 'تأجير أفلام'},
    '54': {'en': 'movie theater', 'ar': 'دار سينما'},
    '55': {'en': 'moving company', 'ar': 'شركة نقل'},
    '56': {'en': 'museum', 'ar': 'متحف'},
    '57': {'en': 'park', 'ar': 'حديقة'},
    '58': {'en': 'parking', 'ar': 'موقف سيارات'},
    '59': {'en': 'pet store', 'ar': 'محل حيوانات أليفة'},
    '60': {'en': 'pharmacy', 'ar': 'صيدلية'},
    '61': {'en': 'physiotherapist', 'ar': 'اخصائي علاج طبيعي'},
    '62': {'en': 'plumber', 'ar': 'سباك'},
    '63': {'en': 'police', 'ar': 'شرطة'},
    '64': {'en': 'post office', 'ar': 'مكتب بريد'},
    '65': {'en': 'real estate agency', 'ar': 'وكالة عقارية'},
    '66': {'en': 'restaurant', 'ar': 'مطعم'},
    '67': {'en': 'roofing contractor', 'ar': 'مقاول تسقيف'},
    '68': {'en': 'rv park', 'ar': 'حديقة سيارات التخييم'},
    '69': {'en': 'school', 'ar': 'مدرسة'},
    '70': {'en': 'shoe store', 'ar': 'متجر أحذية'},
    '71': {'en': 'shopping mall', 'ar': 'مركز تسوق'},
    '72': {'en': 'spa', 'ar': 'منتجع صحي'},
    '73': {'en': 'stadium', 'ar': 'ملعب'},
    '74': {'en': 'storage', 'ar': 'تخزين'},
    '75': {'en': 'store', 'ar': 'متجر'},
    '76': {'en': 'subway station', 'ar': 'محطة مترو'},
    '77': {'en': 'taxi stand', 'ar': 'موقف سيارات أجرة'},
    '78': {'en': 'train station', 'ar': 'محطة قطار'},
    '79': {'en': 'transit station', 'ar': 'محطة نقل'},
    '80': {'en': 'travel agency', 'ar': 'وكالة سفر'},
    '81': {'en': 'university', 'ar': 'جامعة'},
    '82': {'en': 'veterinary care', 'ar': 'رعاية بيطرية'},
    '81': {'en': 'zoo', 'ar': 'حديقة حيوان'}
    '82': {'en': 'law firm', 'ar': 'مكتب محاماة'},
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
