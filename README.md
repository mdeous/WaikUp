# WaikUp

Collaborative news sharing platform.

## Introduction

WaikUp is an application for teams who want a collaborative platform to share their findings around the Web.

Additionally to the traditionnal web interface, WaikUp provides a RESTful API to allow any other interface 
(browser extension, mobile application, etc...) to be built upon it.


## Development status

* Web UI: OK
* Users management: OK (misses reader/contributor roles)
* API: NOT USABLE YET
* Database migration: NOT USABLE YET


## Management utility

All the application's management is done using the `waikup_manage` utility (installed in your `$PATH` by the `setup.py`).

_To be more documented... Meanwhile, use `--help` to know more about available commands_


## API

A dedicated documentation page is available [here](docs/API.md).


## Deployment

A dedicated documentation page is available [here](docs/DEPLOY.md).


## Issues and contributions

If you encounter any bug, or think a particular feature is missing, feel free to open a ticket, or even better, fork 
the repository and make a pull request with your changes! ;)


### Version control workflow

Development of this application and its features (try to) follow the `git-flow` workflow, to ensure features' code is 
separated from the stable (`master`) branch, and stable code remains, well... stable!

The complete workflow is explained in details on
[this page](http://nvie.com/posts/a-successful-git-branching-model/ "A successful branching model"),
and the `git-flow` utility can be found [here](https://github.com/nvie/gitflow "Git-Flow").



## Licensing

This project is licensed under the GNU General Public License v3.
