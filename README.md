# `blync`

Control your Embrava BlyncLight from the command-line!

## Usage

Use the `blync` utility to directly control your Embrava BlyncLight:


```console
$ blync -R        # turn the light on with red color and leave it on
$ blync --off     # turn the light off
$ blync -RG --dim # turn the light on with yellow color and dim
$ blync -RBG      # turn the light on with white color
```

Colors can be specified by values between 0 and 255 using the lower-case
color options or using the upper-case full value options.


```console
$ blync -r 127                # half intensity red
$ blync -r 255                # full intensity red
$ blync -R                    # also full intensity red
$ blync -r 255 -b 255 -g 255  # full intensity white
$ blync -RBG                  # full intensity white
```


If that's not enough fun, there are three builtin color modes:
`fli`, `throbber`, and `rainbow`. All modes continue until the
user terminates with a Control-C or platform equivalent.


```console
$ blync fli
$ blync throbber
$ blync rainbow
```

## Installation


```console
$ python3 -m pip install blynclight
$ python3 -m pip install git+https://github.com/JnyJny/blynclight.git # latest
```

This module depends on
[hidapi](https://github.com/trezor/cython-hidapi), which supports
Windows, Linux, FreeBSD and MacOS via a Cython module.

**Usage**:

```console
$ blync [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-l, --light-id INTEGER`: Light identifier  [default: 0]
* `-r, --red INTEGER`: Red color value range: 0 - 255  [default: 0]
* `-b, --blue INTEGER`: Blue color value range: 0 - 255  [default: 0]
* `-g, --green INTEGER`: Green color value range: 0 - 255  [default: 0]
* `-R, --RED`: Full value red [255]
* `-B, --BLUE`: Full value blue [255]
* `-G, --GREEN`: Full value green [255]
* `-o, --off / -n, --on`: Turn the light off/on.  [default: False]
* `-d, --dim`: Toggle bright/dim mode.  [default: False]
* `-f, --flash`: Enable flash mode.
* `-p, --play INTEGER`: Select song: 1-15
* `--repeat`: Repeat the selected song.  [default: False]
* `--volume INTEGER`: Set the volume: 1-10  [default: 5]
* `-a, --list-available`
* `-v, --verbose`
* `-V, --version`
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `fli`: Flash Light Impressively.
* `rainbow`: BlyncLights Love Rainbows.
* `throbber`: BlyncLight Intensifies.
* `udev-rules`: Generate a Linux udev rules file.

## `blync fli`

Flash Light Impressively.

This mode cycles light color red, blue, green and then repeats. The
user can specify the interval between color changes and the intesity
of the colors. Color values specified on the command-line are ignored.

## Examples


```console
$ blync fli -n 1      # one second between color changes
$ blync fli -i 128    # light intensity is half as bright
```

This mode runs until the user interrupts.

**Usage**:

```console
$ blync fli [OPTIONS]
```

**Options**:

* `-n, --interval FLOAT`: Seconds between flashes.  [default: 0.1]
* `-i, --intensity INTEGER`: Integer range: 0 - 255  [default: 255]
* `--help`: Show this message and exit.

## `blync rainbow`

BlyncLights Love Rainbows.

Smoothly transition the color of the light using a rainbow sequence.
The user can slow the speed of the color cycling by adding more
--slow options to the command line:

## Examples


```console
$ blync rainbow -s   # slow cycling by 0.1 seconds
$ blync rainbow -ss  # slow cycling by 0.15 seconds
```

This mode runs until the user interrupts.

**Usage**:

```console
$ blync rainbow [OPTIONS]
```

**Options**:

* `-s, --slow`: Increase color cycle interval by 0.1 seconds.
* `--help`: Show this message and exit.

## `blync throbber`

BlyncLight Intensifies.

This mode increases the intensity of the light color starting with
the specified red, green and blue values and ramping the color
intensity up and down and repeating. The user can increase the rate
of ramp by adding more -f options to the command line:

## Examples


```console
$ blync throbber -f   # a little faster
$ blync throbber -ff  # a little more faster
$ blync -G throbber   # throb with a green color
```

This mode runs until the user interrupts.

**Usage**:

```console
$ blync throbber [OPTIONS]
```

**Options**:

* `-f, --faster`: Increases speed.
* `--help`: Show this message and exit.

## `blync udev-rules`

Generate a Linux udev rules file.

Linux uses the udev subsystem to manage USB devices as they are
plugged and unplugged. By default, only the root user has read and
write access. The rules generated grant read/write access to all users
for all known Embrava device vendor ids. Modify the rules to suit your
particular environment.

Example:


```
$ blync udev-rules -o 99-blynclight.rules
$ sudo cp 99-blynclight.rules /etc/udev/rules.d
$ sudo udevadm control -R
# unplug/plug USB devices
```

**Usage**:

```console
$ blync udev-rules [OPTIONS]
```

**Options**:

* `-o, --output PATH`: Save udev rules to this file.
* `--help`: Show this message and exit.
