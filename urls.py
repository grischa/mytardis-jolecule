# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns(
    'tardis.apps.jolecule.views',
    (r'^view/(?P<dataset_file_id>\d+)/$', 'view'),
    (r'^loadViews/(?P<dataset_file_id>\d+)/$', 'loadViews'),
    (r'^saveView/(?P<dataset_file_id>\d+)/$', 'saveViews'),
)
