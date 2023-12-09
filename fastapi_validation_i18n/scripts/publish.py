import os
import shutil
from typing import Annotated, Union

import typer

SUPPORTED_LOCALES = ['zh-TW', 'en-US', 'ja-JP']

app = typer.Typer()


@app.command(name='export')
def export_locale_folder(
    target_path: Annotated[str,
                           typer.Argument(
                               help='destination path to export to')] = 'locale',
    locale: Annotated[Union[str, None],
                      typer.Option(help='specific locale to export')] = None
) -> None:
    """
    Exports either the entire locale directory or a specific locale's message.json file to the given destination path.

    Args:
    target_path: The destination directory where the locale data will be copied.
    locale: The specific locale to export or None to export all locales.
    """
    working_dir = os.getcwd()
    locale_path = os.path.join(
        os.path.join(os.path.dirname(os.path.dirname(__file__))),
        'locale',
    )

    target_locale_path = os.path.join(working_dir, target_path)

    if locale:
        if locale not in SUPPORTED_LOCALES:
            typer.secho(
                f'Locale {locale} is not supported. Supported locales are:',
                fg=typer.colors.RED,
            )
            typer.secho(SUPPORTED_LOCALES, fg=typer.colors.RED)
            return

        target_locale_path = os.path.join(target_locale_path, locale)

    if not os.path.exists(target_locale_path):
        os.makedirs(target_locale_path)
    else:
        typer.secho(
            f'Destination path {target_locale_path} already exists. '
            'Please remove it or choose a different destination path.',
            fg=typer.colors.RED,
        )
        return

    if locale:
        locale_path = os.path.join(locale_path, locale)

        json_file = os.path.join(locale_path, 'message.json')

        if any([not os.path.exists(locale_path), not os.path.isfile(json_file)]):
            typer.secho(
                f"Locale '{locale}' does not exist or it does not contain a 'message.json' file.",
                fg=typer.colors.RED,
            )
            return
        shutil.copy2(json_file, os.path.join(target_locale_path, 'message.json'))
        typer.secho(
            f'Successfully exported {locale}/message.json to {target_locale_path}',
            fg=typer.colors.GREEN,
        )
    else:
        shutil.copytree(locale_path, target_locale_path, dirs_exist_ok=True)
        typer.secho(
            f'Successfully exported "locale" folder to {target_locale_path}',
            fg=typer.colors.GREEN,
        )


def main() -> None:
    typer.run(export_locale_folder)
