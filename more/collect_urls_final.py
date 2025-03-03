import subprocess
import csv
import json
import signal
import time
import re
import os
import io
import pandas as pd
from typing import List
from datetime import datetime
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse


# Run the playwright install-deps command
#subprocess.run(["/opt/venv/bin/playwright", "install"], check=True)

# Run the playwright install-deps command
#subprocess.run(["/opt/venv/bin/playwright", "install-deps"], check=True)


# Set the timeout duration (in seconds)
timeout_duration = 240 # 480 # 360   # 30  # 60
#timeout_duration = float('inf')   # Set to infinity
wait_sleep = 1  #2   #3
#wait_timeout= 4000   # 10000 suggested by DeepSeek


# Start the timer
start_time = time.time()

targetURL = 'https://group.mercedes-benz.com/sustainability/sustainability-reports-archive.html'
base_path = "/teamspace/studios/this_studio"
sub_directory = "XtractnParse"
# Get the value of the PWD environment variable
pwd_dir = os.getenv('PWD')
file_name = "urls1.csv"

yearEnd = 2023
yearStart = 2014
#This flag determines whether there are hidden elements that need to be expanded
ExpandHidden = False # True; # 

topLevelURL = 'https://group.mercedes-benz.com'
#topLevelURL = 'https://group.mercedes-benz.com/investors/'
#topLevelURL = 'https://www.siemens.com/global/en/company/investor-relations.html'

depth = 2  #3  # Maximum depth of URLs to collect
# Topic to search for in URLs
topics = ['sustainability', 'ESG', 'environment', 'social', 'governance', 'corporate responsibility', 'transparency'] 
collections = ['report', 'document', 'archive']
keywords = topics + collections

# List of file extensions to exclude
excluded_extensions = ['.pdf', '.ics', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mkv', '.mov', '.exe', '.dmg']


def commonDomain(url, benchmarkURL):
    # Verify it starts with benchmarkURL
    if not url.startswith(benchmarkURL):
        # Extract netlocs
        url_netloc = urlparse(url).netloc
        benchmark_netloc = urlparse(benchmarkURL).netloc
        
        # Split netlocs into components
        url_parts = url_netloc.split('.')
        benchmark_parts = benchmark_netloc.split('.')
        
        # Compare highest two-level domains
        if url_parts[-2:] == benchmark_parts[-2:] and len(url_parts) >= 2:
            return True
        return False
    return True


def is_excluded(url):
    """
    Enhanced URL filtering with multiple checks.
    Returns True if URL should be excluded, False if it should be kept.
    """
    try:
        # Check for None or empty URLs
        if not url:
            return True
            
        # Basic extension check
        if any(url.lower().endswith(ext) for ext in excluded_extensions):
            return True
                       
        # Check if it does not share the highest two-level domain with topLevelURL
        if not commonDomain(url, topLevelURL):
            return True
        #==============================================================================
        # Verify it starts with topLevelURL
        #if not url.startswith(topLevelURL):
        #    return True
        #==============================================================================
            
        # Additional safety checks can be added here
        
        return False
    except Exception as e:
        print(f"Error in is_excluded for URL {url}: {str(e)}")
        return True





def filter_urls(urls):
    # Step 1: Sort URLs to ensure higher-level URLs come first
    urls = sorted(urls)  # Sort the set of URLs
    
    # Step 2: Retain only non-lower-level URLs
    result = []
    for url in urls:
        if not is_excluded(url) and not any(url.startswith(retained_url) and url != retained_url for retained_url in result):
            result.append(url)
    
    return result



def save_urls_to_csv(filename, urls):
    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['URL'])  # Write the header
        for url in sorted(urls):
            writer.writerow([url])


def timeout_handler(signum, frame):
    print("Timeout reached, saving collected URLs to CSV.")
    #=============================================================
    # Post processing with postprocess() function
    #all_urls = postprocess(all_urls, topLevelURL)
    #=============================================================
    save_urls_to_csv('AllURLs.csv', all_urls)

    save_urls_to_csv('visitedURLs.csv', visited_urls)
    # Calculate and print the total processing time
    end_time = time.time()
    total_processing_time = end_time - start_time
    print(f"Total processing time: {total_processing_time:.2f} seconds")

    exit(0)


#==============================================================================
def clean_url_segment(segment):
    return re.sub(r'[^a-zA-Z0-9]', '', segment).lower()

