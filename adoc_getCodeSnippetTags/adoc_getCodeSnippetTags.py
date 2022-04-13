# roughscript

inDir = "./"
inFile = "_param-tags_code-search.txt"
outDir = "./"
outFile = "listOfCodeSnippetTags.csv"
mylines = ()
thisfile = None
with open (f"{inDir}{inFile}", "r") as infile:
    mylines = infile.readlines()
    with open(f"{outDir}{outFile}","w") as outfile:
        outfile.write('tag,file,line,module,page\n')
        for line in mylines:
            if line.startswith("cbl"):
                thisfile = line.split(" • ")[1].replace('\n','')
                thisfilebits = thisfile.split("/")
                thispage = thisfilebits[len(thisfilebits)-1]
                thismodule = thisfilebits[1]
            if not thisfile is None:
                if ":param-tags:" in line:
                    taglineparts=line.split(" ")
                    if len(taglineparts)<6:
                        thisline=taglineparts[2].replace(':','')
                        thistag=taglineparts[4].replace('\n','')
                        print(f"{thistag},{thisfile},{thisline},{thismodule},{thispage}")
                        outfile.write(f"{thistag},{thisfile},{thisline},{thismodule},{thispage}\n")
