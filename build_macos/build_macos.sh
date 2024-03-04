#!/bin/bash
# -- Loading .env variables --
set -o allexport
source .env set
set +o allexport

# -- Building the App --
# Variables for building the app
APP_BUILD_DIR=ResizeImagesContextMenu/Applications

# Variables for building the pkg
PKG_CONTENT_DIR=../ResizeImagesContextMenu # From the "pkg" directory
BUILDS_DIR=../../builds # From the "pkg" directory
PKG_NAME=ResizeImagesContextMenuInstaller.pkg


# -- Building the app --
# Creating venv
python -m venv .venv
# Activating the venv, .venv does not exists when using shellcheck,
# thus using a directive
# shellcheck disable=SC1091
source .venv/bin/activate
# Installing the dependencies in the venv
pip install -r ../macos.txt
# Building the app
python setup.py py2app
# Desactivating the venv
deactivate

# -- Moving and cleaning the app --
# Moving the app to the installer directory
SRC=dist/$APP_NAME
DEST=$APP_BUILD_DIR/$APP_NAME
mv -v "$SRC" "$DEST"
echo "Moved $SRC to $DEST"
# Cleaning up build directories
rm -rfv build dist .venv

# -- Building the pkg --
# Locate in the "pkg" dir
cd pkg/ || (echo "No pkg dir - exiting" && exit)
# Creating component packages
pkgbuild --root $PKG_CONTENT_DIR/Applications --install-location /Applications --identifier "$ID_APP" ResizeImagesAppDemo.pkg
pkgbuild --root $PKG_CONTENT_DIR/Library/Services --install-location ~/Library/Services --identifier "$ID_WORKFLOW" ResizeImagesWorkFlowDemo.pkg
# Creating the final pkg
productbuild --distribution distribution.xml --package-path . $PKG_NAME
# Making the builds dir if it does not exists
[ ! -d $BUILDS_DIR ] && mkdir $BUILDS_DIR
# Moving the built pkg to the builds dir
mv -v $PKG_NAME $BUILDS_DIR
# Cleaning intermediate pkgs
rm -rfv -- *.pkg
# Go back
cd ..

# -- Cleaning the app --
# Cleaning the APP_INSTALLER_DIR
OLD_APP=${APP_BUILD_DIR:?}/$APP_NAME
rm -rf "$OLD_APP" && echo "Cleaned $OLD_APP"
