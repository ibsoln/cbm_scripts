# adoc_validate_xrefs.py

# Objective = Identify any malformed or unresolved asciidoc XREFs remaining in the published HTML site
#  Runs against a local copy of the website either 'local' or 'staged'



# import validators
import glob
import os
import pathlib
import re
import urllib.error
import urllib.request
import urllib.response
from genericpath import isfile


# import urllib3

def get_data(argFile):
  f = open(argFile)
  text = f.read()
  f.close()
  return text



def is_ValidUrl (argURL):
  result = (False,"Invlaid URL")
  # if validators.url(argURL):
    #  Only process 'valid' url
  try:
    conn = urllib.request.urlopen(argURL)
  except urllib.request.HTTPError as e:
    #  404 etc
    print(f'{e}')
    result = (False,e.code)
  except urllib.error as e:
    #  non http network type error (conn refused?
    print(f'{e}')
    result = (False,e.code)
  else:
    #  200-OK
    result = (True,"")
  # return result


def main():

  outDir = f"{os.getcwd()}/output/"
  processing_list = []
  valid_processes = ['cbl','sgw','tutorials']

  # Point at local build site

  roots = { "stage300":"/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/stage/stage300/",
              "staging":"https://docs-staging.couchbase.com/",
            "local":"/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/local"}

  rootDirs = { "sgw":"sync-gateway/current/**",
              "cbl":"couchbase-lite/current/**",
              "tutorials":"tutorials/**"}

  outfiles = {"sgw": "adoc_diag_bad_xrefs_sgw.csv",
              "cbl": "adoc_diag_bad_xrefs_cbl.csv",
              "tutorial":"adoc_diag_bad_xrefs_tutorials.csv"}

  # url_roots = ['http://localhost:5000/sync-gateway/current/',
  #             'https://ibsoln.github.io/stage/stage300/couchbase-lite/current/']
  # url_roots = ['https://ibsoln.github.io/stage/3.0-GA/sync-gateway/current/',
  #             'https://ibsoln.github.io/stage/3.0-GA/couchbase-lite/current/']
  url_roots = ['https://docs-staging.couchbase.com/sync-gateway/current/',
              'https://docs-staging.couchbase.com/couchbase-lite/current/']

  # outfilename = outDir + 'adoc_diag_bad_xrefs.csv'
  # outfilename = outDir + 'href_tags_sgw.csv'
  # url_root = 'https://ibsoln.github.io/stage/stage300/sync-gateway/current/'
  # url_root = 'https://ibsoln.github.io/stage/stage300/couchbase-lite/current/'
  newline = '\n'
  search_pattern_Xrefs = '((.*xref.*)|(.*url-.*)|(.*http.*pfx.*)|(.*http.*adoc.*))'
  # search_pattern_Xrefs = '{((.*xref.*)|(.*url-.*)|(.*pfx.*)|(.*adoc.*))}'
  search_pattern_In_Braces = '{(.+?)}'
  search_pattern_Html_Hrefs = '(?:href=)(".*")'


  for i in range(len(rootDirs)):
    # outfilename = getOutputFile( argName=outfiles[i], argPath=outDir )
    x=outfiles[valid_processes(i)]
    outfilename = f'{outDir}{x}'
    root_dir = rootDirs[i]
    # url_root = url_roots[i]
    cnt_processed = 0
    cnt_errors = 0
    print(f'Processing {root_dir}')
    with open(outfilename,'w') as of:
      # thisDir = os.path.dirname(os.path.realpath(__file__))
      of.write(f'string, file {newline}')
      fileList = glob.glob(root_dir,recursive=True)
      for fname in fileList:
        if isfile(fname):
          if 'htm' in pathlib.Path(fname).suffix:
            # Process any html files
            cnt_processed +=1
            search_text = get_data(fname)
            for match in re.finditer(search_pattern_Xrefs,search_text):
              cnt_errors +=1
              report_line = f'{search_text[match.start():match.end()]}, {fname}{newline}'
              of.write(report_line)
      of.write(f'{cnt_processed},{cnt_errors}{newline}')
      of.close()

      print(f'Validated and verified {cnt_processed} url; rejected {cnt_errors}')


if __name__ == "__main__":
    main()


