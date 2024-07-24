from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel
from tomlkit import document, dump, load  # type: ignore

if TYPE_CHECKING:
    from tomlkit import TOMLDocument


# Base classes
class ConfigBase(BaseModel):
    pass


class KeyBase(BaseModel):
    pass


class IntervalBase(BaseModel):
    pass


# Key classes
class MoveKey(KeyBase):
    forward: "str" = "w"
    backward: "str" = "s"
    left: "str" = "a"
    right: "str" = "d"


class CameraKey(KeyBase):
    up: "str" = "i"
    down: "str" = "k"
    left: "str" = "j"
    right: "str" = "l"


class InteractionKey(KeyBase):
    ashes_of_war: "str" = "f"
    map: "str" = "m"
    sites_of_grace: "str" = "f"
    confirm: "str" = "e"


class Key(ConfigBase):
    move: "MoveKey" = MoveKey()
    camera: "CameraKey" = CameraKey()
    interaction: "InteractionKey" = InteractionKey()


# Interval classes
class ActionInterval(IntervalBase):
    move_forward_from_site_of_grace: "float" = 2.65
    move_forward_to_destination: "float" = 2.3
    rotate_camera_to_left: "float" = 0.24
    ashes_of_war: "float" = 5.0


class LoadingInterval(IntervalBase):
    loading: "float" = 6.0


class FixedInterval(IntervalBase):
    key_press: "float" = 0.15
    map: "float" = 0.4
    sites_of_grace: "float" = 0.4
    travel: "float" = 0.4


class Interval(ConfigBase):
    action: "ActionInterval" = ActionInterval()
    loading: "LoadingInterval" = LoadingInterval()
    fixed: "FixedInterval" = FixedInterval()


# Config class
class Config(BaseModel):
    key: "Key" = Key()
    interval: "Interval" = Interval()

    _toml: "TOMLDocument | None" = None

    @classmethod
    def load(cls) -> "Config":
        path = Path("config.toml")
        config = cls()
        print(config)
        if not path.exists():
            config._toml = document()
        else:
            with path.open("r", encoding="utf-8") as f:
                toml = load(f)
            config.__dict__.update(**toml)
            config._toml = toml
        return config

    def save(self) -> "None":
        self._toml.update(self.model_dump())  # type: ignore
        path = Path("config.toml")
        with path.open("w") as f:
            dump(self._toml, f)  # type: ignore


if __name__ == "__main__":
    config = Config.load()
    print(config.model_dump())
    config.save()
