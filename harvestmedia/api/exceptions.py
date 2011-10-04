# -*- coding: utf-8 -*-

class HarvestMediaError(Exception):
    def __init__(self, reason):
        super(HarvestMediaError, self).__init__(reason)


class APITimeoutError(HarvestMediaError):
    pass

class InvalidAPIResponse(HarvestMediaError):
    def __init__(self, reason):
        super(HarvestMediaError, self).__init__(reason)
        self.code = None

class MissingParameter(HarvestMediaError):
    pass
