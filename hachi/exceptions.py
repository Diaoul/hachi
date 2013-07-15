# -*- coding: utf-8 -*-


class HachiError(Exception):
    """Base class for all exceptions in hachi"""
    pass


class Timeout(HachiError):
    """Timeout"""
    pass
