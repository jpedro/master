# Master

![Strong password](https://raw.githubusercontent.com/jpedro/master/master/.github/assets/password.jpeg)

Deterministic passwords for everyone.

This uses a sha256 hashed combination of `username + password + service`
to generate the same password, over and over again, thus eliminating
the need to store, maintain and back up other generated passwords.

The username and password **are not stored anywhere**.

The used service name list is kept under the file `~/.config/master/list.txt`
(or whatever `MASTER_LIST` points to) *purely for autocompletion*,
which will be added later.


## Install

    pip install masterpass

Yes, yes. The package is called `masterpass` but the binary is called
`master`. To be fixed after [#2582](https://github.com/pypi/support/issues/2582)
is resolved.


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
