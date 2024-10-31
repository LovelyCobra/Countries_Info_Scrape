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
    
    if "COUNTRIES" not in os.listdir(save_dir):
        os.mkdir(os.path.join(save_dir, "COUNTRIES"), mode=0o777)
    save_dir = os.path.join(save_dir, "COUNTRIES")
    
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
            country_txt = open(os.path.join(save_dir, f"{country}.txt"), 'w', encoding='utf-8')
            
            try: 
                browser.open(wiki_addr)
                par = browser.page.find_all('p', attrs={"class": None})
                par_txt = [value.text for value in par]
                
                if "in Europe" in par_txt[0]:
                    first_par = par_txt[1]
                else:
                    first_par = par_txt[0]
                    
                file.write(f"{first_par}\n")
                country_txt.write(f"{country.upper()}\n\n")
                country_txt.write(f"{first_par}\n")
                
                th = browser.page.find_all("th", attrs={"class": "infobox-label"})  
                th_text = [value.text for value in th]                              
                td = browser.page.find_all("td", attrs={"class": "infobox-data"})   
                td_text = [value.text for value in td]                              
                
                for index, line in enumerate(th_text):
                    file.write(f"\n{line}: {td_text[index]}\n")
                    country_txt.write(f"\n{line}: {td_text[index]}\n")
                
                
            except:
                miss.append(country)
                
            country_txt.close()
    
    browser.close()
    return miss
    
    
    
    
    
if __name__ == '__main__':
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    miss = countries_info_scrap()
    print(f"\n\nBasic info about 195 sovereign states has been scraped from the Wikipedia website\nand saved in the '\033[92mCOUNTRIES_info.txt\033[0m' text file, as well as in separate txt files for each state,\nin the \033[92mDocuments/COUNTRIES\033[0m suddirectory of your user's home directory.\n\n")
    if miss != []:
        print("\n\nScraping \033[91mfailed\033[0m for these countries:\n\n")
        for country in miss:
            print(country)
