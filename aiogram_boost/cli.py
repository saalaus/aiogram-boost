from pathlib import Path

import click
from aiogram_boost.create import create_all_project_file, create_folder, make_command, make_handler, make_keyboard, make_state
from aiogram_boost.utils import is_dir_empty


@click.group
def basic_group() -> None:
    """Fastest aiogram bots develop"""
    pass


@basic_group.command
@click.argument("path")
def startproject(path: Path) -> None:
    """Starting new project"""
    path = Path(path)

    if path.exists():
        if path.is_dir():
            if not is_dir_empty(path):
                click.echo(f"{path} directory is not empty")
                return
        else:
            click.echo(f"{path} is not a directory")
            return

    parse_mode = click.prompt("Choose parse mode",
                              type=click.Choice(
                                  ["HTML", "Markdowv", "MarkdownV2"],
                                  case_sensitive=False
                              ),
                              default="HTML")
    use_redis = click.confirm("Use Redis?", default=False, show_default=True)
    use_db = click.confirm("Use db with sqlalchemy?", default=False,
                           show_default=True)
    create_venv = click.confirm("Create new virtualenv?", default=False,
                                show_default=True)
    

    if not path.exists():
        create_folder(path)

    click.echo(f"OK! Configuratio: path={path.absolute()}, {parse_mode=}, "
               f"{use_redis=}, {use_db=}, {create_venv=}")

    create_all_project_file(path, use_redis, use_db, create_venv, parse_mode)


@basic_group.group
def new() -> None:
    """create new object"""
    pass


@new.command
@click.argument("name")
@click.argument("path", type=click.Path(), default=".")
@click.option("--type", "-t", default="message")
def handler(name: str, path: Path, type: str) -> None:
    """create new handler"""
    path = Path(path)
    file = path / "tgbot" / "handlers" / f"{name}.py"
    if file.exists():
        click.echo(f"{name} already exists")
        return
    make_handler(path, name, type)


@new.command
@click.argument("name")
@click.argument("path", type=click.Path(), default=".")
def state(name: str, path: Path) -> None:
    """create new state manager"""
    path = Path(path)
    file = path / "tgbot" / "misc" / f"{name}_state.py"
    if file.exists():
        click.echo(f"{name} already exists")
        return
    
    make_state(path, name)


@new.command
def model() -> None:
    """create new model"""
    click.echo("model")


@new.command
def filter() -> None:
    """create new filter"""
    click.echo("filter")


@new.command
@click.option("--from-template", "-template",
              help="Create new middleware from template")
@click.option("--list", "-l", is_flag=True,
              help="Print list middlewares templates")
def middleware(list: bool, from_template: str) -> None:
    """create new middleware"""
    click.echo(list)


@new.command
@click.argument("name")
@click.option("--inline", is_flag=True)
@click.argument("path", type=click.Path(), default=".")
def keyboard(path: Path, inline: bool, name: str) -> None:
    """create new keyboard file"""
    path = Path(path)
    
    make_keyboard(path, inline, name)
    
    
@new.command
@click.argument("name")
@click.argument("description")
@click.argument("path", type=click.Path(), default=".")
def command(path: Path, name: str, description: str) -> None:
    """create new command"""
    path = Path(path)
    click.echo(f"New command with {name=} {description=}")
    make_command(path, name, description)


if __name__ == "__main__":
    basic_group()
