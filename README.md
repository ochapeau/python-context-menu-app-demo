# Resize Images Context Menu App
## Description
This repository contains a demo application to add actions to the context menu (right-click menu on macOS Finder or Windows explorer).

The application takes paths as inputs and creates a copy of images resized by a factor of 0.5 by default. Resizing the images is made using the [Pillow](https://pypi.org/project/pillow/) package.

**Usage**:

The CLI arguments are the resizing factor (0.5 by default) and the paths of the files like in the following command:
```sh
ResizeImagesContextMenu [-h] [-f FACTOR] files [files ...]
```
Once installed, it can be used via the context menu (right-click menu. On macOS the action is available in the "Quick Actions" Finder menu, on windows it is available in the Explorer menu, like on the following pictures:

On macOS:
[macOS picture](./readme_images/macOS_screen.png)

On Windows:
[macOS picture](./readme_images/macOS_screen.png)

**It features**:
- Logging with platform detection to put the logs in an appropriate folder
- Checks the filetype using MIME types to detect images
- Checks if an image with the expected filename exists and if so checks if it has the expected dimensions after resizing in order to avoid resizing images if not needed

## Building on macOS
### Building the application
The macOS app is built using the package [py2app](https://py2app.readthedocs.io/en/latest/). The script to build the application is [build_app.sh](./build_macos/build_app.sh). It creates a python [virtualenv](https://virtualenv.pypa.io/en/latest/) and installs the depencies from [macos.txt](macos.txt). Then it builds the application by using a [setup.py](./build_macos/setup.py) file, and it deletes the virtualenv.

### Building the pkg (installer)
The script to build the pkg is [build_pkg.sh](./build_macos/build_pkg.sh). It generates two pkg files, one for the app and one for the context menu action. Then using the [distribution.xml](./build_macos/pkg/distribution.xml) file it creates the complete pkg file. The built pkg file is then available in the `builds` directory.

### Building all
To make the process of building the application

### Uninstalling the application on macOS
The script [uninstall.sh](./build_macos/uninstall.sh) is available to uninstall all the installed files by the pkg and the logs created by the app. It uses the command `pkgutil --forget` to delete the package ids created at the installation of the app.

Note: It must be run with administrative privileges (e.g. sudo)

Note: The [.env](./build_macos/.env) file contains shared variables to both [build_pkg.sh](./build_macos/build_pkg.sh) and [uninstall.sh](./build_macos/uninstall.sh) scripts, therefore is useful to reduce human errors while editing the scripts. 

## Building on Windows
### Building the application
The windows app is built using the package [py2installer](https://pyinstaller.org/en/stable/).