# -*- coding: utf-8 -*-
#
"""
urls.py

.. moduleauthor:: Grischa Meyer <grischa.meyer@monash.edu>

"""

import os

from django.http import HttpResponse
from django.template import Context

from tardis.tardis_portal.auth.decorators import datafile_access_required
from tardis.tardis_portal.shortcuts import render_response_index
from tardis.tardis_portal.models.datafile import Dataset_File
from tardis.tardis_portal.models.parameters import Schema
from tardis.tardis_portal.models.parameters import DatafileParameterSet
from tardis.tardis_portal.models.parameters import DatafileParameter
from tardis.tardis_portal.models.parameters import ParameterName

from tardis.apps.jolecule.settings import JOLECULE_VIEWS_SCHEMA
from tardis.apps.jolecule.settings import JOLECULE_VIEWS_PARNAME


@datafile_access_required
def view(request, dataset_file_id):
    df = Dataset_File.objects.get(id=dataset_file_id)
    context = Context({
        'filename': os.path.splitext(df.filename)[0],
        'dataset_file_id': dataset_file_id,
    })
    return HttpResponse(render_response_index(
        request,
        "jolecule/index.html",
        context))


def _get_create_schema(namespace):
    try:
        the_schema = Schema.objects.get(namespace=namespace)
    except Schema.DoesNotExist:
        the_schema = Schema(namespace=namespace, hidden=True)
        the_schema.save()
    return the_schema


def _get_create_dfps(namespace, dataset_file_id):
    schema = _get_create_schema(namespace)
    try:
        dfps = DatafileParameterSet.objects.get(
            schema=schema,
            dataset_file_id=dataset_file_id)
    except DatafileParameterSet.DoesNotExist:
        dfps = DatafileParameterSet(schema=schema,
                                    dataset_file_id=dataset_file_id)
        dfps.save()
    return dfps


def _get_create_pn(namespace, name):
    schema = _get_create_schema(namespace)
    try:
        pn = ParameterName.objects.get(schema=schema,
                                       name=name)
    except ParameterName.DoesNotExist:
        pn = ParameterName(schema=schema,
                           name=name,
                           full_name=name)
        pn.save()
    return pn


def _get_views(dataset_file_id):
    dfps = _get_create_dfps(JOLECULE_VIEWS_SCHEMA, dataset_file_id)
    _get_create_pn(JOLECULE_VIEWS_SCHEMA, JOLECULE_VIEWS_PARNAME)
    views = dfps.get_param(JOLECULE_VIEWS_PARNAME, value=True)
    return views


@datafile_access_required
def loadViews(request, dataset_file_id):
    try:
        views = _get_views(dataset_file_id)
    except DatafileParameter.DoesNotExist:
        views = "{}"
    return HttpResponse(views, mimetype='application/json')


@datafile_access_required
def saveViews(request, dataset_file_id):
    response = HttpResponse(None)
    if request.method == "POST":
        if request.user.has_perm('tardis_acls.change_dataset_file',
                                 Dataset_File.objects.get(id=dataset_file_id)):
            new_views = request.body
            dfps = _get_create_dfps(JOLECULE_VIEWS_SCHEMA, dataset_file_id)
            dfps.set_param(JOLECULE_VIEWS_PARNAME, new_views)
            response.status_code = 201
        else:
            response.status_code = 401
    else:
        response.status_code = 200
    return response
