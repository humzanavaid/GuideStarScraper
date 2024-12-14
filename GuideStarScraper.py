from bs4 import BeautifulSoup
import requests
import pandas as pd
from lxml import html

# Function to extract data 1 (primary data point)


def get_name(soup):
    # Locate the <td> element with the specific class
    div_tag = soup.find('div', class_=['CPBData',"GovernenceData"])
    
    # Check if the <td> tag is found and has a nested <span> containing the data
    if div_tag:
        # Extract text from within the <span> tag that holds the desired data
        data_name = div_tag.find('span').get_text(strip=True)
        return data_name
    else:
        return None





def get_data_1(soup):
    # Locate the <td> element with the specific class
    td_tag = soup.find('td', class_='GSBorderTableItemRow', width="25%")
    
    # Check if the <td> tag is found and has a nested <span> containing the data
    if td_tag:
        # Extract text from within the <span> tag that holds the desired data
        data_1_text = td_tag.find('span').get_text(strip=True)
        return data_1_text
    else:
        return None
    

# Function to extract data 2
def get_data_2(soup):
    # Locate all <div> elements with the specific class
    div_tags = soup.find('div', class_='CPBData')

    if div_tags:  
        span_tag = div_tags.find('span', class_=False)
        
        if span_tag:

            data_2_text = span_tag.get_text(strip=True)  # Getting text from the second <span>
            return data_2_text
    return None


# Function to extract data 3
def get_data_3(soup):
    # Locate all <div> elements with the specific class 'CPBData'
    div_tags = soup.find_all('div', class_='CPBData')

    for div_tag in div_tags:
        # Find the <span> with the specific class for data 3
        target_span = div_tag.find('span', class_='SectionPlaceHolder1_ctl01_DynVariableList1_ctl15_TextControl4_desc')

        if target_span:
            # Get the next <span> sibling (same level)
            next_span = target_span.find_next_sibling('span', class_=False)

            if next_span:
                # Return the text of the next <span> as data point 3
                return next_span.get_text(strip=True)

    return None




# Function to extract data 4
def get_data_4(soup):
    # Locate all <div> elements with the specific class 'CPBData'
    div_tags = soup.find_all('div', class_='CPBData')

    for div_tag in div_tags:
        # Find the <span> with the specific class for data 4
        target_span = div_tag.find('span', class_='SectionPlaceHolder1_ctl01_DynVariableList1_ctl18_TextControl4_desc')

        if target_span:
            # Get the next <span> sibling (same level)
            next_span = target_span.find_next_sibling('span', class_=False)

            if next_span:
                # Return the text of the next <span> as data point 4
                return next_span.get_text(strip=True)

    return None


# Function to extract data 5
# Function to extract data 5
def get_data_5(soup):
    # Locate the <div> element with the specific class
    div_tag = soup.find('div', class_='CPBData')
    
    # Check if the <div> tag is found
    if div_tag:
        # Locate all <span> elements within the <div>
        span_tags = div_tag.find_all('span')
        
        # Check if there are enough spans, then extract the text from the second <span>
        if len(span_tags) > 1:
            data_5_text = span_tags[1].get_text(strip=True)  # Getting text from the second <span>
            return data_5_text
    return None

if __name__ == '__main__':

    # User agent to mimic a browser request
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

    # List to store extracted data
    data_list = []

    # Loop through a range of page numbers (adjust based on the actual number of pages)
    for page_number in range(15001, 20000):  # Adjust the range as needed
        URL = f"https://guidestarindia.org/Documents.aspx?CCReg={page_number}"

        try:
            # Make the HTTP request with a timeout to handle unresponsive pages
            webpage = requests.get(URL, headers=HEADERS, timeout=15)
            webpage.raise_for_status()  # Raise an error for HTTP issues like 404, 500

            # Parse the page content
            soup = BeautifulSoup(webpage.content, "html.parser")

            # Extract data points individually
            data_name = get_name(soup)

            # Skip if "data_name" is not present
            if not data_name:
                continue

            # Extract other data points only if "data_name" is present
            data_1 = get_data_1(soup)
            data_2 = get_data_2(soup)
            
            # Append to data list
            data_list.append({
                'page': page_number,
                'name': data_name,
                'data 1': data_1,
                'data 2': data_2,
                # Add additional data points if needed
            })
            print(f"Data extracted for page {page_number}")

        except requests.exceptions.Timeout:
            print(f"Timeout error: Skipping URL {URL}")

        except requests.exceptions.RequestException as e:
            print(f"Request error for {URL}: {e}")

    # Convert data list to DataFrame and save to CSV
    df = pd.DataFrame(data_list)
    df.to_csv('data_points_15_to_20.csv', index=False)

    print("Data extraction completed!")
