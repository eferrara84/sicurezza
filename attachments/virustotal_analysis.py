from time import sleep, time

import requests
import pprint
import progressbar

class singleton(object):
    def __init__(self, cls):
        self.cls = cls
        self.obj = None

    def __call__(self, *args, **kwargs):
        if self.obj is None: self.obj = self.cls(*args, **kwargs)
        return self.obj


@singleton
class vt_singleton():

    @property
    def api_key(self):
        return self._api_key

    def __init__(self, api_key=None):
        if api_key is None:
            self._api_key = '3981c576e8b31f88f700ea8dcf912a39bb778aa32063e78c198fd4a376d258f9'
        else:
            self._api_key= api_key

    def scan(self, file_path):
        """
        Send file to virustotal

        :param file_path:
        :return: resource_id needed to see virus total report

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
        params = {'apikey': self._api_key}
        files = {'file': (file_path, open(file_path, 'rb'))}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan',
                                 files=files, params=params)
        json_response = response.json()
        return json_response['resource']

    def get_repoort(self,res):
        """

        :param res: resource id
        :return: report

        example response:
        {
          'response_code': 1,
          'verbose_msg': 'Scan finished, scan information embedded in this object',
          'scan_id': '1db0ad7dbcec0676710ea0eaacd35d5e471d3e11944d53bcbd31f0cbd11bce31-1390467782',
          'permalink': 'https://www.virustotal.com/url/__urlsha256__/analysis/1390467782/',
          'url': 'http://www.virustotal.com/',
          'scan_date': '2014-01-23 09:03:02',
          'filescan_id': None,
          'positives': 0,
          'total': 51,
          'scans': {
              'CLEAN MX': {'detected': False, 'result': 'clean site'},
              'MalwarePatrol': {'detected': False, 'result': 'clean site'}
              [... continues ...]
            }
        }
        """
        params = {'apikey': self._api_key,
                  'resource': res}
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "python"
        }
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
                                params=params, headers=headers)
        json_response = response.json()
        return json_response

if __name__ == '__main__':

    vt = vt_singleton()

    file = './attachments_files/Schermata 2017-07-31 alle 12.46.29.jpg'

    f_resource = vt.scan(file_path=file)
    # print f_resource
    # print 'ee551491bf660b85eca8925bc52457a3e1915ba127d2392222fccd93eb67a87a'
    bar = progressbar.ProgressBar()

    for i in bar(range(100)):
        sleep(0.3)
        bar.update(i)
    try:
        report = vt.get_repoort(res=f_resource)
        pprint.pprint(report)
        if report['response_code'] == -2:
            raise Exception
    except Exception:
        print "Requested resource is not among the finished"
        print "Trying to request the report again"
        for i in bar(range(100)):
            sleep(0.015)
            bar.update(i)
        report = vt.get_repoort(res=f_resource)
        pprint.pprint(report)


