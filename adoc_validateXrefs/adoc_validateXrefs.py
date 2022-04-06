program = { 'name': 'adoc_validateXrefs', 'version' : '3.0', 'date' : '',
            'description': 'Return selected properties from a YAML Swagger UI Api spec'}

# Objective = Identify any malformed or unresolved asciidoc XREFs remaining in the published HTML site
# Runs against a local copy of the website either 'local' or 'staged'

import glob
import os
import pathlib
import re
from genericpath import isfile
from class_cli_args import cli_arguments_service as cs

newline = '\n'

def get_data(argFile):
    # Return file contents as text
    
    f = open(argFile)
    text = f.read()
    f.close()
    return text


def  get_arguements(cwd):
    # Get the command line arguments and return to main() in usable form
    
    actual_processes = ['cbl', 'sgw', 'tutorials']
    valid_processes = actual_processes.copy()
    valid_processes.append('all')
    valid_targets = ['local', 'stage']

    arg_items = {
      "-o": {"flag": "--out", "default": f"{cwd}", "help": "Defines the _adoc_output file path"},
      "-p": {"flag": "--process", "default": "all",
             "help": "Defines components to be processed (sgw/cbl/tutorials/all)", "choices": valid_processes},
      "-b": {"flag": "--build", "default": "local", "help": "Select the target build site to check (ibsoln/staging)",
             "choices": valid_targets},
    }
    
    our_args = cs.cli_arguments_class()
    if our_args.add_args(arg_items):
      this_outDir = our_args.cli_arguments.get('out')
      this_process = our_args.cli_arguments.get('process')
      if this_process == 'all':
        this_process_list = actual_processes
      else:
        this_process_list = [this_process]

      this_build_site = our_args.cli_arguments.get('build')

      return this_build_site, this_process_list, this_outDir
    else:
      return  0,0,0


def main():

    cwd = os.getcwd()
    # Folder holding antora site
    roots = {"local": f"{cwd}/local/",
             "stage": f"{cwd}/stage/"}

    # Product components to include
    rootDirs = {"sgw": "sync-gateway/current/**",
                "cbl": "couchbase-lite/current/**",
                "tutorials": "tutorials/**"}

    # _adoc_output file names per component
    outfiles = {"sgw": "_adoc_diag_bad_xrefs_sgw.csv",
                "cbl": "_adoc_diag_bad_xrefs_cbl.csv",
                "tutorial": "_adoc_diag_bad_xrefs_tutorials.csv"}

    (build_site, process_list, outDir) = get_arguements(cwd)
    if not build_site:
      exit(999)

    print(f"Targetting {build_site}{newline}Processing {len(process_list)} components{newline}Writing to {outDir}")

    # regex used to discover malformed xrefs
    search_pattern_Xrefs = '((.*xref.*)|(.*url-.*)|(.*http.*pfx.*)|(.*http.*adoc.*))'

    # alternates
    # search_pattern_Xrefs = '{((.*xref.*)|(.*url-.*)|(.*pfx.*)|(.*adoc.*))}'
    # search_pattern_In_Braces = '{(.+?)}'
    # search_pattern_Html_Hrefs = '(?:href=)(".*")'

    # for each selected component
    for i in process_list:
        outfilename = f"{outDir}/{outfiles.get(i)}"
        root_dir = f"{roots.get(build_site)}{rootDirs[i]}"
        cnt_processed = 0
        cnt_errors = 0
        print(f'Processing {root_dir}')
        with open(outfilename, 'w') as of:
            of.write(f'string, file {newline}')
            fileList = glob.glob(root_dir, recursive=True)
            # For each file in folder path
            for fname in fileList:
                if isfile(fname):
                    if 'htm' in pathlib.Path(fname).suffix:
                        # Process any html files
                        cnt_processed += 1
                        search_text = get_data(fname)
                        for match in re.finditer(search_pattern_Xrefs, search_text):
                            cnt_errors += 1
                            report_line = f'{search_text[match.start():match.end()]}, {fname}{newline}'
                            of.write(report_line)
            of.write(f'{cnt_processed},{cnt_errors}{newline}')
            of.close()

            print(f'Validated and verified {cnt_processed} url; rejected {cnt_errors}')


if __name__ == "__main__":
    print(f'Running {program}')
    main()
