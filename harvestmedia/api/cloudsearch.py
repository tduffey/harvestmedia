# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

from album import Album
from track import Track
from category import Category
from util import DictObj


class CloudSearchQuery(object):
    METHOD_URI = '/cloudsearch/{{service_token}}'
    AUTOCOMPLETE_METHOD_URI = '/autocomplete/{{service_token}}'

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

    def search_playlist(self, playlist_id, search_term_bundle, result_view, _client, save_search_history=False):

        xml_data = self._search(search_term_bundle, result_view, _client, save_search_history, playlist=playlist_id)

        xml_tracks = xml_data.find('tracks')

        tracks = []

        if xml_tracks is not None:
            for xml_track in xml_tracks.getchildren():
                tracks.append(Track._from_xml(xml_track, _client))

        return tracks

    def _search(self, search_term_bundle, result_view, _client, save_search_history=False, playlist=None):

        xml_data = ET.Element('requestcloudsearch')
        xml_search_filters = ET.SubElement(xml_data, 'searchfilters')
        search_type = 'Normal'
        if playlist:
            ET.SubElement(xml_search_filters, 'playlist').text = playlist
            search_type = 'PlaylistTracks'
        ET.SubElement(xml_search_filters, 'searchtype').text = search_type
        if search_term_bundle:
            xml_search_term_bundle = ET.SubElement(xml_search_filters, 'searchtermbundle')
            for search_term in search_term_bundle:
                xml_element = ET.SubElement(xml_search_term_bundle, search_term.name)
                xml_element.text = search_term.value
                if search_term.fields:
                    for field, value in search_term.fields.iteritems():
                        xml_element.set(field, value)

        if result_view:
            xml_result_view = ET.SubElement(xml_search_filters, 'resultview')
            for view, value in result_view.iteritems():
                ET.SubElement(xml_result_view, view).text = value

        if save_search_history:
            ET.SubElement(xml_search_filters, 'savesearchhistory').text = 'true'

        xml_post_body = ET.tostring(xml_data)

        return _client.post_xml(self.METHOD_URI, xml_post_body)

    def autocomplete_tracks(self, request_autocomplete, _client):
        xml_result = self._autocomplete(request_autocomplete, _client)

        xml_tracks = xml_result.find('autocomplete_tracks')

        tracks = []

        if xml_tracks is not None:
            for xml_track in xml_tracks.getchildren():
                tracks.append(Track._from_xml(xml_track, _client))

        return tracks

    def autocomplete_categories(self, request_autocomplete, _client):
        xml_result = self._autocomplete(request_autocomplete, _client)

        xml_categories = xml_result.find('autocomplete_categoryattributes')

        tracks = []

        if xml_categories is not None:
            for category in xml_categories.getchildren():
                tracks.append(Category._from_xml(category, _client))

        return tracks

    def _autocomplete(self, request_autocomplete, _client):

        xml_data = ET.Element('requestautocomplete')
        if request_autocomplete:
            for field in request_autocomplete:
                xml_element = ET.SubElement(xml_data, field.name)
                xml_element.text = field.value

        xml_element_region = ET.SubElement(xml_data, 'regionid')
        xml_element_region.text = _client.config.region_id

        xml_post_body = ET.tostring(xml_data)

        return _client.post_xml(self.AUTOCOMPLETE_METHOD_URI, xml_post_body)


class CloudSearch(DictObj):

    query = CloudSearchQuery()

    def __init__(self, _client):
        self.client = _client


class SearchTerm:

    def __init__(self, name, value, fields=None):
        self.name = name
        self.value = value
        self.fields = {}
        if fields:
            self.fields = fields

    def addField(self, field):
        self.fields.update(field)

    def addValue(self, value):
        self.value = value

