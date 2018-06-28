#!/usr/bin/env python

"""Utlities for Mapbox Integration module for Viable Cloud API.

Created by Viable Industries, L.L.C. on 06/28/2018.
Copyright (c) 2018 Viable Industries, L.L.C. All rights reserved.

For license and copyright information please see the LICENSE document (the
"License") included with this software package. This file may not be used
in any manner except in compliance with the License unless required by
applicable law or agreed to in writing, software distributed under the
License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.

See the License for the specific language governing permissions and
limitations under the License.
"""


import json
import requests
import time
import urllib2


from app import logger


from flask import current_app
from flask import jsonify


def get_datasets():
    """Load a list of datasets from the Mapbox API.

    @return (object) response
        the fully qualified response object
    """
    logger.info('get_datasets')

    datasets_ = []

    time_ = int(time.time())

    try:
        response = urllib2.urlopen('https://api.mapbox.com/datasets/v1/%s?access_token=%s&_=%s' % (current_app.config['MAPBOX_USER_NAME'], current_app.config['MAPBOX_ACCESS_TOKEN'], time_))
        datasets_ = json.loads(response.read(response))
    except urllib2.HTTPError as error:
        logger.error('Mapbox API responded with an unexpected value')
        reader = error.read()

    return datasets_

def get_dataset(dataset_id, preview=False):
    """Load a list of features from a single dataset from the Mapbox API.

    :param (object) dataset_id
        a Mapbox API dataset ID

    @return (object) response
        the fully qualified response object
    """
    logger.info('get_dataset')

    datasets_ = []

    time_ = int(time.time())

    limit = ""

    if preview:
        limit = "limit=3&"

    try:
        url_ = 'https://api.mapbox.com/datasets/v1/%s/%s/features?%saccess_token=%s&_=%s' % (current_app.config['MAPBOX_USER_NAME'], dataset_id, limit, current_app.config['MAPBOX_ACCESS_TOKEN'], time_)
        response = urllib2.urlopen(url_)
        features_ = json.loads(response.read(response))
    except urllib2.HTTPError as error:
        logger.error('Mapbox API responded with an unexpected value')
        reader = error.read()

    """Lookup available fields.
    """
    features_["fields"] = get_fields(features_)

    return features_

def get_feature(dataset_id, feature_id):
    """Load a single feature from the Mapbox API.

    :param (object) dataset_id
        a Mapbox API dataset ID

    :param (object) feature_id
        a Mapbox API dataset feature ID

    @return (object) response
        the fully qualified response object
    """
    logger.info('get_feature')

    time_ = int(time.time())

    try:
        response = urllib2.urlopen('https://api.mapbox.com/datasets/v1/%s/%s/features/%s?access_token=%s&_=%s' % (current_app.config['MAPBOX_USER_NAME'], dataset_id, feature_id, current_app.config['MAPBOX_ACCESS_TOKEN'], time_))
        feature_ = json.loads(response.read(response))
    except urllib2.HTTPError as error:
        logger.error('Mapbox API responded with an unexpected value')
        reader = error.read()

    return feature_

def put_feature(dataset_id, feature_id, payload):
    """Load a single feature from the Mapbox API.

    :param (object) dataset_id
        a Mapbox API dataset ID

    :param (object) feature_id
        a Mapbox API dataset feature ID

    @return (object) response
        the fully qualified response object
    """
    logger.info('Update a feature %s', payload)

    try:
        url_ = 'https://api.mapbox.com/datasets/v1/%s/%s/features?access_token=%s' % (current_app.config['MAPBOX_USER_NAME'], dataset_id, current_app.config['MAPBOX_ACCESS_TOKEN'])

        headers_ = {
            'Content-Type': 'application/json'
        }

        feature_ = json.loads(payload)

        payload_ = {
            "put": [feature_],
            "delete": []
        }

        final_payload_ = json.dumps(payload_)

        logger.info('Payload being submitted to Mapbox %s', final_payload_)

        response_ = requests.post(url_, headers=headers_, data=final_payload_)

        if response_.raise_for_status():
            logger.error(response_.raise_for_status())

        response_data_ = response_.json()

        logger.info('Request successfuly with data: %s', response_data_)

        update_tileset(dataset_id)

    except urllib2.HTTPError as error:
        logger.error('Mapbox API responded with an unexpected value')
        reader = error.read()

    return response_data_

def delete_feature(dataset_id, feature_id):
    """Delete a single feature from the Mapbox API.

    :param (object) dataset_id
        a Mapbox API dataset ID

    :param (object) feature_id
        a Mapbox API dataset feature ID

    @return (object) response
        the fully qualified response object
    """
    logger.info('Delete feature %s', feature_id)

    try:
        url_ = 'https://api.mapbox.com/datasets/v1/%s/%s/features/%s?access_token=%s' % (current_app.config['MAPBOX_USER_NAME'], dataset_id, feature_id, current_app.config['MAPBOX_ACCESS_TOKEN'])

        headers_ = {
            'Content-Type': 'application/json'
        }

        response_ = requests.delete(url_, headers=headers_)

        if response_.raise_for_status():
            logger.error(response_.raise_for_status())

        logger.info('Delete complete')

        update_tileset(dataset_id)

    except urllib2.HTTPError as error:
        logger.error('Mapbox API responded with an unexpected value')
        reader = error.read()

    return {}

def get_fields(dataset):

    fields_ = set()

    for index_, feature_ in enumerate(dataset["features"]):
        for field_name_, value_ in enumerate(feature_["properties"]):
            fields_.add(value_)

    return list(fields_)


def update_tileset(dataset_id):
    """Update a Tileset in the Mapbox API.

    :param (object) dataset_id
        a Mapbox API dataset ID

    @return (object) response
        the fully qualified response object
    """

    user_ = current_app.config['MAPBOX_USER_NAME']
    tileset_id = "viablefractracker.cjiuc7qk601r2cqpe720dmrvq-6pnn7"

    response = requests.post(
        url="https://api.mapbox.com/uploads/v1/%s" % (user_),
        params={
            "access_token": current_app.config['MAPBOX_ACCESS_TOKEN'],
        },
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
        data=json.dumps({
            "name": "reports",
            "tileset": tileset_id,
            "url": "mapbox://datasets/%s/%s" % (user_, dataset_id)
        })
    )

    if response.raise_for_status():
        logger.error(response.raise_for_status())

    logger.info('Update Tileset Request Complete')

    return response
