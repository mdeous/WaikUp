# WaikUp

Collaborative news sharing platform.

## Introduction

WaikUp is an application for teams who want a collaborative platform to share their
findings around the Web.

## API-centric

This application is entirely built around a RESTful API, allowing to build any interface
on top of it, be it a traditionnal WebUI, a browser extension, or a mobile application.

## Version control workflow

Development of this application and its features use the `git-flow` workflow, to ensure
feature's code are separated from the stable (`master`) branch, and stable code remains,
well... stable!

The complete workflow is explained in details on
[this page](http://nvie.com/posts/a-successful-git-branching-model/ "A successful branching model"),
and the `git-flow` utility can be found [here](https://github.com/nvie/gitflow "Git-Flow").

## API endpoints & parameters

### Links API

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

### Users API

* `/api/users/auth` [POST] - Retrieve an authentication token
    * `username` (required)
    * `password` (required)
* `/api/users/deauth` [POST+Auth] - Delete authentication token
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
