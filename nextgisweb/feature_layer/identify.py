# -*- coding: utf-8 -*-
import json

from pyramid.response import Response

from view import ComplexEncoder
from .interface import IFeatureLayer
from ..geometry import geom_from_wkt
from ..models import DBSession
from ..resource import (
    Resource,
    ResourceScope,
    DataScope)

PR_R = ResourceScope.read


def identify(request):
    """
    ---
    post:
      summary: Identification service for layers that support IFeatureLayer.
      description:
      tags:
        - feature_layer
      parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            geom:
              description: Polygon geometry in WKT.
              type: string
            layers:
              description: Array of layers identifiers
              type: array
            srs:
              description: EPSG code of definition of coordinate reference systems
              type: number
      consumes:
      - application/json
      produces:
      - application/json
      responses:
        200:
          description: success
          schema:
            type: object
            description: Dictionary where key - layer identifier, value - features count and array of features
    """
    sett_name = 'permissions.disable_check.identify'
    setting_disable_check = request.env.core.settings.get(sett_name, 'false').lower()
    if setting_disable_check in ('true', 'yes', '1'):
        setting_disable_check = True
    else:
        setting_disable_check = False

    srs = int(request.json_body['srs'])
    geom = geom_from_wkt(request.json_body['geom'], srid=srs)
    lids = map(int, (
        layer['id'] for layer in request.json_body['layers']))
    queries = map(json.loads, (
        layer['query'] for layer in request.json_body['layers']))

    layer_list = DBSession.query(Resource).filter(Resource.id.in_(lids))

    result = dict()

    # Number of features in all layers
    feature_count = 0

    for idx, layer in enumerate(layer_list):
        if not setting_disable_check and not layer.has_permission(DataScope.read, request.user):
            result[layer.id] = dict(error="Forbidden")

        elif not IFeatureLayer.providedBy(layer):
            result[layer.id] = dict(error="Not implemented")

        else:
            query = layer.feature_query()
            query.intersects(geom)
            query.filter_by_query(queries[idx])

            # Limit number of identifyable features by 10 per layer,
            # otherwise the response might be too big.
            query.limit(10)

            features = [
                dict(id=f.id, layerId=layer.id,
                     label=f.label, fields=f.fields)
                for f in query()
            ]

            # Add name of parent resource to identification results,
            # if there is no way to get layer name by id on the client
            if not setting_disable_check:
                allow = layer.parent.has_permission(PR_R, request.user)
            else:
                allow = True

            if allow:
                for feature in features:
                    feature['parent'] = layer.parent.display_name

            result[layer.id] = dict(
                features=features,
                featureCount=len(features)
            )

            feature_count += len(features)

    result['featureCount'] = feature_count

    return Response(
        json.dumps(result, cls=ComplexEncoder),
        content_type='application/json')
