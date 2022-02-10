# adoc_validate_verify_downloads_page.py

# Objective = Identify any embedded HREFS onthe specified page that do not point to functioning endpoints
#
# Runs against the live/staged website


# from genericpath import isfile
import re
import os
from pathlib import Path
import validators
import glob
import requests
import web_page_service as ws
# import mypackages.web_page_service as ws
    # import web_page_class as wc
from urllib import error
from urllib import request
from urllib import response
# import urllib3


def get_data(argFile):
    f = open(argFile)
    text = f.read()
    f.close()
    return text


def is_ValidUrl(argURL):
    msg = ""
    result = False
    if validators.url(argURL):
        conn = requests.get(argURL, timeout=5)
        # conn.time
        msg = msg + str(conn.status_code)
        result = conn.status_code == 200
    else:
        msg = "Invalid URL"
    return (result, msg)


def validate_hrefs_on_page(html_to_check,
                           outfilename,
                           exceptions_only):
    newline = '\n'
    search_pattern_Html_Hrefs = '(?:href=)(".*")'
    working_url = 0
    non_working_url = 0
    # fname = '/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/local/couchbase-lite/3.0/c/gs-downloads.html'

    with open(outfilename, 'w') as of:
        print(f"Writing to {of.name}")
        of.write(f'URL, filepath, filename,message{newline}')

        search_text = html_to_check
        for match in re.finditer(search_pattern_Html_Hrefs, search_text):

            this_url = search_text[match.start():match.end()].split('"')[1]
            msg = ''

            if ".adoc" in this_url:
                # Trap any Asiidoc/Antora malformed URI
                non_working_url += 1
                msg = "Antora - Malformed"
            else:
                # Compile the formed url to test
                if ('packages' in this_url):
                    (result, msg) = is_ValidUrl(this_url)
                    if result:
                        working_url += 1
                        if exceptions_only:
                            msg=''
                    else:
                        non_working_url += 1
            if msg:
                of.write(f'{this_url},{msg}{newline}')

        print(f'Validated {page_to_check} \n and verified {working_url} url; rejected {non_working_url}')


if __name__ == "__main__":
    # page_to_check = 'https://docs-staging.couchbase.com/couchbase-lite/current/c/gs-downloads.html'
    page_to_check = 'https://docs.couchbase.com/couchbase-lite/3.0/c/gs-downloads.html'
    outfilename = f"./adoc_diag_href_tags_cbl.csv"
    # Report only failing URLS
    exceptions_only = True
    # Report result of all checks
    # exceptions_only = False

    this_ws = ws.web_page_class()

    if this_ws.get_endpoint(page_to_check):
        validate_hrefs_on_page(this_ws.html,
                               outfilename,
                               exceptions_only)


