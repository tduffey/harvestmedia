# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

from album import Album
from track import Track
from util import DictObj


class CloudSearchQuery(object):
    METHOD_URI = '/cloudsearch/{{service_token}}'

    def get_recent_albums(self, _client):

        xml_data = ET.Element('requestcloudsearch')
        xml_search_filters = ET.SubElement(xml_data, 'searchfilters')
        ET.SubElement(xml_search_filters, 'searchtype').text = 'normal'
        xml_search_term_bundle = ET.SubElement(xml_search_filters, 'searchtermbundle')
        ET.SubElement(xml_search_term_bundle, 'st_keyword_aggregated').text = '%'
        xml_result_view = ET.SubElement(xml_search_filters, 'resultview')
        ET.SubElement(xml_result_view, 'limit').text = '6'
        ET.SubElement(xml_result_view, 'view').text = 'album'
        ET.SubElement(xml_result_view, 'sort_predefined').text = 'ReleaseDate_Desc'

        ET.dump(xml_data)
        xml_post_body = ET.tostring(xml_data)

        xml_data = _client.post_xml(self.METHOD_URI, xml_post_body)

        xml_albums = xml_data.find('albums')

        albums = []

        if xml_albums is not None:
            for xml_album in xml_albums.getchildren():
                albums.append(Album._from_xml(xml_album, _client))

        return albums


    def get_tracks_by_albums(self, album_ids, _client):

        xml_data = ET.Element('requestcloudsearch')
        xml_search_filters = ET.SubElement(xml_data, 'searchfilters')
        ET.SubElement(xml_search_filters, 'searchtype').text = 'normal'
        xml_search_term_bundle = ET.SubElement(xml_search_filters, 'searchtermbundle')
        ET.SubElement(xml_search_term_bundle, 'st_keyword_aggregated').text = '%'
        ET.SubElement(xml_search_term_bundle, 'st_album').text = ','.join(str(i) for i in album_ids)
        xml_result_view = ET.SubElement(xml_search_filters, 'resultview')
        ET.SubElement(xml_result_view, 'limit').text = '100'
        ET.SubElement(xml_result_view, 'view').text = 'track'

        ET.dump(xml_data)
        xml_post_body = ET.tostring(xml_data)

        xml_data = _client.post_xml(self.METHOD_URI, xml_post_body)

        xml_tracks = xml_data.find('tracks')

        tracks = []

        if xml_tracks is not None:
            for xml_track in xml_tracks.getchildren():
                tracks.append(Track._from_xml(xml_track, _client))

        return tracks


class CloudSearch(DictObj):

    query = CloudSearchQuery()

    def __init__(self, _client):
        self.client = _client

