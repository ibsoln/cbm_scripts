program = { 'name': 'adoc_collateJavaKotlinSnippets',
            'version' : '1.0',
            'date' : '',
            'description': 'Concatenate the module files used to hold java and kotlin snippets'}

import glob
import os

cwd = os.getcwd()
jwd = cwd.replace('android', 'java')

packages = ["ktx", "java", "jvm"]

packageroot = "/snippets/app/src/main/"
ktx_sfx="kotlin/com/couchbase/code_snippets/*.kt"
java_sfx="java/com/couchbase/code_snippets/*.java"
jvm_sfx=f"{jwd}/snippets/src/main/java/com/couchbase/code_snippets/*.java"



packages_names = {
  "ktx":f"{cwd}/snippets/app/src/main/kotlin/com/couchbase/code_snippets/*.kt",
  "java":f"{cwd}/snippets/app/src/main/java/com/couchbase/code_snippets/*.java",
  "jvm":f"{jwd}/snippets/src/main/java/com/couchbase/code_snippets/*.java"
}

outfilenames = {
  "ktx": f"{cwd}/codesnippet_collection.kt",
  "java": f"{cwd}/codesnippet_collection.java",
  "jvm": f"{jwd}/codesnippet_collection.java"
}

def main():
    print(f'Working in: {cwd}')
    for package in packages:
      print(package)
      filenames = glob.glob(packages_names[package])
      with open(outfilenames[package], 'w') as outfile:
          print(f"Writing to {outfile.name}")
          # for filename in glob.glob('*.txt'):
          for filename in filenames:
              if filename == outfilenames[package]:
                  # don't want to copy the _adoc_output into the _adoc_output
                  continue
              outfile.write(f"\n\n// MODULE_BEGIN --{filename} \n")
              with open(filename, 'r') as readfile:
                  print(f"Including {filename}\n")
                  outfile.write(readfile.read() + "\n\n")
                  outfile.write(f"\n// MODULE_END --{filename} \n\n")
                  # shutil.copyfileobj(readfile, outfile)



if __name__ == "__main__":
    print(f'Running {program}')
    main()




