import requests
from bs4 import BeautifulSoup
import csv

def contains_keywords(tag):
    # Check if the argument is a BeautifulSoup Tag
    if not tag or not hasattr(tag, 'get_text'):
        return False

    # List of keywords to search for
    keywords = ['symptoms']
    
    # Return True if the tag contains any of the keywords
    tag_text = tag.get_text()
    return any(keyword in tag_text for keyword in keywords)

def scrape_url(url, desc):
    try:
        response = requests.get("https://www.obd-codes.com/" + str(url))
        print("https://www.obd-codes.com/" + str(url))
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        soup = BeautifulSoup(response.text, 'html.parser')

        keyword = 'symptom'

        # Find the <h2> tag that contains the specified keyword
        h2_tag = soup.find(lambda tag: tag.name == 'h2' and keyword.lower() in tag.get_text().lower())

        # Initialize an empty list to store the list items
        symptom_items = []
        causes_items = []
        # Check if the <h2> tag was found
        if h2_tag:
            # Find the next sibling that is either <ul> or <ol>
            list_container = h2_tag.find_next_sibling(lambda tag: tag.name in ['ul', 'ol'])

            # Check if a list container is found
            if list_container:
                # Find all <li> elements within the list container
                symptom_items = ', '.join([li.get_text().strip() for li in list_container.find_all('li')])

        h2_tag = soup.find(lambda tag: tag.name == 'h2' and 'causes' in tag.get_text().lower())
        if h2_tag:
            # Find the next sibling that is either <ul> or <ol>
            list_container = h2_tag.find_next_sibling(lambda tag: tag.name in ['ul', 'ol'])

            # Check if a list container is found
            if list_container:
                # Find all <li> elements within the list container
                causes_items = ', '.join([li.get_text().strip() for li in list_container.find_all('li')])

        mydict = [{'code': str(url).upper(), 'description': str(desc), 'symptoms': str(symptom_items), 'causes': str(causes_items)}]
 
        # field names
        fields = ['code', 'description', 'symptoms', 'causes']
        
        # name of csv file
        filename = 'C:/Users/Samue/Documents/OBDWebscraper/finished_codes.csv'
        
        # writing to csv file
        with open(filename, 'a',newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)
        
            # writing data rows
            writer.writerows(mydict)
        
    except requests.RequestException as e:
        print(e)
        mydict = [{'code': str(url).upper(), 'description': str(desc), 'symptoms': 'NA', 'causes': 'NA'}]
 
        # field names
        fields = ['code', 'description', 'symptoms', 'causes']
        
        # name of csv file
        filename = 'C:/Users/Samue/Documents/OBDWebscraper/finished_codes.csv'
        
        # writing to csv file
        with open(filename, 'a',newline='') as csvfile:
            # creating a csv dict writer object
            writer = csv.DictWriter(csvfile, fieldnames=fields)
        
            # writing data rows
            writer.writerows(mydict)
        return None

def main():
    with open('C:/Users/Samue/Documents/OBDWebscraper/obd-trouble-codes.csv') as file_obj: 
      
        # Create reader object by passing the file 
        # object to DictReader method 
        reader_obj = csv.DictReader(file_obj) 
        
        # Iterate over each row in the csv file 
        # using reader object 
        scrape_url('P0100', 'Mass or Volume Air Flow Circuit Malfunction')
        for row in reader_obj: 
            scrape_url(str(row['P0100']), str(row['Mass or Volume Air Flow Circuit Malfunction']))


if __name__ == "__main__":
    main()
