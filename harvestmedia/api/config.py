# -*- coding: utf-8 -*-
import logging
import arrow

from urlparse import urlparse

from .exceptions import TokenExpired


logger = logging.getLogger('harvestmedia')


class ServiceToken(object):
    def __init__(self, config, token, offset, expiry):
        self._token = None
        self._offset = None
        self._expiry = None

        self.config = config
        self.offset = offset
        self.expiry = expiry
        self.token = token

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = -int(value)

    @property
    def expiry(self):
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        hm_expire_date = arrow.get(value)
        utc_expire_date = hm_expire_date.shift(hours=self._offset)
        self._expiry = utc_expire_date

    @property
    def token(self):
        utc_now = arrow.utcnow()
        logger.debug('checking token: %s <=> %s' % (self._expiry, utc_now))
        if self._expiry <= utc_now:
            logger.debug('%s <=> %s' % (self._expiry, utc_now))
            raise TokenExpired

        return self._token

    @token.setter
    def token(self, value):
        self._token = value


class Config(object):

    def _set(self, param, default=None, **kwargs):
        if kwargs.get(param, None):
            setattr(self, param, kwargs[param])
        else:
            setattr(self, param, default)

    def __init__(self, *args, **kwargs):
        self._set('waveform_url', **kwargs)
        self._set('webservice_url', **kwargs)
        self._set('debug_level', **kwargs)
        self._set('timezone', 'Australia/Sydney', **kwargs)
        self.service_token = None

        self.album_art_url = None
        self.waveform_url = None
        self.download_url = None
        self.playlistdownload_url = None
        self.playlist_art_url = None
        self.library_logo_url = None
        self.stream_url = None

        self.trackformats = []

    @property
    def webservice_url(self):
        return self._webservice_url

    @webservice_url.setter
    def webservice_url(self, value):
        self.webservice_url_parsed = None

        if value is not None:
            self.webservice_url_parsed = urlparse(value)
            self._webservice_url = value
            self.webservice_prefix = self.webservice_url_parsed.path
            self.webservice_host = self.webservice_url_parsed.netloc

    def get_format_identifier(self, requested_format, bitrate=None, is_master=False):
        format_identifier = None
        for track_format in self.trackformats:
            if track_format['extension'].lower() == str(requested_format).lower() and \
                (bitrate is None or track_format['bitrate'] == bitrate) and \
                ((is_master is True and track_format['ismaster'] == 'true') or \
                 (is_master is False and track_format['ismaster'] == 'false')):
                format_identifier = track_format['identifier']
        return format_identifier