def matches_keywords(url, keywords):
    segments = urlparse(url).path.split('/')
    for segment in segments:
        cleaned_segment = clean_url_segment(segment)
        for keyword in keywords:
            cleaned_keyword = clean_url_segment(keyword)
            if cleaned_keyword in cleaned_segment:
                return True
    return False
#==============================================================================



def preprocess_href(href):
    # Remove all spaces
    href = href.replace(' ', '')
    
    # Replace the first occurrence of :/ with :// if not already ://
    if '://' not in href:
        href = href.replace(':/', '://', 1)
    
    # Replace any occurrence of more than one consecutive / with a single /
    parts = href.split('://')
    if len(parts) > 1:
        scheme, rest = parts[0], parts[1]
        rest = rest.replace('//', '/')
        href = f'{scheme}://{rest}'
    else:
        href = href.replace('//', '/')
    
    return href


def get_all_urls(page, base_url): #, current_depth, max_depth):
#    if current_depth > max_depth:
#        return set()
    
    urls = set()
    anchors = page.query_selector_all('a[href]')
    for anchor in anchors:
        href = anchor.get_attribute('href')
        href = preprocess_href(href)
        
        parsed_href = urlparse(href)
        
        if not parsed_href.scheme:
            full_url = urljoin(base_url, href)
        elif parsed_href.scheme in ['http', 'https']:
            full_url = href
        
        if full_url:
            urls.add(full_url)
    
    return urls
#==============================================================================
#def get_all_urls(page, base_url):
#    urls = set()
#    anchors = page.query_selector_all('a[href]')
#    for anchor in anchors:
#        href = anchor.get_attribute('href')
#        full_url = urljoin(base_url, href)
#        parsed_url = urlparse(full_url)
#        if parsed_url.scheme in ['http', 'https']:
#            urls.add(full_url)
#    return urls
#==============================================================================



# Function to collect URLs starting from topLevelURL
# Main loop with depth and keyword matching
def collect_urls(page, base_url, current_depth, max_depth, all_urls_init):
#def collect_urls(page, base_url, current_depth, max_depth):
    if current_depth > max_depth or base_url in visited_urls: 
        #return set()
        return all_urls_init
    
    visited_urls.append(base_url)
    page.goto(base_url, wait_until="domcontentloaded")
#    time.sleep(wait_sleep)  # Add an additional x seconds wait
    urls = get_all_urls(page, base_url) #, current_depth, max_depth)
    filtered_urls = {url for url in urls if matches_keywords(url, keywords) and not is_excluded(url)}
    filtered_urls = sorted(filtered_urls)  # Sort the set into a list
    #==============================================================================
    # Get the current time and format it as a string
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #print(f"Exploring the following URL at the {current_depth}th level from a seed url: \n     [{timestamp}] {base_url}")

    #==============================================================================
    if targetURL in urls:
        print(f"  [{timestamp}] targetURL in urls")
    if base_url == targetURL:
        print(f"  [{timestamp}] Reaching targetURL: {base_url}")

#    save_urls_to_csv(f'urls_{timestamp}.csv', urls)
#    save_urls_to_csv(f'filtered_urls_{timestamp}.csv', filtered_urls)


    all_urls_init.update(urls)
    #all_collected_urls = {url for url in urls if commonDomain(url, topLevelURL)}
    for url in filtered_urls:   # navigate to only filtered urls
        all_urls_init.update(collect_urls(page, url, current_depth + 1, max_depth, all_urls_init))    
    return all_urls_init
    #return all_collected_urls

# Read URLs from urls1.csv
file_path = os.path.join(pwd_dir, file_name)  # full file path of urls1.csv
#file_path = os.path.join(base_path, sub_directory, file_name)  # full file path of urls1.csv
print(file_path)
with open(file_path, 'r') as infile:
    reader = csv.DictReader(infile)
    urls = [row['URL'] for row in reader if 'sustainability' in row['URL']]

# Filter URLs
seed_urls = filter_urls(urls)
# Write filtered URLs to URLseeds.csv
save_urls_to_csv('URLseeds.csv', seed_urls)
# Later collect all URLs from the URL seeds and also several levels down
all_urls = set(seed_urls)

# Load cookies and local storage
with open('cookies.json', 'r') as f:
    cookies = json.load(f)

with open('localStorage.json', 'r') as f:
    local_storage = json.load(f)


# Set the timeout signal handler
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(timeout_duration)


