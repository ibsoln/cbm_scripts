program = { 'name': 'getApiDataModels', 'version' : '1.0', 'date' : '5/04/2022', \
            'description': 'Return selected properties from a YAML Swagger UI Api spec'}

import os
import yaml as YAML
from yaml.loader import SafeLoader as LOADER



def getConfigData(config_type):
    with open('_adoc_yaml_parser_config.yaml', 'r') as f:
        config = YAML.load(f, Loader=LOADER)
        return config[config_type]

def getPyYamlSettings():
    # Return parameter values
    settings = getConfigData('pyyaml_settings')
    return settings['encoding'], settings['default_flow_style'], settings['sort_keys']

def getParameters():
    # Return parameter values
    params = getConfigData('params')
    inFile = params['inFile']
    if not inFile.endswith('.yaml') and not inFile.endswith('.yml'):
        inFile = f'{inFile}.yaml'
    os.makedirs(os.path.dirname(params['outDir']), exist_ok=True)
    return params['inDir'], params['outDir'], inFile, params['selectors']


def getData(dir, file):
    with open( f'{dir}{file}', 'r') as f:
        try:
            data = YAML.load(f, Loader=LOADER)
        except YAML.YAMLError as exc:
            print(f'Error in configuration file: {exc}')
    return data['definitions']


def main():

    encoding, \
    default_flow_style, \
    sort_keys = getPyYamlSettings()

    inDir, \
    outDir, \
    inFile, \
    selectors, = getParameters()

    if selectors:
        definitions = getData(inDir, inFile)
        for s in selectors:
            # Expand any $ref definitions
            for key, value in definitions[s]['properties'].items():
                if '$ref' in value:
                    d = value['$ref'].split('definitions/', 1)[1]
                    definitions[s]['properties'][key] = definitions[d]
            # Write the sg-yaml file
            with open(f'{outDir}sg-{s}.yaml', 'w') as of:
                print(f'Generating {s}')
                YAML.dump(definitions[s], of, sort_keys=sort_keys, default_flow_style=default_flow_style, encoding=encoding)
    else:
        print('No _adoc_output objects selected')


if __name__ == '__main__':
    print(program)
    main()