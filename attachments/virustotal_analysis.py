import requests

class singleton(object):
    def __init__(self, cls):
        self.cls = cls
        self.obj = None

    def __call__(self, *args, **kwargs):
        if self.obj is None: self.obj = self.cls(*args, **kwargs)
        return self.obj


@singleton
class blank_common(object):
    def __init__(self):
        self.const1 = 100
        self.const2 = 200

@singleton
class vt_singleton():

    @property
    def api_key(self):
        return self._api_key

    def __init__(self, api_key):
        self._api_key = api_key

    def scan(self, file_path):
        """
        Send file to virustotal

        :param file_path:
        :return: resource

        response example:
        {
          'permalink': 'https://www.virustotal.com/file/d140c...244ef892e5/analysis/1359112395/',
          'resource': u'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556',
          'response_code': 1,
          'scan_id': 'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556-1359112395',
          'verbose_msg': 'Scan request successfully queued, come back later for the report',
          'sha256': 'd140c244ef892e59c7f68bd0c6f74bb711032563e2a12fa9dda5b760daecd556'
        }

        """
        params = {'apikey': self.api_key}
        files = {'file': ('myfile.exe', open('myfile.exe', 'rb'))}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan',
                                 files=files, params=params)
        json_response = response.json()
        return json_response


    pass

