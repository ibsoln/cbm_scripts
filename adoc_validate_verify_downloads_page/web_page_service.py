'''dependencies'''
import requests
import validators

class web_page_class:
    url = ''
    is_valid = ''
    url_exists = ''
    response_content = ''
    html = ''
    http_status = ''
    diagnostic = ''

    def __init__(self):
        self.is_valid = False
        self.url_exists = False
        self.response_content = ''
        self.html = ''
        self.http_status = ''
        self.diagnostic = 'Initialized'
        print('Initialized')

    def get_endpoint(self, url):
        self.is_valid = self.validate_url(url)
        if self.is_valid:
            self.url = url
            return self.get(url)

    def validate_url(self, url=''):
        '''Validate url formation is correct'''
        return validators.url(url)

    def connect(self, url=''):
        '''Connect to endpoint and verify it exists'''
        pass

    def get(self, url=''):
        '''Retrieve html content from page'''
        result = False

        if self.is_valid:
            self.response_content = ''
            self.html = ''
            self.status = -1
            self.url_exists = False
            payload = {}
            headers = {
                # 'Authorization': 'Basic SWFuLmJyaWRnZTpDOUZpY2lubyE=',
                # 'Cookie': 'JSESSIONID=B2DB7C7E1C490CCE9F0E8F31311B374C; atlassian.xsrf.token=B2JT-82WI-PU49-SXVL_c193a72d25d965da3217d3ca0fac773b555a49f9_lin'
            }
            content = requests.request("GET", self.url, headers=headers, data=payload)
            self.status = content.status_code
            if self.status == 200:
                self.response_content = content
                self.html = self.response_content.text
                self.url_exists = True
            else:
                self.diagnostic = 'Error accessing endpoint'
        else:
            self.diagnostic = 'Invalid URL'
        return self.url_exists


def main(this_ws: web_page_class):
    ws = this_ws
    if ws.get_endpoint('https://www.bbc.co.uk/'):
        print(ws.response_content)


if __name__ == '__main__':
    print(f'Running {__name__}')
    main(web_page_service())
