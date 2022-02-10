# adoc_validate_hrefs_on_page.py

# Objective = Identify any embedded HREFS onthe specified page that do not point to functioning endpoints
#
# Runs against the live/staged website



import re
import os
import shutil

import time, glob

packages = ["ktx", "java", "jvm"]

packageroot = "/snippets/app/src/main/"
ktx_sfx="kotlin/com/couchbase/code_snippets/*.kt"
java_sfx="java/com/couchbase/code_snippets/*.java"
jvm_sfx="/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/java/examples/snippets/src/main/java/com/couchbase/code_snippets/*.java"

packages_names = {
  "ktx":"/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/android/examples/snippets/app/src/main/kotlin/com/couchbase/code_snippets/*.kt",
  "java":"/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/android/examples/snippets/app/src/main/java/com/couchbase/code_snippets/*.java",
  "jvm":"/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/java/examples/snippets/src/main/java/com/couchbase/code_snippets/*.java"
}

outfilenames = {
  "ktx": "/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/android/examples/codesnippet_collection.kt",
  "java": "/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/android/examples/codesnippet_collection.java",
  "jvm": '/Users/ianbridge/CouchbaseDocs/bau/cbl/modules/java/examples/codesnippet_collection.java'
}

for package in packages:
  print(package)
  filenames = glob.glob(packages_names[package])
  with open(outfilenames[package], 'w') as outfile:
      print(f"Writing to {outfile.name}")
      # for filename in glob.glob('*.txt'):
      for filename in filenames:
          if filename == outfilenames[package]:
              # don't want to copy the output into the output
              continue
          outfile.write(f"\n\n// MODULE_BEGIN --{filename} \n")
          with open(filename, 'r') as readfile:
              print(f"Including {filename}\n")
              outfile.write(readfile.read() + "\n\n")
              outfile.write(f"\n// MODULE_END --{filename} \n\n")
              # shutil.copyfileobj(readfile, outfile)






