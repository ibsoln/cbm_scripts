
import cli_arguments_service as cs
import os

def main():
    # outfile = f"{os.getcwd()}/output/"

    our_args = {}

    arg_items = {
        "-o": {"flag": "--out", "default": f"{os.getcwd()}/output/", "help": "Defines the output file path" },
        "-o": {"flag": "--out", "default": f"{os.getcwd()}/output/", "help": "Defines the output file path"},
        "-o": {"flag": "--out", "default": f"{os.getcwd()}/output/", "help": "Defines the output file path"},
    }

    our_args = cs.cli_arguments_class()
    if our_args.add_args(arg_items):
        outfile = our_args.cli_arguments.get('out')
        print(f"Writing to {outfile}")


if __name__ == "__main__":
    print(f'Running {__name__}')
    main()


