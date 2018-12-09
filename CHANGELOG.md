# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - [Unreleased]
### Added
- Base feature set added

## [0.6.0] - 2018-12-09
### Changed
*   Refactored RedditYoutubeBot -> RedditBot
*   Refactored post_template.txt -> template.md to make use of Reddit's markdown style comments.
*   Changed README.md: revised Badges and added html centering for title/description.
*   Added database.load_db to encapsulate database loading logic.  Also implemented six for urllib to simplify imports.

*   Started simplifying the functions in each bot that were too complex:
    -   Added YouCompareBot.make_relationship to abstract that logic out.
    -   Added RedditBot.comment override that does retry logic within the RedditBot not within YouCompareBot.
    -   Moved class properties REDDIT_REPLY_INTERVAL and REDDIT_NUM_RETRIES from YouCompareBot to RedditBot
## Added
*   Added Changelog for 0.5.0 release
*   Added boilerplate CONTRIBUTING.md

## [0.5.0] - 2018-12-03
### Changed
*   Removed cli.py in favor of __main__.py as entrypoint.
*   Segregated logging to its own module and added logging points to both stream/file handlers.
*   Fixed Procfile entry according to new entrypoint
*   Added error check in case the user entered invalid Reddit credentials.
### Added
*   Added a placeholder CLI flag for specifying run intervals on continuous runs.
*   Automated building the conf.REDDIT_AGENT.

## [0.4.0] - 2018-11-21
### Added
*   CLI entry point/argparser module.
*   Heroku Procfile
### Changed
*   Added class properties to YouCompareBot to enable changing vars at runtime
    -   YouCompareBot.post_template_file = conf.POST_TEMPLATE
    -   YouCompareBot.SIMILARITY_LIMIT = conf.SIMILARITY_LIMIT
    -   YouCompareBot.REDDIT_REPLY_INTERVAL = conf.REDDIT_REPLY_INTERVAL
    -   YouCompareBot.REDDIT_NUM_RETRIES = conf.REDDIT_NUM_RETRIES
*   Removed unused RedditYoutubeBot.SUBMISSION_TRACKER

## [0.3.0] - 2018-11-21
### Changed
*   Refactored code base to use SQL database structure with [peewee](https://peewee.readthedocs.io/en/latest/index.html)
*   Fixed CircleCI config file
*   Added TOC and new header names to [README.md](README.md)
### Added
*   Added new unittests
*   Added coverage reporting
*   Added [CHANGELOG.md](CHANGELOG.md)
*   Added [LICENSE.md](LICENSE.md)

## [0.2.0] - 2018-11-14
### Changed
*   Fixed README.md to conform with Markdown conventions.
### Added
*   Enabled combining coverage for all versions of python coverage reports
### Fixed
*   Fixed 62 Codacy issues
*   Fixed persisting workspace folders in CircleCI

## [0.1.0] - 2018-11-10
### Changed
*   Specified Nosetests as test runner instead of unittest
*   CircleCI Coverage reporting section that is still WIP
*   Updated all imports to be package referenced instead of local referenced
### Added
*   .txt file for checking checked posts
*   Codacy badge/initial setup
### Fixed
*   config.py -> conf.py to fix any namespace issues.

## Release Comparisons
-   [0.6.0](https://github.com/AndresMWeber/youcomment/compare/v0.5.0-alpha...v0.6.0-alpha)
-   [0.5.0](https://github.com/AndresMWeber/youcomment/compare/v0.4.0-alpha...v0.5.0-alpha)
-   [0.4.1](https://github.com/AndresMWeber/youcomment/compare/v0.3.0-alpha...v0.4.0-alpha)
-   [0.3.0](https://github.com/AndresMWeber/youcomment/compare/v0.2.0-alpha...v0.3.0-alpha)
-   [0.2.0](https://github.com/AndresMWeber/youcomment/compare/v0.2.0-alpha...v0.1.0-alpha)
-   [0.1.0](https://github.com/AndresMWeber/youcomment/compare/e62c443...v0.1.0-alpha)
