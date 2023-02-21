# Master

Generates deterministic passwords for services.

This uses a combination of `username + password + service + counter`
to generate the same password, over and over again, thus eliminating
the need to store, maintain and back up other generated passwords.

The username and password are not stored anywhere. A service name
list is kept under the file `~/.config/master/list.txt` (or whatever
`MASTER_LIST` points to) purely for autocompletion (which will be
added later).


## Install

    pip install masterpass

Yes. The package is called `masterpass` but the binary is called
`master`.


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

**Note [1]:** If you don't set the `MASTER_USERNAME` or the
`MASTER_PASSWORD` you will be prompted for them.
