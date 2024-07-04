import os

from dynaconf import Dynaconf

current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    root_path=current_directory,
    settings_files=["settings.toml", ".secrets.toml"],
    environments=[
        "testing",
        "development",
        "homologation",
        "staging",
        "production",
    ],
    envvar_prefix="VPO_APPLICATION",
    env_switcher="API_ENV",
    merge_enable=True,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
