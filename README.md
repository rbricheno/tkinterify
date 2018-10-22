# tkinterify
An easy way to turn a CLI implemented with click into a GUI using tkinter.

This allows you to type function names into a text input box, and have the output appear when you click "Run". Your commands must first be added to a group to use this.

```
import click
from tkinterify import tkinterify


# You must add your commands to a group in order to use tkinterify
@click.group()
def cli():
    pass


@click.command()
def my_function():
    print("My Stuff")


@click.command()
def my_other_function():
    print("More Things")


cli.add_command(my_function)
cli.add_command(my_other_function)

# Pass the group, and optionally app_name="my app"
# tkinterify(cli, app_name="My functions")
tkinterify(cli)
```
