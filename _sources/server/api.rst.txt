The API
=======

The server exposes a simple API to get data from the database. The methods can
be classified in two groups, based on the object they return. All API access is
over HTTPS and accessed from ``https://giuseppe-desolda.ddns.net:8080``. All
data is returned as JSON.

Users
-----

Index
*****

* :http:get:`/api/users`
* :http:get:`/api/users/(int:skip)-(int:limit)`
* :http:get:`/api/user/(str:id)`

APIs
****

.. http:get:: /api/users

   Get all the users.

   **Example request**:

   .. sourcecode:: http

      GET /api/users HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5ea18ca785dffb5712068595",
            "age": "2",
            "internet": "4",
            "gender": "m"
         },
         {
            "_id": "5ea1b63385dffb57120720c3",
            "age": "2",
            "internet": "4",
            "gender": "m"
         }
      ]
      
   :statuscode 200: No error

.. http:get:: /api/users/(int:skip)-(int:limit)

   Get the first `limit` users starting from `skip` (included).

   **Example request**:

   .. sourcecode:: http

      GET /api/users/3-2 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5eab3d3f348b1746eeb06a99",
            "age": "2",
            "gender": "m",
            "internet": "18"
         },
         {
            "_id": "5eb014d0348b1746eeb76c18",
            "age": "2",
            "gender": "m",
            "internet": "18"
         }
      ]
   
   :param skip: The number of users to skip
   :param limit: The number of users to return
   :statuscode 200: No error

.. http:get:: /api/user/(str:id)

   Get the user with id `id`.

   **Example request**:

   .. sourcecode:: http

      GET /api/user/5ebd67189976b12b146a2735 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
         "_id": "5ebd67189976b12b146a2735",
         "age": "2",
         "gender": "f",
         "internet": "7"
      }
      
   :param id: The id of the user
   :statuscode 200: No error

Interactions
------------

Index
*****

* :http:get:`/api/interactions`
* :http:get:`/api/interactions/(int:skip)-(int:limit)`
* :http:get:`/api/interaction/(str:id)`
* :http:get:`/api/user/(str:id)/interactions`
* :http:get:`/api/user/(str:id)/interactions/(int:skip)-(int:limit)`

APIs
****

.. http:get:: /api/interactions

   Get all the interactions. **Warning:** due to the huge quantity of data it's
   likely that the connection will timeout.

   **Example request**:

   .. sourcecode:: http

      GET /api/user/5ebd67189976b12b146a2735 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5ea1bc9a85dffb571207298e",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878562,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb571207298f",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878685,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072990",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878810,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072991",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878857,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072992",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878966,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         }
      ]
      
   :statuscode 200: No error

.. http:get:: /api/interactions/(int:skip)-(int:limit)

   Get the first `limit` interactions starting from the `skip`. **Warning:** due
   to the huge quantity of data it's likely that the connection will timeout.

   **Example request**:

   .. sourcecode:: http

      GET /api/interactions/4-2 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5ea1bc9a85dffb5712072992",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878966,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072993",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657879058,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         }
      ]
      
   :param skip: The number of interactions to skip
   :param limit: The number of interactions to return
   :statuscode 200: No error

.. http:get:: /api/interaction/(str:id)

   Get the interaction with id `id`.

   **Example request**:

   .. sourcecode:: http

      GET /api/interaction/5ea1bc9a85dffb5712072992 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      {
         "_id": "5ea1bc9a85dffb5712072992",
         "k": {
            "a": false,
            "f": false,
            "n": false,
            "s": false
         },
         "m": {
            "b": {
               "l": false,
               "r": false,
               "m": false
            },
            "p": [
               0,
               0
            ]
         },
         "s": {
            "a": [
               0,
               400
            ],
            "r": [
               100,
               400
            ]
         },
         "t": 1587657878966,
         "u": "https://www.repubblica.it/",
         "ui": "5ea1b63385dffb57120720c3",
         "w": [
            1537,
            956
         ],
         "e": {}
      }
      
   :param id: The id of the interaction
   :statuscode 200: No error

.. http:get:: /api/user/(str:id)/interactions

   Get all the interaction of the user with id `id`.

   **Example request**:

   .. sourcecode:: http

      GET /api/user/5ea1b63385dffb57120720c3/interactions HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5ea1bc9a85dffb571207298e",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878562,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb571207298f",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878685,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072990",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657878810,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         }
      ]
      
   :param id: The id of the user
   :statuscode 200: No error

.. http:get:: /api/user/(str:id)/interactions/(int:skip)-(int:limit)

   Get the first `limit` interactions starting from the `skip` of the user with
   id `id`.

   **Example request**:

   .. sourcecode:: http

      GET /api/user/5ea1b63385dffb57120720c3/interactions/6-2 HTTP/1.1
      HOST: giuseppe-desolda.ddns.net:8080

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json; charset=utf-8

      [
         {
            "_id": "5ea1bc9a85dffb5712072994",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657879177,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         },
         {
            "_id": "5ea1bc9a85dffb5712072995",
            "k": {
               "a": false,
               "f": false,
               "n": false,
               "s": false
            },
            "m": {
               "b": {
                  "l": false,
                  "r": false,
                  "m": false
               },
               "p": [
                  0,
                  0
               ]
            },
            "s": {
               "a": [
                  0,
                  400
               ],
               "r": [
                  100,
                  400
               ]
            },
            "t": 1587657879295,
            "u": "https://www.repubblica.it/",
            "ui": "5ea1b63385dffb57120720c3",
            "w": [
               1537,
               956
            ],
            "e": {}
         }
      ]
      
   :param skip: The number of interactions to skip
   :param limit: The number of interactions to return
   :param id: The id of the user
   :statuscode 200: No error
