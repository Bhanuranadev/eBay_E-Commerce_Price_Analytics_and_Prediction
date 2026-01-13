import requests
import pandas as pd
import os

# =================================================
# 1. EBAY API KEY (SANDBOX)
# =================================================
EBAY_APP_ID = "BharmanR-Ecommerc-SBX-b95844d28-47cce072"

# =================================================
# 2. PATH SETUP (SAFE FOR WINDOWS)
# =================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_FILE = os.path.join(DATA_DIR, "raw_data.csv")

# =================================================
# 3. EBAY FINDING API (SANDBOX URL)
# =================================================
API_URL = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"

# =================================================
# 4. API PARAMETERS
# =================================================
BASE_PARAMS = {
    "OPERATION-NAME": "findItemsByKeywords",
    "SERVICE-VERSION": "1.0.0",
    "SECURITY-APPNAME": EBAY_APP_ID,
    "RESPONSE-DATA-FORMAT": "JSON",
    "REST-PAYLOAD": "",
    "keywords": "laptop",
    "paginationInput.entriesPerPage": 50
}

# =================================================
# 5. FETCH DATA
# =================================================
items = []

for page in range(1, 6):  # 5 pages → ~200–250 products
    print(f"Fetching page {page}")

    BASE_PARAMS["paginationInput.pageNumber"] = page

    response = requests.get(API_URL, params=BASE_PARAMS)
    data = response.json()

    try:
        results = data["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
    except:
        results = []

    for product in results:
        items.append({
            "title": product.get("title", [None])[0],
            "price": float(
                product["sellingStatus"][0]["currentPrice"][0]["__value__"]
                
            ),
            "currency": product["sellingStatus"][0]["currentPrice"][0]["@currencyId"],
            "category": product["primaryCategory"][0]["categoryName"][0],
            "condition": product.get("condition", [{}])[0].get(
                "conditionDisplayName", [None]
            )[0],
            "item_url": product.get("viewItemURL", [None])[0]
        })

# =================================================
# 6. SAVE TO CSV
# =================================================
df = pd.DataFrame(items)
df.to_csv(OUTPUT_FILE, index=False)

print("===================================")
print("EBAY DATA COLLECTED SUCCESSFULLY ✅")
print("Total products:", len(df))
print("Saved at:", OUTPUT_FILE)
print("===================================")
