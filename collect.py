import redis
import fileinput
import requests
import argparse
import os
import settings
from StringIO import StringIO

class UnistoreClient(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def _upload_file(self, type_id, file_name, content):
        response = requests.post(self.url,
                                 data={'type_id': type_id},
                                 files={'file': (file_name, content)},
                                 headers={'Token': self.token})
        return response.status_code == 200 and response.json['id'] or None

    def _memorize(self, url, id):
        return self.redis.set(url, id)

    def put_file(self, url, type_id, file_name, content):
        id = self._upload_file(type_id, file_name, content)
        return id and self._memorize(url, id) or False


def main():
    parser = argparse.ArgumentParser(prog=__file__)
    parser.add_argument('token', help='Unistore access token')
    parser.add_argument('url_list', help='File that contains URLs (one URL per line)')
    args = parser.parse_args()

    unistore = UnistoreClient(settings.UNISTORE_URL, args.token)

    for line in fileinput.input(args.url_list):
        url = line.strip()	
        print url,
        
        try:
            response = requests.get(url)
            print '.'

            if response.status_code == 200:
                type_id = os.path.basename(args.url_list)
                file_name = url.rsplit('/', 1)[1]
                succeed = unistore.put_file(url, type_id, file_name, response.content)
                print (succeed and 'OK' or 'F')
            else:
                print 'E'
        except:
            print 'E!'


if __name__ == '__main__':
    main()