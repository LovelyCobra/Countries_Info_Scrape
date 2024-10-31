import os
import mechanicalsoup as ms
from pathlib import Path
from tqdm import tqdm

# SCRAPING quick basic info about countries in the "List of Sovereign States" on Wikipedia

def countries_info_scrap():
    browser = ms.StatefulBrowser()
    
    countries_list_site = "https://en.wikipedia.org/wiki/List_of_sovereign_states"
    root_path = "https://en.wikipedia.org/wiki/"
    save_dir = os.path.join(str(Path.home()), "Documents")
    save_dir = save_dir.replace('\\', '/')
    
    browser.open(countries_list_site)
        
    b = browser.page.find_all('b')
    b_text = [value.text for value in b][2:197]
    
    clean_countries_list = [item[1:].replace('\xa0', '') for item in b_text]
    miss = []
    
    with open(os.path.join(save_dir, "COUNTRIES_info.txt"), 'w', encoding='utf-8') as file:
        file.write("COUNTRIES - Basic Information\n\n")
        
        for country in tqdm(clean_countries_list, desc=f"Processing:", ascii=True, colour='green'):
            file.write(f"\n{country.upper()}\n\n")
            country = country.replace(' ', '_')
            wiki_addr = root_path + country
            
            try: 
                browser.open(wiki_addr)
                par = browser.page.find_all('p', attrs={"class": None})
                first_par = [value.text for value in par][0]
                file.write(f"{first_par}\n")
                
                th = browser.page.find_all("th", attrs={"class": "infobox-label"})  
                th_text = [value.text for value in th]                              
                td = browser.page.find_all("td", attrs={"class": "infobox-data"})   
                td_text = [value.text for value in td]                              
                
                for index, line in enumerate(th_text):
                    file.write(f"\n{line}: {td_text[index]}\n")
                
                
            except:
                miss.append(country)
    
    browser.close()            
    return miss
    
    
    
    
    
if __name__ == '__main__':
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    miss = countries_info_scrap()
    print(f"\n\nBasic info has been scraped from the Wikipedia website\nand saved in the '\033[92mCOUNTRIES_info.txt\033[0m' text file in the \033[92mDocuments\033[0m suddirectory of your user's home directory.")
    if miss != []:
        print("\n\nScraping \033[91mfailed\033[0m for these countries:\n\n")
        for country in miss:
            print(country)