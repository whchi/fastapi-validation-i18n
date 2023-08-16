import os
import shutil
import sys


def export_locale_folder(target_path: str) -> None:
    working_dir = os.getcwd()

    locale_path = os.path.join(
        os.path.join(os.path.dirname(os.path.dirname(__file__))),
        'locale',
    )

    target_locale_path = os.path.join(working_dir, target_path)

    if not os.path.exists(target_locale_path):
        os.makedirs(target_locale_path, exist_ok=False)
    else:
        print(f'The target path {target_locale_path} already exists.')
        return
    shutil.copytree(locale_path, target_locale_path, dirs_exist_ok=True)
    print('Successfully exported "locale" folder to:', target_locale_path)


def main() -> None:
    if len(sys.argv) != 2:
        print('missing <target_path>')
    else:
        export_locale_folder(sys.argv[1])
