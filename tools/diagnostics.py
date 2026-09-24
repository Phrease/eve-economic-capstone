import requests

# Target Jita without the /page/ modifier to test base access
url = "https://zkillboard.com/api/solarSystemID/30000142/"

# zKillboard prefers strict application/json and gzip encoding to save bandwidth
headers = {
    'User-Agent': 'Maintainer: ryan.durkin@csuglobal.edu',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate'
}

print("Testing zKillboard connection...")
response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Raw Response Length: {len(response.text)} characters")

# Attempt to parse the first 200 characters to identify Cloudflare HTML blocks
if response.status_code == 200 and len(response.text) > 0:
    try:
        data = response.json()
        print(f"Success! Retrieved {len(data)} killmails.")
    except Exception as e:
        print(f"Failed to parse JSON. Raw text snippet:\n{response.text[:200]}")
else:
    print("Server returned an empty response. You are currently under a temporary IP cooldown.")