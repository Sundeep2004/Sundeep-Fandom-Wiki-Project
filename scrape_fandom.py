import requests
from bs4 import BeautifulSoup
import csv

# ---------- CONFIGURATION ----------
fandom_url = "https://memory-alpha.fandom.com/wiki/Portal:Main"  # Change this to your target Fandom page
output_csv = "fandom_links.csv"
base_url = "https://memory-alpha.fandom.com"  # Base Fandom URL
# -----------------------------------

def scrape_fandom_article(url):
    print(f"Fetching article: {url}")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")  # Get only text from paragraphs
    dataset = []

    for para in paragraphs:
        sentence = para.get_text().strip()
        
        # Find all links in this paragraph
        for link in para.find_all("a"):
            linked_word = link.get_text().strip()
            href = link.get('href')

            if href and href.startswith('/wiki/'):  # Only internal links
                start_pos = sentence.find(linked_word)
                end_pos = start_pos + len(linked_word)

                dataset.append({
                    "sentence": sentence,
                    "linked_word": linked_word,
                    "start": start_pos,
                    "end": end_pos,
                    "url": base_url + href
                })

    print(f"Extracted {len(dataset)} links.")
    return dataset

def save_to_csv(dataset, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['sentence', 'linked_word', 'start', 'end', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    print(f"Dataset saved to {output_file}")

def main():
    dataset = scrape_fandom_article(fandom_url)
    if dataset:
        save_to_csv(dataset, output_csv)

if __name__ == "__main__":
    main()