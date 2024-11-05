import pymupdf
import csv

year = '2020'
pdf = pymupdf.open(f"./data/treinprijzen{year}.pdf")

startpage = 4
endpage = 7

i = startpage
price_list = []
while i < endpage:
    raw_prices = str(pdf.load_page(i).get_text().split("excl. BTW\n")[1]).split('\n')
    raw_prices = [item for item in raw_prices if '€' != item]
    format_check = lambda x: str(x) if '€' in x else '€ ' + str(x)

    x = 1
    while x < (len(raw_prices) - 1):
        price_list.append({
            "tariff_units": raw_prices[x],
            "second_class_full_tariff": format_check(raw_prices[x + 1]),
            "second_class_20_discount_tariff": format_check(raw_prices[x + 2]),
            "second_class_40_discount_tariff": format_check(raw_prices[x + 3]),
            "second_class_full_tariff_ex_tax": format_check(raw_prices[x + 4]),
        })

        x += 5

    i += 1

if len(price_list) > 0:
    with open(f'./data/treinprijzen{year}.csv', mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=price_list[0].keys())
        writer.writeheader()
        for price in price_list:
            writer.writerow(price)
