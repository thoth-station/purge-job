#!/usr/bin/env python3
# thoth-purge-job
# Copyright(C) 2021 Red Hat, Inc.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Purging old data out of a Thoth deployment."""

import logging
from typing import Optional

import click
from dateutil.parser import parse
from thoth.common import init_logging
from thoth.common import __version__ as thoth_common_version
from thoth.storages import GraphDatabase
from thoth.storages import __version__ as thoth_storages_version

__version__ = "0.0.0"
__component_version__ = f"{__version__}+storages.{thoth_storages_version}.common.{thoth_common_version}"

init_logging()
_LOGGER = logging.getLogger("thoth.purge")


def _print_version(ctx: click.Context, _, value: str):
    """Print purge-job version and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo(__component_version__)
    ctx.exit()


@click.group()
@click.pass_context
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    envvar="THOTH_PURGE_DEBUG",
    help="Be verbose about what's going on.",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print purge-job version and exit.",
)
def cli(ctx=None, verbose=False) -> None:
    """Thoth purge-job command line interface."""
    if ctx:
        ctx.auto_envvar_prefix = "THOTH_PURGE"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)

    _LOGGER.debug("Debug mode is on")
    _LOGGER.info("Component version: %s", __component_version__)


@cli.command()
@click.pass_context
@click.option(
    "--os-name",
    "-o",
    type=str,
    metavar="OS_NAME",
    envvar="THOTH_PURGE_OPERATING_SYSTEM_NAME",
    required=True,
    help="Purge specific operating system name data",
)
@click.option(
    "--os-version",
    "-v",
    type=str,
    metavar="OS_VERSION",
    envvar="THOTH_PURGE_OPERATING_SYSTEM_VERSION",
    required=True,
    help="Purge specific operating system version data",
)
@click.option(
    "--python-version",
    "-p",
    type=str,
    metavar="PY_VERSION",
    envvar="THOTH_PURGE_PYTHON_VERSION",
    required=True,
    help="Purge specific Python version data",
)
def solver(os_name: str, os_version: str, python_version: str) -> None:
    """Purge solver data."""
    graph = GraphDatabase()
    graph.connect()
    result = graph.delete_solved(os_name=os_name, os_version=os_version, python_version=python_version)
    _LOGGER.info("Removed %d solver entries from the database", result)


@cli.command()
@click.pass_context
@click.option(
    "--adviser-version",
    type=str,
    metavar="VERSION",
    envvar="THOTH_PURGE_ADVISER_VERSION",
    help="Purge specific adviser results corresponding to a specific adviser version",
)
@click.option(
    "--end-datetime",
    "end",
    type=str,
    metavar="DATETIME",
    envvar="THOTH_PURGE_ADVISER_END_DATETIME",
    help="Purge specific adviser results older than datetime provided.",
)
def adviser(end: Optional[str], adviser_version: Optional[str]) -> None:
    """Purge adviser data."""
    graph = GraphDatabase()
    graph.connect()
    result = graph.delete_adviser_run(end_datetime=parse(end) if end else None, adviser_version=adviser_version or None)
    _LOGGER.info("Removed %d adviser entries from the database", result)


@cli.command()
@click.pass_context
@click.option(
    "--package-extract-version",
    type=str,
    metavar="VERSION",
    envvar="THOTH_PURGE_PACKAGE_EXTRACT_VERSION",
    help="Purge specific package-extract results corresponding to a specific package-extract version",
)
@click.option(
    "--end-datetime",
    "end",
    type=str,
    metavar="DATETIME",
    envvar="THOTH_PURGE_PACKAGE_EXTRACT_END_DATETIME",
    help="Purge specific package-extract results older than datetime provided.",
)
def package_extract(end: Optional[str], package_extract_version: Optional[str]) -> None:
    """Purge package-extract data."""
    graph = GraphDatabase()
    graph.connect()
    result = graph.delete_package_extract_run(
        end_datetime=parse(end) if end else None, package_extract_version=package_extract_version or None
    )
    _LOGGER.info("Removed %d package-extract entries from the database", result)


__name__ == "__main__" and cli()
