@dataclass
class ProgramId:
    name: str
    description: str
    version: str = '1.0'
    date: str = 'n/a'

    def print(self, verbose: bool = False):
        _printstring = f'{self.name} ({self.version})'
        if verbose:
            _printstring = f'{_printstring}\n{self.description}\nDated: {self.date}'
        print(_printstring)

# program = ProgramId(
#     name ='verifyValidateDownloadPage',
#     description = 'Validates all links scraped from the designated page and outputs results to a specified _adoc_output file',
#     version = 2.0)