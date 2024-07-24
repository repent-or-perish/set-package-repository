# Set Package Repository

Set Package Repository is a simple GTK3 application that allows users to select a package repository for GhostBSD and update the `/etc/pkg/GhostBSD.conf` file accordingly. It uses `libappindicator` to provide a system tray icon and menu.
It hasn't been decided whether to make this a stand-alone program or to incorporate the key components into update-station. It was written to give Eric Turgeon a hand. :-)

## Features

- Allows selection of different GhostBSD repositories.
- Updates the `/etc/pkg/GhostBSD.conf` file with the selected repository.
- Creates a backup of the existing configuration file before making changes.
- Provides user feedback through message dialogs.

## Requirements

- Python 3
- `gtk3` package
- `libappindicator` package

## Installation

### Install Dependencies

#### On GhostBSD:

```
sudo pkg install gtk3 libappindicator
```

### Clone the Repository

```
git clone https://github.com/repent-or-perish/set-pkg-repository.git
cd set-pkg-repository
```

## Usage

Run the script with elevated permissions to allow it to modify the `/etc/pkg/GhostBSD.conf` file:

```
sudo python3 set_pkg_repo.py
```

### Functionality

- The application will add a system tray icon.
- Click on the icon to open the menu.
- Select the desired repository from the menu.
- The application will update the `/etc/pkg/GhostBSD.conf` file and create a backup of the existing configuration.
- A message dialog will confirm the update or display an error message if something goes wrong.

## Configuration File

The `/etc/pkg/GhostBSD.conf` file will be updated with the selected repository URLs. The program ensures both the `latest` and `base` URLs are set for the selected repository.

## Repositories

The following repositories are available for selection:

- GhostBSD_Unstable
- GhostBSD_CA
- GhostBSD
- GhostBSD_FR
- GhostBSD_NO
- GhostBSD_ZA

Each repository has paired `latest` and `base` URLs.

## Files Used for Reference

- `/etc/pkg/GhostBSD.conf`: The main configuration file that will be updated by the application.
- `/etc/pkg/GhostBSD.conf.bak`: A backup of the existing configuration file before any changes are made.
- `/usr/local/etc/pkg/repos`: The directory containing the repository configuration files.