#==============================================================================
#def wait_for_network_idle():
#    try:
#        # Wait for network to be idle
#        page.wait_for_load_state('networkidle', timeout=wait_timeout)
#    except Exception as e:
#        print(f"Network idle timeout reached, continuing anyway: {e}")
#==============================================================================


# Initialize the list of visited URLs
visited_urls = list()

# Start the collection process
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    # Set cookies and local storage
    context.add_cookies(cookies)
    page = context.new_page()

    # Navigate to a valid URL before manipulating localStorage
    page.goto(topLevelURL)  # Replace with a valid URL

    page.evaluate("localStorage.clear();")
    for key, value in local_storage.items():
        page.evaluate(f"localStorage.setItem('{key}', '{value}');")

    #all_urls = set()
    all_urls = set(seed_urls)
    #==============================================================================
    # Collect URLs starting from seed URLs
    for base_url in seed_urls:
        print(f"Start exploring from the seed URL: {base_url}")
        #page.goto(base_url)#, wait_until="domcontentloaded")
        #time.sleep(wait_sleep)  # Add an additional x seconds wait
        all_urls.update(collect_urls(page, base_url, 1, depth, all_urls))
    #==============================================================================
    # Collect URLs starting from topLevelURL
    #all_urls = collect_urls(page, topLevelURL, 0, depth)
    #==============================================================================
    browser.close()
#==============================================================================
#with sync_playwright() as p:
#    browser = p.chromium.launch(headless=True)
#    context = browser.new_context()
#
#    # Set cookies and local storage
#    context.add_cookies(cookies)
#    page = context.new_page()
#
#    # Navigate to a valid URL before manipulating localStorage
#    page.goto(topLevelURL)  # Replace with a valid URL
#
#    page.evaluate("localStorage.clear();")
#    for key, value in local_storage.items():
#        page.evaluate(f"localStorage.setItem('{key}', '{value}');")
#
#    # Process second-level URLs
#    for seed in filtered_urls:
#        print(f"Navigating to seed URL: {seed}")
#        page.goto(seed)
#        seed_urls = get_all_urls(page, seed)
#        all_urls.update(seed_urls)
#        for url in seed_urls:
#            if not is_excluded(url):  # Skip URLs with excluded extensions
#                print(f"Navigating to URL: {url}")
#                page.goto(url)
#                all_urls.update(get_all_urls(page, url))
#
#    browser.close()
#==============================================================================

# Cancel the alarm if the process completes before the timeout
signal.alarm(0)


def extract_filename(url):
    return url.split('/')[-1]

def extract_extension(filename):
    if '.' in filename:
        # Split on the last dot
        extension = filename.split('.')[-1]
        # Remove any special character
        extension = re.split(r'[?#/]', extension)[0]
        return extension
    return ''

def postprocess(urls, topLevelURL):
    try:

        save_urls_to_csv('URLs.csv', urls)
        # Read the CSV file into a DataFrame
        df = pd.read_csv('URLs.csv', dtype=str)

        # Extract filenames and extensions
        df['Filename'] = df['URL'].apply(extract_filename)
        df['Extension'] = df['Filename'].apply(extract_extension)
        
        # Reorder columns
        df = df[['Extension', 'Filename', 'URL']]
        
        # Sort DataFrame
#        df_sorted = df.sort_values(['Extension', 'URL'])


        # Save to CSV
        df.to_csv('AllURLs.csv', index=False)
        #df_sorted.to_csv('AllURLs.csv', index=False)
        #return df_sorted['URL'].tolist()
        return df['URL'].tolist()
    except Exception as e:
        print(f"Error in postprocess: {str(e)}")
        return list(urls)

def keepPDF(urls):
    try:
        # Filter URLs that end with .pdf
        pdf_urls = [url for url in urls if url.lower().endswith('.pdf')]
        return pdf_urls
    except Exception as e:
        print(f"Error in keepPDF: {str(e)}")
        return []


#=============================================================
# Post processing with postprocess() function
all_urls = postprocess(all_urls, topLevelURL)
#=============================================================
# Write all collected pdf URLs to a new CSV file
save_urls_to_csv('pdfURLs.csv', keepPDF(all_urls))
save_urls_to_csv('visitedURLs.csv', visited_urls)

# Calculate and print the total processing time
end_time = time.time()
total_processing_time = end_time - start_time
print(f"Total processing time: {total_processing_time:.2f} seconds")

