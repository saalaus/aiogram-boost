import shutil
from pathlib import Path

import click


def copy(file: Path, target: Path) -> Path:
    "copy file from <file> to <target> return new file path"
    return Path(shutil.copy(file, target))


def create_folder(path: Path) -> Path:
    "Create new folder from <path> return <path>"
    click.echo(f"Create fold: {path}")
    path.mkdir()
    return path


def create_empty_file(path: Path) -> Path:
    "Create new empty file from <path>. Return <path>"
    click.echo(f"Create file {path}")
    with open(path, "a"):
        pass
    return path


def copy_file_from_template(template_file_name: str, path: Path,
                            new_name: "str | None" = None) -> Path:
    """
    Copy file from <package_path>/template/<template_file_name>
    to <path> and rename his if <new_name> is not None
    return: Path to new file
    """
    template_file = Path(__file__).parents[0] / "template" / template_file_name

    file_name = new_name if new_name else template_file_name

    click.echo(f"Create file {path/file_name}")

    copy_path = copy(template_file, path)

    if new_name:
        copy_path.rename(copy_path.parents[0] / new_name)

    return copy_path.parents[0] / new_name if new_name else copy_path


def format_file(file_path: Path, **format_options: "str | bool | int") -> None:
    "format file from <file_path> with <format_options>"
    with open(file_path, "a+") as f:
        f.seek(0)
        text = f.read()
        text = text.format(**format_options)
        f.seek(0)
        f.truncate()
        f.write(text)


def create_requirements_file(path: Path, use_redis: bool, use_db: bool) -> Path:
    path = copy_file_from_template("requirements.txt", path)
    optional_requirements = []
    if use_db:
        optional_requirements.append("sqlalchemy")
    if use_redis:
        optional_requirements.append("aioredis")
    format_file(path, optional_dependencies="\n".join(optional_requirements))
    return path


def create_env_file(path: Path, use_redis: bool) -> Path:
    path = copy_file_from_template("env.env", path, ".env")
    format_file(path, use_redis=use_redis)
    return path


def create_all_project_file(
        path: Path,
        use_redis: bool = False,
        use_db: bool = False,
        create_venv: bool = False,
        parse_mode: bool = False) -> None:
    bot_folder = create_folder(path / "tgbot")
    handlers_folder = create_folder(bot_folder / "handlers")
    filters_folder = create_folder(bot_folder / "filters")
    middlewares_folder = create_folder(bot_folder / "middlewares")
    keyboards_folder = create_folder(bot_folder / "keyboards")
    misc_folder = create_folder(bot_folder / "misc")
    services_folder = create_folder(bot_folder / "services")

    create_empty_file(bot_folder / "__init__.py")
    create_empty_file(handlers_folder / "__init__.py")
    create_empty_file(filters_folder / "__init__.py")
    create_empty_file(middlewares_folder / "__init__.py")
    create_empty_file(keyboards_folder / "__init__.py")
    create_empty_file(misc_folder / "__init__.py")
    create_empty_file(services_folder / "__init__.py")

    create_env_file(path, use_redis)
    create_requirements_file(path, use_redis, use_db)

    bot = copy_file_from_template("bot.py", path)
    format_file(bot,
                parse_mode=parse_mode)
    copy_file_from_template("config.py", bot_folder)
    


def format_with_replace(file_path: Path, replace_dict: dict) -> None:
    "format file from <file_path> with <replace_dict>"
    with open(file_path, "a+") as f:
        f.seek(0)
        text = f.read()
        for key, value in replace_dict.items():
            text = text.replace(key, value)
        f.seek(0)
        f.truncate()
        f.write(text)


def make_handler(path: Path, name: str, type: str) -> Path:
    "Create new handler from <path> with <name> and type=<type>"
    handler = copy_file_from_template(
        "handler.py", path / "tgbot" / "handlers",
        f"{name}.py"
    )
    format_file(handler, name=name, type=type, type_title=type.title())
    format_with_replace(path / "bot.py", {
        "# extended imports": f"from tgbot.handlers.{name} "
                              f"import register_{name}",
        "# extended handlers": f"register_{name}(dp)"
                               f"    # extended handlers",
    })
    return handler


def make_command(path: Path, name: str, description: str) -> Path:
    bot = path / "bot.py"
    format_with_replace(bot, {
        "# extended commands": f"BotCommand(\"{name}\", \"{description}\"),\n"
                               "        # extended commands",
    })
    return bot

def make_state(path: Path, name: str) -> Path:
    state_fold = path / "tgbot" / "misc"
    file = copy_file_from_template("state.py", state_fold, f"{name}_state.py")
    format_file(file, name=name.capitalize())
    return file


def make_keyboard(path: Path, inline: bool, name: str) -> Path:
    keyboard_fold = path / "tgbot" / "keyboards"
    if inline:
        type = "inline"
        btn = "inline"
    else:
        type = "reply"
        btn = ""
    file = copy_file_from_template("keyboard.py", keyboard_fold,
                                   f"{name}_{type}.py")
    format_file(file, name=name, btn_type=btn, type=type.capitalize())
    return file