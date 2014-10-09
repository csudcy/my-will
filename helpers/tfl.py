import random
import re
import xml.etree.ElementTree as ET

from memoize import Memoizer
import requests


LINE_STATUS_URL = "http://cloud.tfl.gov.uk/TrackerNet/LineStatus"

store = {}
memo = Memoizer(store)

class TFL(object):
    def __init__(self):
        self.url =LINE_STATUS_URL

    @memo(max_age=60)
    def get_all_line_statuses(self):
        """
        Fetch the list of linee statuses from tfl
        """
        headers = {'Content-type': 'application/xml', 'Accept': 'application/xml'}
        response = requests.get(self.url, headers=headers)
        # do some encoding to make sure we get it in the correct format
        response.encoding ='utf-8'
        xml = response.text
        xml_test = xml.encode('utf-8')
        root = ET.fromstring(xml_test)

        # Now go and work out the line statuses
        train_status = {}
        for line in root:
            line_name = None
            line_status = None
            for line_info in line:
                name = re.sub('{.*?}', '', line_info.tag)
                if name == 'Line':
                    line_name = line_info.attrib['Name']
                elif name == 'Status':
                    line_status = line_info.attrib['Description']

            train_status[line_name.lower()] = line_status

        return train_status

    def get_line_status(self, line):
        """
        Find line status based on the given search string
        """
        line_statuses = self.get_all_line_statuses()

        if line.lower() in line_statuses:
            return 'The {0} line currently has {1}'.format(line, line_statuses[line.lower()])
        else:
            key = random.choice(line_statuses.keys())
            return 'I don\'t know the {0} line so I\'ve picked on at random for you. Your line is the {1} line and it currently has {2}'.format(
                line,
                key,
                line_statuses[key]
            )

if __name__ == '__main__':
    tfl = TFL()
    print tfl.get_all_line_statuses()
    print tfl.get_line_status('Bakerloo')
    print tfl.get_line_status('Bakerpoo')

