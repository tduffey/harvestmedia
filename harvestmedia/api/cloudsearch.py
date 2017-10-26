# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

from album import Album
from track import Track
from util import DictObj


class CloudSearchQuery(object):
    METHOD_URI = '/cloudsearch/{{service_token}}'

    def search_albums(self, search_term_bundle, result_view, _client, save_search_history=False):

        xml_data = self._search(search_term_bundle, result_view, _client, save_search_history)

        xml_albums = xml_data.find('albums')

        albums = []
        if xml_albums is not None:
            for xml_album in xml_albums.getchildren():
                albums.append(Album._from_xml(xml_album, _client))

        return albums

    def search_tracks(self, search_term_bundle, result_view, _client, save_search_history=False):

        xml_data = self._search(search_term_bundle, result_view, _client, save_search_history)

        xml_tracks = xml_data.find('tracks')

        tracks = []

        if xml_tracks is not None:
            for xml_track in xml_tracks.getchildren():
                tracks.append(Track._from_xml(xml_track, _client))

        return tracks

    def _search(self, search_term_bundle, result_view, _client, save_search_history=False):

        xml_data = ET.Element('requestcloudsearch')
        xml_search_filters = ET.SubElement(xml_data, 'searchfilters')
        ET.SubElement(xml_search_filters, 'searchtype').text = 'normal'
        if search_term_bundle:
            xml_search_term_bundle = ET.SubElement(xml_search_filters, 'searchtermbundle')
            for search_term, value in search_term_bundle.iteritems():
                ET.SubElement(xml_search_term_bundle, search_term).text = value

        if result_view:
            xml_result_view = ET.SubElement(xml_search_filters, 'resultview')
            for view, value in result_view.iteritems():
                ET.SubElement(xml_result_view, view).text = value

        if save_search_history:
            ET.SubElement(xml_search_filters, 'savesearchhistory').text = 'true'

        print 'dump ' + ET.tostring(xml_data)
        xml_post_body = ET.tostring(xml_data)

        return _client.post_xml(self.METHOD_URI, xml_post_body)



class CloudSearch(DictObj):

    query = CloudSearchQuery()

    def __init__(self, _client):
        self.client = _client

