#!/usr/bin/env python3
# A simple wrapper script to run purge-job specific commands in a Thoth
# deployment.

case "${THOTH_PURGE_JOB_SUBCOMMAND}" in
    'adviser')
        exec /opt/app-root/bin/python3 app.py adviser
        ;;
    'package-extract')
        exec /opt/app-root/bin/python3 app.py package-extract
        ;;
    'solver')
        exec /opt/app-root/bin/python3 app.py solver
        ;;
    *)
        echo "Application configuration error - bad purge-job subcommand specified." >&2
        exit 1
        ;;
esac
