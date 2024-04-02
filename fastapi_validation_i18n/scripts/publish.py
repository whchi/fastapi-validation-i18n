import argparse
import os
import shutil

SUPPORTED_LOCALES = ['zh-TW', 'en-US', 'ja-JP']


def export_locale_folder(target_path: str, locale: str | None = None) -> None:
    working_dir = os.getcwd()
    locale_path = os.path.join(
        os.path.join(os.path.dirname(os.path.dirname(__file__))),
        'locales',
    )

    target_locale_path = os.path.join(working_dir, target_path)

    if locale:
        if locale not in SUPPORTED_LOCALES:
            print(f'Locale {locale} is not supported. Supported locales are:')
            print(SUPPORTED_LOCALES)
            return

        target_locale_path = os.path.join(target_locale_path, locale)

    if not os.path.exists(target_locale_path):
        os.makedirs(target_locale_path)
    else:
        print(f'Destination path {target_locale_path} already exists. '
              'Please remove it or choose a different destination path.')
        return

    if locale:
        locale_path = os.path.join(locale_path, locale)

        json_file = os.path.join(locale_path, 'message.json')

        if any([not os.path.exists(locale_path), not os.path.isfile(json_file)]):
            print(
                f"Locale '{locale}' does not exist or it does not contain a 'message.json' file."
            )
            return
        shutil.copy2(json_file, os.path.join(target_locale_path, 'message.json'))
        print(f'Successfully exported {locale}/message.json to {target_locale_path}')
    else:
        shutil.copytree(locale_path, target_locale_path, dirs_exist_ok=True)
        print(f'Successfully exported "locale" folder to {target_locale_path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Export locales folder.')
    parser.add_argument(
        'target_path',
        help='destination path to export to',
        type=str,
    )
    parser.add_argument('--locale', default=None, help='specific locale to export')
    args = parser.parse_args()

    export_locale_folder(args.target_path, args.locale)


if __name__ == '__main__':
    main()
