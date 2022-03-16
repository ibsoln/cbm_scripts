# adoc_validate_verify_downloads_page.py

# Objective = Identify any embedded HREFS onthe specified page that do not point to functioning endpoints
#
# Runs against the live/staged website

import re
import requests
import validators.url
import web_page_service as ws
import argparse

program_name = "verifyValidateDownloadPage"
program_version = 2.0
program_description = 'Validates all links scraped from the designated page and outputs results to a specified output file'

# Command Line Parameters are as shown in 'get_args()' below

def get_args():

    # Set default values
    arg_page = 'https://docs-staging.couchbase.com/couchbase-lite/current/c/gs-downloads.html'
    arg_page = 'https://docs-staging.couchbase.com/couchbase-lite/current/c/gs-downloads.html'
    arg_out = f"./output/adoc_diag_href_tags_cbl.csv"
    arg_except = False

    parser = argparse.ArgumentParser()
    # BEGIN - COMMAND LINE PARAMETERS
    parser.add_argument("-p", "--page", help="Define the page to be checked")
    parser.add_argument("-o", "--out", help="Define the output file")
    parser.add_argument("-e", "--exceptions", help="Report only on exceptions")
    # END - COMMAND LINE PARAMETERS
    args = parser.parse_args()

    if args.page:
        arg_page = args.page
    if args.out:
        arg_out = args.out
    if args.exceptions:
        arg_except = args.exceptions
    return (arg_page, arg_out, arg_except)


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


def validate_hrefs_on_page(page_to_check,
                           html_to_check,
                           outfilename,
                           exceptions_only):
    newline = '\n'
    search_pattern_Html_Hrefs = '(?:href=)(".*")'
    working_url = 0
    non_working_url = 0
    expected_errors = 0
    known_errors = [
        'https://www.linkedin.com/company/couchbase',
        'https://support.couchbase.com',
        'https://blog.couchbase.com',
        'https://blog.couchbase.com/category/couchbase-mobile/?ref=blog-menu'
    ]

    with open(outfilename, 'w') as of:
        print(f"Writing to {of.name}")
        print(f"Processing {page_to_check}")
        if exceptions_only:
            print('Reporting only exceptions')

        of.write(f'URL, filepath, filename,message{newline}')

        search_text = html_to_check
        for match in re.finditer(search_pattern_Html_Hrefs, search_text):

            this_url = search_text[match.start():match.end()].split('"')[1]
            msg = ''

            if ".adoc" in this_url:
                # Trap any Asiidoc/Antora malformed URI
                if ('/edit/' in this_url):
                    #  Ignore the 'Edit on Github' links for this purpose
                    expected_errors += 1
                else:
                    non_working_url += 1
                    msg = "Antora - Malformed"
            else:
                # Compile the formed url to test
                if ('packages' in this_url) or ('http' in this_url):
                    (result, msg) = is_ValidUrl(this_url)
                    if result:
                        working_url += 1
                        if exceptions_only:
                            msg=''
                    else:
                        if this_url in known_errors:
                            # Accept that some domains reject crawler pings with 403 (eg Couchbase)
                            msg=''
                            expected_errors += 1
                        else:
                            non_working_url += 1
            if msg:
                of.write(f'{this_url},{msg}{newline}')

        print(f'Validated and verified {working_url} url; rejected {non_working_url}; expected {expected_errors}')



def main( ):

    (page_to_check, outfilename, exceptions_only) = get_args()


    known_errors = [
        'https://support.couchbase.com',
        'https://blog.couchbase.com',
        'https://www.linkedin.com/company/couchbase'
    ]

    #
    # END CONFIG

    # print(f'Processing - {page_to_check}\n Writing - {outfilename}\n Exceptions-only - {exceptions_only}')

    # Initialize web service class
    this_ws = ws.web_page_class()
    # Check URL exists and scrape the HTML to valiadate_hrefs_on_page for checking
    if this_ws.get_endpoint(page_to_check):
        validate_hrefs_on_page(page_to_check,
                               this_ws.html,
                               outfilename,
                               exceptions_only)



if __name__ == "__main__":
    print(f'Running {program_name} version {program_version}')
    main()


