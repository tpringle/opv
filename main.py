import toml
import requests
import click
import json
from lazyme.string import color_print

class loader(object):
    @staticmethod
    def load_toml(definition):
        """
        responsible for loading the checks.toml file used to guide this tool
        """
        with open(definition) as conffile:
            config = toml.loads(conffile.read())
            return config

class request(object):
    @staticmethod
    def get(url, apikey):
        headers = {
            'X-Octopus-ApiKey': apikey
        }
        r = requests.get(url, headers=headers)
        return r.json()


class parser(object):
    @staticmethod
    def parse(json, check):
        for k, v in check.items(): #For each of the checks in the toml file
            if type(v) == dict:
                for j in json['Items']:
                    for key, value in j[k].items():
                        if key in v:
                            if v.get(key) != value:
                                color_print('{0} is not configured correctly for {1}: expected {2} but found {3}'.format(j['Name'], k, v, value), color='red', underline=True, bold=True)


            elif type(v) == list:
                for j in json['Items']:
                    if set(v).issubset(set(j[k])) == False:
                        color_print('{0} is not configured correctly for {1}: expected {2} but found {3}'.format(j['Name'], k, v, j[k]), color='red', underline=True, bold=True)

            else:
                for j in json['Items']:
                    if v != j[k]:
                        color_print('{0} is not configured correctly for {1}: expected {2} but found {3}'.format(j['Name'],k, v, j[k]), color='red', underline=True, bold=True)




@click.command()
@click.option('--apikey', required=True, help='API Key for Octopus Deploy')
def main(apikey):
    main_data = loader.load_toml("checks.toml")
    color_print('Checking the following configurations: {0}'.format(main_data['checks']), color='green', underline=True, bold=True)


    # Initial query
    req = request.get(main_data['server']['url'] + "/api/projects", apikey)
    parser.parse(req, main_data['checks'])

    # If more pages exist
    while req.get('Links', {}).get('Page.Next') != None:
        req = request.get(main_data['server']['url'] + req['Links']['Page.Next'], apikey)
        parser.parse(req, main_data['checks'])

if __name__ == "__main__":
    main()
