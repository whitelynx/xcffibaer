xcffibär
========

A themeable status bar written in Python, using `xcffib`.


Prerequisites
-------------

Ensure you have [pyenv](https://github.com/pyenv/pyenv) and
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) installed. (preferably using
[pyenv-installer](https://github.com/pyenv/pyenv-installer))

You will also need [libstatgrab](http://www.i-scream.org/libstatgrab).


Setup
-----

From within the `xcffibaer` directory, run:

```bash
./bootstrap.sh
```


Running
-------

From within the `xcffibaer` directory, run:

```bash
python xcffibaer
```


In order to be able to run `xcffibaer` from anywhere (e.g., from your `~.config/i3/config` or a `systemd` job) you'll
want to use [the runner script](scripts/xcffibaer); copy it into your `PATH` (`~/.local/bin` is probably a good spot)
and modify the paths in the script to match your environment. Then you should be able to run it by executing
`xcffibaer`.
