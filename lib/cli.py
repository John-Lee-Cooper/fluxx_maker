#!/usr/bin/env python

""" Command Line Interface functions """

from typing import Callable, Any

import typer


def run(function: Callable[..., Any]) -> Any:
    """ TODO """
    app = typer.Typer(add_completion=False)
    command = app.command()
    command(function)
    app()
