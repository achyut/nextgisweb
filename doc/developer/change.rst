.. sectionauthor:: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.ru>

Editing
==============

Change resource
-----------------

Execute following PUT request to change resource.

.. http:put:: /resource/(int:parent_id)/child/(int:id)

   Change resource request
    
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate    
   :param parent_id: parent resource id
   :param id: changing resource id
   :<json jsonobj resource: resource JSON object
   :<json string display_name: resource new name
   :<json string keyname: resource new key
   :<json int id: resource id (cannot be changed)
   :<json string description: resource new description
   :<jsonarr permissions: resource permissions array
   :statuscode 200: no error
   
**Example request**:

.. sourcecode:: http

   PUT /resource/7/child/8 HTTP/1.1
   Host: ngw_url
   Accept: */*
   
   {"resource":
      {
          "display_name":"test3",
          "keyname":"qw4",
          "parent":{"id":7},
          "permissions":[],
          "description":"rrr5"
       }
   }

.. note::
   Payload of change resource request is equal to create resource request payload. The request must be authorized.
   
Change file bucket resource
-----------------------------

To change file bucket execute following PUT request:

.. http:put:: /api/resource/(int:id)

   Change file bucket request.
    
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate 
   :param id: resource identificator
   :<json jsonobj resource: resource JSON object
   :<json string cls: type (must be ``file_bucket``, for a list of supported types see :ref:`ngwdev_resource_classes`)
   :<json jsonobj parent:  parent resource json object
   :<json int id: parent resource identificator
   :<json string display_name: name
   :<json string keyname: key (optional)
   :<json string description: decription text, HTML supported (optional)
   :<json jsonobj file_bucket: file bucket JSON object
   :<jsonarr files: array of files should present in bucket: present (which need to delete don't include in array), also new files (upload response JSON object, files == upload_meta)
   :statuscode 200: no error
      
**Example request**:

.. sourcecode:: http

   PUT /api/resource/22 HTTP/1.1
   Host: ngw_url
   Accept: */*

    {
      "file_bucket": {
        "files": [
          {
            "mime_type": "application/x-dbf", 
            "name": "grunt_area_2_multipolygon.dbf", 
            "size": 36607
          }, 
          {
            "mime_type": "application/x-esri-shape", 
            "name": "grunt_area_2_multipolygon.shp", 
            "size": 65132
          }, 
          {
            "mime_type": "application/x-esri-shape", 
            "name": "grunt_area_2_multipolygon.shx", 
            "size": 1324
          },
          {
            "id": "fb439bfa-1a63-cccc-957d-ae57bb5eb67b", 
            "mime_type": "application/octet-stream", 
            "name": "grunt area description.txt", 
            "size": 50
          }
        ]
      }, 
      "resource": {
        "cls": "file_bucket", 
        "description": "some new text", 
        "display_name": "new grunt_area", 
        "keyname": null, 
        "parent": {
          "id": 0
        }
      }
    }
    
In this example, file *grunt area description.txt* will be added, files
*grunt_area_2_multipolygon.cpg*, *grunt_area_2_multipolygon.prj* - deleted, 
and bucket name and description will be changed.

Change lookup table resource
-----------------------------

To change flookup table execute following PUT request:

.. http:put:: /api/resource/(int:id)

   Change lookup table request.
    
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate 
   :param id: resource identificator
   :<json jsonobj resource: resource JSON object
   :<json string cls: type (must be ``lookup_table``, for a list of supported types see :ref:`ngwdev_resource_classes`)
   :<json int id: parent resource identificator
   :<json string display_name: name
   :<json string keyname: key (optional)
   :<json string description: decription text, HTML supported (optional)
   :<json jsonobj resmeta: metadata JSON object. Key - value JSON object struct.
   :<json file_bucket: file bucket JSON object
   :<json jsonobj lookup_table: lookup table values JSON object. Key - value JSON object struct.
   :statuscode 200: no error
      
**Example request**:

.. sourcecode:: http

   PUT /api/resource/22 HTTP/1.1
   Host: ngw_url
   Accept: */*

   {
     "lookup_table": {
        "items": {
            "car": "Машина",
            "plane": "Самолет"
        }
     }
   }
   
Same steps with curl:

.. sourcecode:: bash
   
   $ curl --user "user:password" -H 'Accept: */*' -X PUT -d '{"lookup_table":
   {"items":{"car":"Машина", "plane":"Самолет"}}}' 
   http://<ngw url>/api/resource/

Change feature
----------------

To change feature in vector layer execute following request:

.. http:put:: /api/resource/(int:layer_id)/feature/(int:feature_id)

   Change feature request
   
   :param layer_id: layer resource identificator
   :param feature_id: feature identificator
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate 
   :<json string geom: geometry in WKT format (geometry type ans spatial reference must be corespondent to layer geometry type and spatial reference)
   :<jsonarr fields: attributes array in form of JSON field name - value object 
   :<json int id: feture identificator
   :statuscode 200: no error
   
**Example request**:

.. sourcecode:: http

   PUT /api/resource/3/feature/1 HTTP/1.1
   Host: ngw_url
   Accept: */*
   
   {
     "extensions": {
       "attachment": null, 
       "description": null
     }, 
     "fields": {
       "Age": 1, 
       "DateTr": {
         "day": 7, 
         "month": 2, 
         "year": 2015
       }, 
       "Davnost": 4, 
       "Foto": 26, 
       "Nomerp": 1, 
       "Nomers": 1, 
       "Samka": 0, 
       "Sex": 3, 
       "Sizeb": 0.0, 
       "Sizef": 0.0, 
       "Sizes": 9.19999980926514, 
       "Snowdepth": 31, 
       "Wher": "\u043b\u044b\u0436\u043d\u044f", 
       "id01": 0
     }, 
     "geom": "MULTIPOINT (15112317.9207317382097244 6059092.3103669174015522)", 
     "id": 1
   }   
   
In request payload add only change fields. Other fields will stay unchanged. Also geom field may be skipped.

To change features in batch mode use patch request.

.. http:patch:: /api/resource/(int:layer_id)/feature

   Change features request
   
   :param layer_id: layer resource identificator
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate 
   :<jsonarr string geom: geometry in WKT format (geometry type ans spatial reference must be corespondent to layer geometry type and spatial reference)
   :<jsonarr jsonarr fields: attributes array in form of JSON field name - value object 
   :<jsonarr int id: feture identificator
   :statuscode 200: no error
   
Request accept array of JSON objects. If feature identificator is not present in vector layer - 
feature will be created, else - changed.
.. Метод принимает на вход список объектов, если у объекта передан id - то обновляется этот объект, а у которых не передан - те создаёт
   
Delete feature
---------------

To delete feature from vector layer execute following request:

.. http:delete:: /api/resource/(int:layer_id)/feature/(int:feature_id)

   Delete feature request
   
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate
   :param layer_id: resource identificator
   :param feature_id: feature identificator
   :statuscode 200: no error
   
**Example request**:

.. sourcecode:: http

   DELETE /api/resource/3/feature/1 HTTP/1.1
   Host: ngw_url
   Accept: */*
   
   
Delete all features
---------------------

To delete all feature in vector layer execute following request:

.. http:delete:: /api/resource/(int:layer_id)/feature/

   Delete features request
   
   :reqheader Accept: must be ``*/*``
   :reqheader Authorization: optional Basic auth string to authenticate
   :param layer_id: resource identificator
   :statuscode 200: no error
   
**Example request**:

.. sourcecode:: http

   DELETE /api/resource/3/feature/ HTTP/1.1
   Host: ngw_url
   Accept: */*
