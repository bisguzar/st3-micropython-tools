!['Logo'](https://raw.githubusercontent.com/bisguzar/st3-micropython-tools/master/images/logo2.png)

# SublimeText MicroPython Tools

MicroPython board tools for Sublime Text 3. You can pull, push and remove files from/to your board which installed MicroPython. 

## Getting Started

You need a Sublime Text (>3). And [PackageControl](http://packagecontrol.io/) if you want install plugin easily.

### Installing

You can install plugin using by PackageControl (suggested) or manually.

#### Install with PackageControl

Launch SublimeText and open command palette (`CTRL`+`SHIFT`+`P`). Type `install` and select *Package Control: Install Package* option. 

Now you can type 'micropython'. You should see 'MicroPython Tools'. Select it and wait for installation.

#### Manual Installation

##### with git

You can install from github if you want, although Package Control automates
just that. Go to your `Packages` subdirectory under ST2's data directory:

* Windows: `%APPDATA%\Sublime Text 2`
* OS X: `~/Library/Application Support/Sublime Text 2`
* Linux: `~/.config/sublime-text-2`
* Portable Installation: `Sublime Text 2/Data`

Then clone this repository:

    git clone https://github.com/bisguzar/st3-micropython-tools.git

##### alternative

[Download](https://github.com/bisguzar/st3-micropython-tools/archive/master.zip)
the plugin as a zip. Copy the *st3-micropython-tools-master* directory to its location
(see prior section).

### How to Use

The best way for using this plugin is command palette. Command Palette is gem for Sublime Text. Just open command palette (`CTRL`+`SHIFT`+`P`) and type MicroPython. You can see all of options on there. Operations will run active file. For example when you select upload file option the active file will push to board.

![Command Palette](https://raw.githubusercontent.com/bisguzar/st3-micropython-tools/master/images/commandpalette.gif)

## Contributing

If you find any problem while using MicroPython Tools, create an [issue](https://github.com/bisguzar/st3-micropython-tools/issues/new) or fork this project and fix it yourself. Then sent a pull request. It will better 😍.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/bisguzar/st3-micropython-tools/tags). 

## TODO

- [ ] uPiP Installer Asistant
- [ ] Bootloader Writer

## Authors

* **Bugra ISGUZAR** - *Initial work* - [Bisguzar](https://github.com/bisguzar)

See also the list of [contributors](https://github.com/bisguzar/st3-micropython-tools/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [AMPY](https://github.com/adafruit/ampy)
* [PySerial](https://github.com/pyserial/pyserial)
