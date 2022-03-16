import argparse
import os

class cli_arguments_class:

    cli_arguments = {}
    cli_numargs = -1

    def __init__(self):
        self.cli_numargs = 0
        self.cli_arguments = {}


    def add_args(self, args):

        parser = argparse.ArgumentParser()
        # parser.add_argument("-p", "--page", help="Define the page to be checked")
        # parser.add_argument("-o", "--out", help="Define the output file")

        for k, v in args.items():
            arg_string =  f"'{k}'"
            for k1, v1 in v.items():
                if k1 == 'flag':
                    this_arg = ''
                else:
                    this_arg = f'{k1} = '
                arg_string = f'{arg_string}, {this_arg} "{v1}"'
                print (arg_string)

            cli = f"parser.add_argument({arg_string})"
            print(cli)
            eval(cli)

        self.cli_arguments = vars(parser.parse_args())
        return self.cli_arguments


def main(this_cs: cli_arguments_class):
    cs = this_cs
    print(cs.cli_arguments.items())

if __name__ == '__main__':
    print(f'Running {__name__}')
    main(cli_arguments_service())