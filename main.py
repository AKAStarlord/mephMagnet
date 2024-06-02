import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        print(f"Hacker voice: I'm in. URL: {url}")
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage. Error: {e}")
        return None


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def extract_product_links(soup):
    product_grid = soup.find('div', id='product-grid')

    product_links = []
    if product_grid:
        # Find all divs with class "w-dyn-item list_item_cw"
        product_items = product_grid.find_all('div', class_='w-dyn-item list_item_cw')

        for item in product_items:
            # Find the <a> tag within each product item
            a_tag = item.find('a', href=True)
            if a_tag:
                full_link = f"https://mephistogenetics.com{a_tag['href']}"
                product_links.append(full_link)

    return product_links


def extract_product_data(soup):
    # Extract the good stuff
    strain = soup.find('h1', class_='heading-style-h3').text.strip()
    # price = soup.find('span', class_='price').text.strip() # idk why this isn't working rn
    genetics = soup.find('div', id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f1-d7b2c481").text.strip()
    seed_type = soup.find('div', id="w-node-_7f69a302-9b3d-44cd-6cac-2152597430f5-d7b2c481").text.strip()
    indica_sativa_ratio = soup.find('div', id='w-node-_7f69a302-9b3d-44cd-6cac-2152597430f9-d7b2c481').text.strip()

    # Extract project and strain descriptions.
    description_tags = soup.find_all('div', class_='metafield-rich_text_field')
    descriptions = [desc.text.strip() for desc in description_tags]
    description = " \n ".join(descriptions)

    # Limiteds, etc. do not have all fields, and thus some may not be present.
    duration_tag = soup.find('div', id='w-node-_7f69a302-9b3d-44cd-6cac-2152597430fd-d7b2c481')
    duration = duration_tag.text.strip() if duration_tag else 'duration not specified'

    height_tag = soup.find('div', class_='size-field')
    height = height_tag.text.strip() if height_tag else 'height not specified'

    yield_tag = soup.find('div', class_='yield-field')
    plant_yield = yield_tag.text.strip() if yield_tag else 'yield not specified'

    aroma_flavor_tag = soup.find('div', class_='aroma-flavour-field')
    aroma_flavor = aroma_flavor_tag.text.strip() if aroma_flavor_tag else 'aroma and flavor not specified'

    effect_tag = soup.find('div', class_='effect-field')
    effect = effect_tag.text.strip() if effect_tag else 'effect not specified'

    medicinal_effect_tag = soup.find('div', class_='medicinal-effect-field')
    medicinal_effect = medicinal_effect_tag.text.strip() if medicinal_effect_tag else 'medicinal effect not specified'

    return {
        'strain': strain,
        # 'price': price,
        'genetics': genetics,
        'seed type': seed_type,
        'indica/sativa ratio': indica_sativa_ratio,
        'duration': duration,
        'height': height,
        'yield': plant_yield,
        'aroma/flavor': aroma_flavor,
        'effect': effect,
        'medicinal effect': medicinal_effect,
        'description': description
    }


def scrape_mephistogenetics():
    base_url = 'https://mephistogenetics.com/collections/seeds'
    html = fetch_page(base_url)

    if html:
        soup = parse_html(html)
        product_links = extract_product_links(soup)

        for link in product_links:
            product_html = fetch_page(link)
            if product_html:
                product_soup = parse_html(product_html)
                product_data = extract_product_data(product_soup)
                print(product_data)


if __name__ == '__main__':
    scrape_mephistogenetics()
