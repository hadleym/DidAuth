import requests
import sys

CONFIG = '/home/mark/projects/login/config.txt'

def main(did):
    print(str(did))
    print('Access Granted')


def resolve(did):
    resolver = ClientWebResolver(CONFIG)
    try:
        result = resolver.resolve(did)
        return result
    except TypeError:
        return None


def authenticate(did):
    return True


class ClientWebResolver:

    def __init__(self, config):
        self.CONFIG = config

    def resolve(self, did):
        configFile = open(self.CONFIG, 'r')
        lines = configFile.readlines()

        try:
            for line in lines:
                if not line.endswith('/'):
                    line += '/'
                url = line + did
                httpResponse = requests.get(url)
                if httpResponse.status_code is 200:
                    return httpResponse.json()
            raise TypeError
        except TypeError:
            print("All web services tested. Please add a working web resolver to the config file and try again.")

    def modifier(self, did):
        pass


if __name__ == '__main__':
    main(sys.argv[1])
