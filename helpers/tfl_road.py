import re
import xml.etree.ElementTree as ET

from memoize import Memoizer
import requests

ROAD_STATUS_URL = "http://data.tfl.gov.uk/tfl/syndication/feeds/tims_feed.xml?app_id=58e00a11&app_key=8f440c979ea6f75fd0e4a6ade1832758"


store = {}
memo = Memoizer(store)

class TFLROAD(object):
    def __init__(self):
        self.url = ROAD_STATUS_URL

    @memo(max_age=300)
    def get_road_statuses(self):
        """
        Fetch the list of road statuses from tfl
        """
        headers = {'Content-type': 'application/xml', 'Accept': 'application/xml'}
        response = requests.get(self.url, headers=headers)
        # do some encoding to make sure we get it in the correct format
        response.encoding ='utf-8'
        xml = response.text
        xml_test = xml.encode('utf-8')
        root = ET.fromstring(xml_test)

        road_status = {}

        for disruption in root[1]:
            road_name = None
            description = None
            for disruption_info in disruption:
                name = re.sub('{.*?}', '', disruption_info.tag)
                if name == 'location':
                    road_name = re.match(r"\[(\w+)\]", disruption_info.text)
                    # for some reason some of them don't have locations/
                    # if this is the case, we'll just ignore it
                    if not road_name:
                        continue
                    road_name = road_name.groups()[0]
                elif name == 'comments':
                    description = disruption_info.text

            road_status[road_name] = description

        return road_status

    def get_road_status(self, road):
        """
        Find road status based on the given search string
        """
        road_statuses = self.get_road_statuses()
        if road.upper() in road_statuses:
            return 'The {0} line currently has {1}'.format(road, road_statuses[road.upper()])
        else:
            return 'There doesn\'t appear to be any problems with that road. So it\'s either clear, i don\'t know about it, or you made it up!'


if __name__ == '__main__':
    tfl_road = TFLROAD()
    print tfl_road.get_road_statuses()
    print tfl_road.get_road_status('M25')
    print tfl_road.get_road_status('A406')
