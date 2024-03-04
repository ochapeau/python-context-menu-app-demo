#!/bin/bash
# Uninstall all the files installed by the pkg
# Note: Run with admin right (e.g. sudo)
# -- Loading .env variables --
set -o allexport
source .env set
set +o allexport
# -- Removing files --
rm -rfv /Applications/"$APP_NAME" # App
rm -rfv ~/Library/Services/"$WORKFLOW_NAME" # Workflow (Quick Action)
rm -rfv ~/Library/Logs/ResizeImagesContextMenu # Logs
# -- Forgetting pkgs id --
pkgutil --forget "$ID_APP" # App
pkgutil --forget "$ID_WORKFLOW" # Workflow (Quick Action)
