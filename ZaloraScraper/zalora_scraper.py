import json
import pprint

import requests


class ZaloraScraper:
    headers = {
        'authority': 'www.zalora.com.my',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
    }

    def __init__(self):
        super().__init__()
        self.offset = 0  # TODO : It is starting offset it would be 0 here
        self.limit = 102  # TODO : You can directly write total number here if you know the total number of products.
        self.category_id = 4  # TODO : category_id of the data you want to scrape
        self.occasion = 'Casual'  # TODO : occasion of your products
        self.brand = 87  # TODO : brand id would needs to written, you can get easily from inspect element,e.g. ALDO:87
        self.gender = 'women'  # TODO : gender for which you want to scrape data
        self.base_url = "https://www.zalora.com.my/"

        self.data_api_url = "https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc" \
                            "&offset={offset}&limit={limit}&category_id={category_id}&occasion={occasion}&brand={brand}&gender={gender}"
        self.items_list = []
        self.output_file_name = 'outputs/output.json'
        self.start_process()

    def start_process(self):
        data_api_url = self.data_api_url.format(offset=self.offset, limit=self.limit, category_id=self.category_id,
                                                occasion=self.occasion, brand=self.brand, gender=self.gender)
        response = self.do_request(url=data_api_url)
        self.process_pagination(response)

    def process_pagination(self, response):
        json_data = json.loads(response.text)
        total_records_count = json_data.get('response', {}).get('numFound', 0)

        data_api_url = self.data_api_url.format(offset=self.offset, limit=total_records_count,
                                                category_id=self.category_id, occasion=self.occasion,
                                                brand=self.brand, gender=self.gender)

        response = self.do_request(url=data_api_url)
        self.parse_response_data(response)

    def parse_response_data(self, response):
        json_data = json.loads(response.text)

        item = dict()
        for product in json_data.get('response', {}).get('docs', []):
            item['SKU'] = product['meta']['sku']
            item['Brand'] = product['meta']['brand']
            item['Product Name'] = product['meta']['name']
            item['Actual price'] = product['meta']['price']
            item['Discounted price'] = product['meta']['special_price'] or product['meta']['price']
            item['Image URL'] = product['image']

            self.items_list.append(item)

            pprint.pprint(item)

        self.process_output_file()

    def do_request(self, url, method='GET'):
        print('processing request to url = {}'.format(url))
        response = requests.request(method=method, url=url, headers=self.headers)

        if not response.status_code == 200:
            self.do_request(url=url, method=method)

        else:
            return response

    def process_output_file(self):
        with open(self.output_file_name, mode='w', encoding='utf-8', newline='') as output_file:
            print("saving data into {}".format(self.output_file_name))
            output_file.writelines(json.dumps(self.items_list))


if __name__ == '__main__':
    obj = ZaloraScraper()
    print(obj.items_list)
