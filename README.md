# Master

Generates deterministic passwords for services.


## Install

    pip install master


## Usage

```
$ master --help
Usage: master [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get      Gets the deterministic password for SERVICE.
  ls       Lists all stored services.
  rm       Removes SERVICE from the stored list.
  version  Shows the version.
```


## Environment variables

| Name                | Default                       |
| ------------------- | ----------------------------- |
| `MASTER_LIST`       | `~/.config/master/list.txt`   |
| `MASTER_USERNAME`   | (None) [1]                    |
| `MASTER_PASSWORD`   | (None) [1]                    |
| `MASTER_SEPARATOR`  | `-`                           |
| `MASTER_LENGTH`     | `6`                           |
| `MASTER_CHUNKS`     | `6`                           |

**Note [1]:** If you don't set the `MASTER_USERNAME` or the `MASTER_PASSWORD` you will
be prompted on them.
