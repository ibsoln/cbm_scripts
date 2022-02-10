# adoc_validate_xrefs.py

# Objective = Identify any malformed or unresolved asciidoc XREFs remaining in the published HTML site
#  Runs against a local copy of the website either 'local' or 'staged'



from genericpath import isdir, isfile
from posixpath import basename
import re
import os
import pathlib
import shutil
# import validators
import time
import glob
import urllib.error
import urllib.request
import urllib.response
# import urllib3
from lib import getOutputFile

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

  outDir = f"{os.getcwd()}/data/badXrefs/"

  # Point at local stage site
  # rootDirs = ["/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/stage/stage280/sync-gateway/current/**",
  #             "/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/stage/stage280/couchbase-lite/current/**"]

  # rootDirs = ["/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/stage/stage300/sync-gateway/current/**",
  #             "/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/stage/stage300/couchbase-lite/current/**"]

  # Point at local build site
  rootDirs = ["/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/local/sync-gateway/current/**",
              "/Users/ianbridge/CouchbaseDocs/ibsoln.github.io/local/couchbase-lite/current/**"]

  outfiles = ['adoc_diag_bad_xrefs_sgw.csv',
              'adoc_diag_bad_xrefs_cbl.csv']

  # url_roots = ['http://localhost:5000/sync-gateway/current/',
  #             'https://ibsoln.github.io/stage/stage300/couchbase-lite/current/']
  url_roots = ['https://ibsoln.github.io/stage/stage300/sync-gateway/current/',
              'https://ibsoln.github.io/stage/stage300/couchbase-lite/current/']
  # url_roots = ['https://ibsoln.github.io/stage/stage280/sync-gateway/current/',
  #             'https://ibsoln.github.io/stage/stage280/couchbase-lite/current/']

  # outfilename = outDir + 'adoc_diag_bad_xrefs.csv'
  # outfilename = outDir + 'href_tags_sgw.csv'
  # url_root = 'https://ibsoln.github.io/stage/stage300/sync-gateway/current/'
  # url_root = 'https://ibsoln.github.io/stage/stage300/couchbase-lite/current/'
  newline = '\n'
  search_pattern_Xrefs = '((.*xref.*)|(.*url-.*)|(.*http.*pfx.*)|(.*http.*adoc.*))'
  # search_pattern_Xrefs = '{((.*xref.*)|(.*url-.*)|(.*pfx.*)|(.*adoc.*))}'
  search_pattern_In_Braces = '{(.+?)}'
  search_pattern_Html_Hrefs = '(?:href=)(".*")'


  for i in range(2):
    # outfilename = getOutputFile( argName=outfiles[i], argPath=outDir )
    outfilename = outDir+outfiles[i]
    rootDir = rootDirs[i]
    url_root = url_roots[i]
    cnt_processed = 0
    cnt_errors = 0
    print(f'Processing {outfilename}')
    with open(outfilename,'w') as of:
      # thisDir = os.path.dirname(os.path.realpath(__file__))
      of.write(f'string, file {newline}')
      fileList = glob.glob(rootDir,recursive=True)
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


