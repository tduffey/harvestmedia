# -*- coding: utf-8 -*-
from urllib import quote as url_quote

from .exceptions import MissingParameter
from .track import Track
from .util import DictObj


class PlaylistQuery(object):
    """Performs calls for the :class:`Playlist` model, also useful in a static
    context.  Available at `Playlist.query` or `playlist_instance.query`

    """

    def get_member_playlists(self, member_id, _client):
        """Gets all of the playlists for a particular member.

        :param member_id: The Harvest Media member identifer
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

        """

        method_uri = '/getmemberplaylists/{{service_token}}/%(member_id)s' % \
                        {'member_id': member_id}
        xml_root = _client.get_xml(method_uri)

        playlists = []
        playlist_elements = xml_root.find('playlists')
        for playlist_element in playlist_elements.getchildren():
            playlist = Playlist._from_xml(playlist_element, _client)
            playlist.member_id = member_id
            playlists.append(playlist)

        return playlists

    def add_track(self, member_id, playlist_id, track_id, _client):
        """Adds a track to a member playlist.

        :param member_id: The Harvest Media member identifer
        :param playlist_id: The Harvest Media playlist identifer
        :param track_id: The Harvest Media track identifer
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

        """

        method_uri = '/addtoplaylist/{{service_token}}/%(member_id)s/%(playlist_id)s/track/%(track_id)s' % \
                          {'member_id': member_id,
                           'playlist_id': playlist_id,
                           'track_id': track_id}
        _client.get_xml(method_uri)

    def remove_track(self, member_id, playlist_id, track_id, _client):
        """Removes a track from a member playlist.

        :param member_id: The Harvest Media member identifer
        :param playlist_id: The Harvest Media playlist identifer
        :param track_id: The Harvest Media track identifer
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

        """

        method_uri = '/removeplaylisttrack/{{service_token}}/%(member_id)s/%(playlist_id)s/%(track_id)s' % \
                            {'member_id': member_id,
                             'playlist_id': playlist_id,
                             'track_id': track_id}
        _client.get_xml(method_uri)

    def remove_playlist(self, member_id, playlist_id, _client):
        """Removes a member playlist.

        :param member_id: The Harvest Media member identifer
        :param playlist_id: The Harvest Media playlist identifer
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

        """

        method_uri = '/removeplaylist/{{service_token}}/%(member_id)s/%(id)s' % \
                        {'member_id': member_id,
                         'id': playlist_id}
        _client.get_xml(method_uri)

    def _add_playlist(self, **kwargs):
        """This method is private because the class method on :class:`Playlist`
        should be used instead

        :param kwargs: The values for the playlist.  See \
        `Add Playlist <http://developer.harvestmedia.net/working-with-members-2/add-a-member-playlist/>`_

        """

        _client = kwargs.get('_client', None)
        if not _client:
            raise MissingParameter('You must pass _client to Playlist.add')

        member_id = kwargs.get('member_id', None)
        if not member_id:
            raise MissingParameter('You must pass member_id to Playlist.add')

        playlist_name = kwargs.get('playlist_name', None)
        if not playlist_name:
            raise MissingParameter('You must pass playlist_name to Playlist.add')

        method_uri = '/addplaylist/{{service_token}}/%(member_id)s/%(playlist_name)s/' % \
                        {'member_id': member_id,
                         'playlist_name': url_quote(playlist_name.encode('utf-8'))}
        xml_root = _client.get_xml(method_uri)
        playlists = xml_root.find('playlists')

        if playlists is not None:
            for playlist_xml in playlists.getchildren():
                name = playlist_xml.get('name')
                if name == playlist_name:
                    return Playlist._from_xml(playlist_xml, _client)


    def update_playlist(self, member_id, playlist_id, playlist_name, _client):
        """Updates a playlist in the Harvest Media database. Essentially
        just a rename.

        :param member_id: The Harvest Media member identifer
        :param playlist_id: The Harvest Media playlist_id identifer
        :param playlist_name: The new name of the playlist"
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`
        :param kwargs: 

        """

        method_uri = '/updateplaylist/{{service_token}}/%(member_id)s/%(playlist_id)s/%(playlist_name)s' % \
                        {'member_id': member_id,
                         'playlist_id': playlist_id,
                         'playlist_name': url_quote(playlist_name.encode('utf-8'))}

        _client.get_xml(method_uri)


class Playlist(DictObj):
    """ Represents a Harvest Media member playlist asset

    :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

    """

    query = PlaylistQuery()

    def __init__(self, _client):

        self.tracks = []
        self._client = _client

    @classmethod
    def _from_xml(cls, xml_data, _client):
        """Internally-used classmethod to create an instance of :class:`Playlist` from
        the XML returned by Harvest Media. Converts all attributes 
        on the node to instance properties.

        Example XML::

            <playlist id="908098a8a0ba8b065" name="sample playlist">
                <tracks>
                    <track tracknumber="1" time="02:50" lengthseconds="170"
                        comment="Track Comment" composer="JJ Jayjay"
                        publisher="PP Peepee" name="Epic Track" albumid="1abcbacbac33" id="11bacbcbabcb3b2823"
                        displaytitle="Epic Track" genre="Pop / Rock"
                        bpm="100" mixout="FULL" frequency="44100" bitrate="1411"
                        dateingested="2008-05-15 06:08:18"/>
                </tracks>
            </playlist>

        :param xml_data: The Harvest Media XML node
        :param _client: An initialized instance of :class:`harvestmedia.api.client.Client`

        """

        instance = cls(_client)
        instance.id = xml_data.get('id')
        for attribute, value in xml_data.items():
            setattr(instance, attribute, value)

        tracks = xml_data.find('tracks')
        if tracks:
            for track in tracks.getchildren():
                instance.tracks.append(Track._from_xml(track, _client))

        return instance

    @classmethod
    def add(cls, **kwargs):
        """Creates and returns a new (empty) playlist for a member 
        `Add Member Playlist <http://developer.harvestmedia.net/working-with-members-2/add-a-member-playlist/>`_
        for arguments.

        """

        return cls.query._add_playlist(**kwargs)

    def add_track(self, track_id):
        """Add a track to a this playlist

        :param track_id: The Harvest Media track identifer

        """

        self.query.add_track(self.member_id, self.playlist_id, track_id, self._client)
        self.tracks.append(Track.query.get_by_id(track_id, self._client))

    def remove_track(self, track_id):
        """Removes a track from this playlist

        :param track_id: The Harvest Media track identifer

        """
        self.query.remove_track(self.member_id, self.id, track_id, self._client)

        for track in self.tracks:
            if track.id == track_id:
                self.tracks.remove(track)

    def remove(self):
        """Remove this playlist"""

        self.query.remove_playlist(self.member_id, self.playlist_id, self._client)

    def update(self):
        """Updates the playlist on Harvest Media with the current values
        values .

        """

        self.query.update_playlist(self.member_id, self.id, self.name, self._client)
