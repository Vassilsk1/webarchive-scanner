import requests
import json

def check_cdx_archive(username):
    # Expanded list with common CTF patterns
    # We use the wildcard * at the end to catch variations in URLs
    base_urls = [
        f"twitter.com/{username}",
        f"facebook.com/{username}",
        f"instagram.com/{username}",
        f"github.com/{username}",
        f"reddit.com/user/{username}",
        f"linkedin.com/in/{username}"
    ]
    
    print(f"[*] Scoping Wayback CDX for: {username}\n")
    
    for base in base_urls:
        # matchType=prefix catches any sub-pages or trailing slash variations
        # limit=1 just gets us the most recent proof of existence
        cdx_url = f"https://web.archive.org/cdx/search/cdx?url={base}*&output=json&limit=1"
        
        try:
            response = requests.get(cdx_url)
            
            # CDX returns an empty string or [] if nothing is found
            if response.text.strip() == "[]" or not response.text.strip():
                print(f"[-] No results: {base}")
                continue

            data = response.json()
            
            if len(data) > 1: # Index 0 is the header row
                header = data[0]
                entry = data[1]
                
                # Mapping the columns (usually: urlkey, timestamp, original, mimetype, statuscode, digest, length)
                result = dict(zip(header, entry))
                
                timestamp = result['timestamp']
                original = result['original']
                archive_url = f"https://web.archive.org/web/{timestamp}/{original}"
                
                print(f"[+] MATCH FOUND: {base}")
                print(f"    - Original: {original}")
                print(f"    - Saved on: {timestamp}")
                print(f"    - Link:     {archive_url}\n")

        except Exception as e:
            print(f"[!] Error querying {base}: {e}")

check_cdx_archive("justinccase2511")