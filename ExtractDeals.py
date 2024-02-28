import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm


def extract_deals_table(file_path):
    start_time = datetime.now()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-16") as file:
            html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    deals_div = soup.find("div", string=lambda text: text and "Deals" in text)
    if not deals_div:
        print("'Deals' not found")
        return

    deals_tr = deals_div.find_parent("tr")
    if not deals_tr:
        print("'Deals' not found")
        return

    rows = []
    all_rows = deals_tr.find_all_next("tr")[1:]
    for row in tqdm(all_rows, desc="Extracting rows"):  # Usa tqdm aquí
        cols = [ele.text.strip() for ele in row.find_all("td")]
        if not all(col in [None, "", "-"] for col in cols):
            rows.append(cols)
        else:
            break

    table_headers = [
        "Time",
        "Deal",
        "Symbol",
        "Type",
        "Direction",
        "Volume",
        "Price",
        "Order",
        "Commission",
        "Swap",
        "Profit",
        "Balance",
        "Comment",
    ]
    df = pd.DataFrame(rows, columns=table_headers)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Data extraction took: {duration}")

    return df


file_path = r"C:\Users\Admin\Desktop\ReportTester.html"
deals_df = extract_deals_table(file_path)
print(deals_df)
