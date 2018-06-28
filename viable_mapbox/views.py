#!/usr/bin/env python

"""Views for Mapbox Integration module for Viable Cloud API.

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


from flask import jsonify
from flask import redirect
from flask import request


from . import module
from . import utilities


@module.route('/v1/data/dataset', methods=['OPTIONS'])
def mapbox_datasets_index_options():
    """Define default index page preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    }), 200


@module.route('/v1/data/dataset', methods=['GET'])
def mapbox_datasets_index_get():

    datasets_ = utilities.get_datasets()

    """Define default index page content."""
    return jsonify(**{
        "type": "FeatureCollection",
        "features": datasets_
    }), 200

@module.route('/v1/data/dataset/<string:dataset_id>', methods=['OPTIONS'])
def mapbox_dataset_index_options(dataset_id):
    """Define default index page preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    }), 200


@module.route('/v1/data/dataset/<string:dataset_id>', methods=['GET'])
def mapbox_dataset_index_get(dataset_id):

    dataset_ = utilities.get_dataset(dataset_id)

    """Define default index page content."""
    return jsonify(**{
        "type": "FeatureCollection",
        "features": dataset_.get("features", []),
        "properties": {
            "fields": dataset_.get("fields", [])
        }
    }), 200

@module.route('/v1/data/dataset/<string:dataset_id>/feature/<string:feature_id>', methods=['OPTIONS'])
def mapbox_feature_index_options(dataset_id, feature_id):
    """Define default index page preflight check."""
    return jsonify(**{
        'meta': {
            'status': 200
        }
    }), 200


@module.route('/v1/data/dataset/<string:dataset_id>/feature/<string:feature_id>', methods=['GET'])
def mapbox_feature_index_get(dataset_id, feature_id):

    feature_ = utilities.get_feature(dataset_id, feature_id)

    if feature_ == [] or feature_ == None:
        return jsonify(**{
            'meta': {
                'status': 404
            },
            'properties': {
                'message': 'Feature not found'
            }
        }), 404

    """Define default index page content."""
    return jsonify(**feature_), 200


@module.route('/v1/data/dataset/<string:dataset_id>/feature/<string:feature_id>', methods=['PUT'])
def mapbox_feature_index_put(dataset_id, feature_id):

    data_ = request.get_data()

    feature_ = utilities.put_feature(dataset_id, feature_id, data_)

    """Define default index page content."""
    return jsonify(**feature_), 200
