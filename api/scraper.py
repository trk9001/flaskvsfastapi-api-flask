__all__ = ['extract_chaldal_products']

import time

import bs4
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

_chaldal_category_urls = [
    'https://chaldal.com/newborn-essentials',
    'https://chaldal.com/wipes',
    'https://chaldal.com/diapers',
    'https://chaldal.com/feeders',
    'https://chaldal.com/formula',
    'https://chaldal.com/toddler-food',
    'https://chaldal.com/milk-juice-drinks',
    'https://chaldal.com/bath-skincare',
    'https://chaldal.com/baby-accessories',
    'https://chaldal.com/baby-oral-care',
    'https://chaldal.com/kitten-food',
    'https://chaldal.com/cat-food',
    'https://chaldal.com/dog-food',
    'https://chaldal.com/other-pet-foods',
    'https://chaldal.com/pet-accessories',
    'https://chaldal.com/fresh-fruit',
    'https://chaldal.com/fresh-vegetable',
    'https://chaldal.com/keto-food',
    'https://chaldal.com/local-breakfast',
    'https://chaldal.com/energy-boosters',
    'https://chaldal.com/cereals',
    'https://chaldal.com/dips-spreads',
    'https://chaldal.com/tea-coffee',
    'https://chaldal.com/coffee-2',
    'https://chaldal.com/juice',
    'https://chaldal.com/soft-drinks',
    'https://chaldal.com/water',
    'https://chaldal.com/powder-mixes',
    'https://chaldal.com/meat',
    'https://chaldal.com/fresh-fish-2',
    'https://chaldal.com/dried-fish',
    'https://chaldal.com/dried-fish',
    'https://chaldal.com/noodles',
    'https://chaldal.com/soups',
    'https://chaldal.com/pasta-macaroni',
    'https://chaldal.com/candy-chocolate',
    'https://chaldal.com/local-snacks',
    'https://chaldal.com/chips-pretzels',
    'https://chaldal.com/popcorn-nuts',
    'https://chaldal.com/biscuits',
    'https://chaldal.com/salad-dressing',
    'https://chaldal.com/sauces',
    'https://chaldal.com/liquid-uht-milk',
    'https://chaldal.com/butter-sour-cream',
    'https://chaldal.com/cheese-2',
    'https://chaldal.com/eggs',
    'https://chaldal.com/milk-cream',
    'https://chaldal.com/yogurt',
    'https://chaldal.com/ice-cream',
    'https://chaldal.com/frozen-snacks',
    'https://chaldal.com/canned-meat-seafood',
    'https://chaldal.com/cookies',
    'https://chaldal.com/bakery-snacks',
    'https://chaldal.com/breads',
    'https://chaldal.com/jams-spreads',
    'https://chaldal.com/honey',
    'https://chaldal.com/cakes',
    'https://chaldal.com/nuts-dried-fruits',
    'https://chaldal.com/baking-tools',
    'https://chaldal.com/baking-mixes',
    'https://chaldal.com/baking-ingredients',
    'https://chaldal.com/flour',
    'https://chaldal.com/rice-2',
    'https://chaldal.com/premium-ingredients',
    'https://chaldal.com/colors-flavours',
    'https://chaldal.com/pickles',
    'https://chaldal.com/spices',
    'https://chaldal.com/oil',
    'https://chaldal.com/ghee',
    'https://chaldal.com/ready-mix',
    'https://chaldal.com/salt-sugar',
    'https://chaldal.com/dal-or-lentil',
    'https://chaldal.com/miscellaneous',
    'https://chaldal.com/shemai-suji',
    'https://chaldal.com/sugar-substitutes',
    'https://chaldal.com/air-freshners',
    'https://chaldal.com/dish-detergents',
    'https://chaldal.com/cleaning-supplies',
    'https://chaldal.com/kitchen-accessories',
    'https://chaldal.com/laundry',
    'https://chaldal.com/paper-products',
    'https://chaldal.com/pest-control',
    'https://chaldal.com/shoe-care',
    'https://chaldal.com/tableware-trash-bags',
    'https://chaldal.com/food-storage',
    'https://chaldal.com/cleaning-accessories',
]


def _get_chaldal_page_products(webdriver: WebDriver, url: str) -> list[dict]:
    """Scrape a chaldal.com page's source for its products' info."""
    web = webdriver
    web.get(url)

    # Scroll down the page to trigger lazy loads.
    lazy_load_trigger_time = 0.5  # In seconds.
    height = web.execute_script('return document.body.scrollHeight')
    while True:
        web.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(lazy_load_trigger_time)
        new_height = web.execute_script('return document.body.scrollHeight')
        if new_height > height:
            height = new_height
        else:
            break

    soup = bs4.BeautifulSoup(web.page_source, 'lxml')
    category_header = soup.find('div', class_='categoryHeader')
    category_name = category_header.find('div', class_='name').string

    products: list[dict] = []
    product_pane = soup.find('div', class_='productPane')
    for product in product_pane('div', class_='product', recursive=False):  # type: bs4.Tag
        product_info = {
            'category': category_name,
            'name': product.find('div', class_='name').string,
            'amount': product.find('div', class_='subText').string,
            'price': product.find('div', class_='price')('span')[1].string
        }
        products.append(product_info)

    return products


def extract_chaldal_products() -> list[dict]:
    """Scrape chaldal.com for their products and return their info.

    Super categories included:
    - Baby Care
    - Pet Care
    - Food

    A product's information includes:
    - its category
    - its name
    - its amount (for which its price is applicable)
    - its price
    """
    options = FirefoxOptions()
    options.headless = True
    fox = Firefox(options=options)
    all_products: list[dict] = []

    for url in _chaldal_category_urls:
        products = _get_chaldal_page_products(fox, url)
        all_products.extend(products)

    fox.quit()
    return all_products
