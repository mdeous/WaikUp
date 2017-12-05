# Contributing to WaikUp
:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

This file defines a few guidelines to help people contributing to WaikUp.

## Coding guidelines
* Respect [PEP8](https://pep8.org/), with max line length of 120.
* ~~make tests~~ (not yet, but if you feel like starting this... please do!).
* If you add any new dependency, don't forget to include it in the `Pipfile`
and to run `pipenv install -d`.

## Versionning guidelines
Development of this application and its features (try to) follow the `git-flow` workflow,
to ensure features code is separated from the stable (`master`) branch, and stable code
remains, well... stable!

tl;dr:
* `master` always contains the latest **stable** version.
* `develop` is the most often updated branch, it contains the latest **development**
(but working) version, and should not be considered ready for production.
* New features are developed in a `feature/<feature-name>` branch, and are merged into
`develop` once they're ready.
* Important bug fixes are done in a `hotfix/<fix-name or issue ID>`, and are merged into
`develop` once they're ready.

The complete workflow is explained in details on
[this page](http://nvie.com/posts/a-successful-git-branching-model/), and the `git-flow` 
utility can be found [here](https://github.com/nvie/gitflow).
