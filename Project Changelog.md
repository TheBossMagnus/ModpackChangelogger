# Changleog
All notable changes to this project will be documented in this file. Betas won't be included.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.2) - 2024-03-1
### Fixed
* Fix -f being mandatory
* Fix script not working on some Linux envirornments
* Fix warnings being printed if there weren't added, updated or removed mods

## [0.3.1](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.1) - 2024-03-1
### Fixed
* Fix Removed and added mod being inverted on Modrinth packs

## [0.3.0](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.0) - 2024-03-1
### Added
* Added support for Curseforge modpacks format and API
     * Now, you can use two packs in the Curseforge format and expect changelogs just like with Modrinth packs
* Added a header to the generated changelogs
     * can be easily customized via the config file
### Changed
* Improved the handling of incomplete or malformatted config with proper error messages
* Made some improvements to the resulting changelog
* Made some improvements to the error messages and logging
* The compiled Linux executable is now deprecated

## [0.2.0](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.2.0) - 2024-01-30
### Added
* Adde the option to print changelog to console (just do -f console)
### Fixed
* Fixed  a crash when running as a module
### Changed
* Improve reliability and performance of web requests
* Various refactorings and improvements

## [0.1.0](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.1.0) - 2023-12-24
First Release
