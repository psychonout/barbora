from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


base = "https://www.barbora.lt"
url = base + "/paieska?uzklausa=" + "sausainiai"
paged = []

while True:
    soup = bs(urlopen(url), 'lxml')
    for i in soup.find("html"):
        try:
            print(i.contents[0])
        except Exception:
            pass
    break
    products = soup.find_all(class_="b-product-wrap-img")
    product_info = soup.find_all(class_="b-product-info-wrap")

    for index, product in enumerate(products):
        title = product.find("span").contents[0].strip()
        price = product.find(class_="b-product-price-current-number").contents[0].strip()
        discount = False

        try:
            look_for = "b-product-promo-label-primary--percent"
            discount = product_info[index].find(class_=look_for).contents[0].strip()
        except Exception:
            pass
        print(f"{price:>7} {discount:^5} {title}")

    try:
        next_page = soup.find(class_="pagination").find_all("li")[-1].find("a", href=True)["href"]
    except Exception:
        break

    if next_page not in paged:
        paged.append(next_page)
        url = base + next_page
    else:
        print("Escaping while going to the next page")
        break