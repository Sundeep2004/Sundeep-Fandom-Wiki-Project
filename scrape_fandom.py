import requests
from bs4 import BeautifulSoup
import csv
import json
from tabulate import tabulate

# ---------- CONFIGURATION ----------
FANDOM_URL = "https://memory-alpha.fandom.com/wiki/Portal:Main"  # Change to your target Fandom page
OUTPUT_CSV = "fandom_links.csv"
OUTPUT_JSON = "fandom_links.json"
BASE_URL = "https://memory-alpha.fandom.com"  # Base Fandom URL
# -----------------------------------

def scrape_fandom_article(url):
    print(f"\n🔍 Fetching article: {url} ...")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Failed to retrieve page. Status code: {response.status_code}")
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
                    "url": BASE_URL + href
                })

    print(f"\n✅ Extracted {len(dataset)} links successfully!\n")
    return dataset

def save_to_csv(dataset, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['sentence', 'linked_word', 'start', 'end', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    print(f"📁 CSV file saved: {output_file}")

def save_to_json(dataset, output_file):
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(dataset, jsonfile, indent=4, ensure_ascii=False)
    print(f"📁 JSON file saved: {output_file}")

def display_table(dataset):
    table_data = [[d["linked_word"], d["start"], d["end"], d["url"]] for d in dataset]
    print("\n📌 Extracted Links:\n")
    print(tabulate(table_data, headers=["Linked Word", "Start", "End", "URL"], tablefmt="fancy_grid"))

def main():
    dataset = scrape_fandom_article(FANDOM_URL)
    if dataset:
        save_to_csv(dataset, OUTPUT_CSV)
        save_to_json(dataset, OUTPUT_JSON)
        display_table(dataset)

if __name__ == "__main__":
    main()