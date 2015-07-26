# API Documentation

## Authentication

Calls to endpoints requiring authentication must provide an `Auth` HTTP header containing the token generated from
your profile information page.


## Links API

* `/api/links/` [GET] - Get all links in database
* `/api/links/<id>` [GET] - Get link with given ID
* `/api/links/` [POST+Auth] - Create a new link
    * `url` (required)
    * `title` (required)
    * `description`
* `/api/links/<id>` [PUT+Owner] - Update informations for link with given ID
    * `url`
    * `title`
    * `description`
* `/api/links/<id>` [DELETE+Owner] - Delete link with given ID


## Users API

* `/api/users/` [GET+Admin] - Get all users in database
* `/api/users/<id>` [GET+Admin] - Get user with given ID
* `/api/users/` [POST+Admin] - Create a new user
    * `username` (required)
    * `first_name` (required)
    * `last_name` (required)
    * `email` (required)
    * `password` (required)
* `/api/links/<id>` [PUT+Admin] - Update informations for user with given ID
    * `first_name`
    * `last_name`
    * `email`
    * `password`
* `/api/links/<id>` [DELETE+Admin] - Delete user with given ID
