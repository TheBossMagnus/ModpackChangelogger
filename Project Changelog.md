# Changleog
All notable changes to this project will be documented in this file. Betas won't be included.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased - TBD
### **BREAKING CHANGES**
* Changed how the project is installed/used
* Changed the name of many config values
* Changed the package name
* Changed how errors are handled
### Added
* The program is now published to Pypi
     * It can run as a standalone CLI or imported as a module
* Added detection of mods added as .jar in the override folder (only for Modrinth)
* Added detection of changes to config files of mods
* Added the ability to return the changelog as a value in 2 ways
     * Unformatted: 3 different variables (added, updated, removed)
     * Formatted: 1 unified variable with the formatted changelog
* The whole code is now linted via Isort and Black
### Removed
* Removed the already-deprecated Linux-compiled binaries
* Removed the advanced debug logging
### Changed
* Changed how the project has to be run from the source .py files
* Changed some texts in the output changelog
* Improved the handling of the extraction temp dir
* Improved the error handling and the error messages

## [0.3.2](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.2) - 2024-03-1
### Fixed
* Fix -f being mandatory
* Fix script not working on some Linux envirornments
* Fix warnings being printed if there weren't added, updated or removed mods

## [0.3.1](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.1) - 2024-03-1
### Fixed
* Fix Removed and added mod being inverted on Modrinth packs

## [0.3.0](https://github.com/TheBossMagnus/ModpackChangelogger/releases/tag/0.3.0) - 2024-03-1
### **BREAKING CHANGES**
* The compiled Linux executable is now deprecated
### Added
* Added support for Curseforge modpacks format and API
     * Now, you can use two packs in the Curseforge format and expect changelogs just like with Modrinth packs
* Added a header to the generated changelogs
     * can be easily customized via the config file
### Changed
* Improved the handling of incomplete or malformatted config with proper error messages
* Made some improvements to the resulting changelog
* Made some improvements to the error messages and logging

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
