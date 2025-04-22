# Changleog
All notable changes to this project will be documented in this file. Betas won't be included.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## To be released
### **BREAKING CHANGES**
* Changed how to generate a blank config (`modpack-changelogger newconfig`, instead of `modpack-changelogger -c new`)
### Added
### Changed
* Improved the cli interface, now using click
* Improved help messages
* Improved the project structure
### Fixed
* Fixed the handling of packs that don't follow the respective format specs
* Handle some errors better
* Fixed many naming inconsistencies arround the project


## [1.0.2](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/1.0.2) - 2025-04-5
republish of 1.0.2

## [1.0.1](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/1.0.1) - 2025-04-5

### Changed
* Bump to Python 3.13
* Re-wrote CI/CD
* Restructured project to follow best practices

### Fixed
* Some changes being mislabeled on some formats
* If runned from cli withouth any args the help meu is now displayed instead of an exception
* If an unknown arg is given avoid trowing an exception

## [1.0.0](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/1.0.0) - 2024-06-22
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

## [0.3.2](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/0.3.2) - 2024-03-1
### Fixed
* Fix -f being mandatory
* Fix script not working on some Linux envirornments
* Fix warnings being printed if there weren't added, updated or removed mods

## [0.3.1](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/0.3.1) - 2024-03-1
### Fixed
* Fix Removed and added mod being inverted on Modrinth packs

## [0.3.0](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/0.3.0) - 2024-03-1
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

## [0.2.0](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/0.2.0) - 2024-01-30
### Added
* Adde the option to print changelog to console (just do -f console)
### Fixed
* Fixed  a crash when running as a module
### Changed
* Improve reliability and performance of web requests
* Various refactorings and improvements

## [0.1.0](https://github.com/TheBossMagnus/modpack-changelogger/releases/tag/0.1.0) - 2023-12-24
First Release
