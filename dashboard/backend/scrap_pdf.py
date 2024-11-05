import pymupdf, re
from copy import deepcopy
import csv
"""
Trein prijzen 2019 ->
    - start heading: Enkele Reizen & Dagretours\n
    - end heading Enkele Reizen NS Flex\n
Trein prijzen 2017 ->
    - start chapter: Enkele Reizen & Dagretours\n
    - end chapter: Traject Vrij\n
"""
# read pdf file with pymupdf from data/treinprijzen2019.pdf
pdf_path = './data/treinprijzen2024.pdf'
pdf = pymupdf.open(pdf_path)

print("hello world")

def find_pages_by_chapter(pdf_document, chapter, next_chapter):
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)

        text = page.get_text()
        matchChapter = re.search(fr'{chapter}\s*(\d+)', text)
        matchNextChapter = re.search(fr'{next_chapter}\s*(\d+)', text)

        if matchChapter and matchNextChapter:
            startnumber = matchChapter.group(1)
            endNumber = matchNextChapter.group(1)
            return int(startnumber) - 1, int(endNumber) - 2

    return None


def extract_prices_from_page(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    tables = page.find_tables()

    if not tables:
        return None

    table = tables[0].extract()
    table_values = table[len(table) - 1]

    def price_list_formatter(x):
        return list(map(float, str(x).replace(" ", "").replace("€", "").replace(",", ".").split('\n')))

    tariff_units = str(table_values[0]).replace(" ", "").split("\n")
    second_class_full_tariff = price_list_formatter(table_values[1])
    second_class_20_discount_tariff = price_list_formatter(table_values[2])
    second_class_40_discount_tariff = price_list_formatter(table_values[3])
    first_class_prices = price_list_formatter(table_values[4])
    first_class_20_discount_tariff = price_list_formatter(table_values[5])
    first_class_prices_class_40_discount_tariff = price_list_formatter(table_values[6])

    combined_price_list = []
    for i in range(len(tariff_units)):
        combined_price_list.append({
            "tariff_units": tariff_units[i],
            "second_class_full_tariff": second_class_full_tariff[i],
            "second_class_20_discount_tariff": second_class_20_discount_tariff[i],
            "second_class_40_discount_tariff": second_class_40_discount_tariff[i],
            "first_class_prices": first_class_prices[i],
            "first_class_20_discount_tariff": first_class_20_discount_tariff[i],
            "first_class_prices_class_40_discount_tariff": first_class_prices_class_40_discount_tariff[i]
        })

    if "t/m" in combined_price_list[0]["tariff_units"]:
        tariff_units_range = list(map(int, combined_price_list[0]["tariff_units"].split("t/m")))
        x = tariff_units_range[0]
        while x <= tariff_units_range[1]:
            price = deepcopy(combined_price_list[0])
            price['tariff_units'] = x
            combined_price_list.append(price)
            x += 1
        del combined_price_list[0]

    return combined_price_list


pages_with_prices = find_pages_by_chapter(pdf, "Enkele Reizen & Dagretours\n",
                                          "Enkele Reizen NS Flex\n")

if pages_with_prices:
    prices = []
    i = pages_with_prices[0]
    while i <= pages_with_prices[1]:
        prices_from_page = extract_prices_from_page(pdf, i)
        prices += prices_from_page
        i += 1

    with open('./data/prices.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=prices[0].keys())
        writer.writeheader()
        for price in prices:
            writer.writerow(price)


print(prices)
