# Quotator

## How to use quotator

1. Clone and unzip the repo
2. Create an alias if you want a shorter access to the script

	>>> cd ~
	>>> sudo nano .bash_profile

	alias quotator="python /path/to/quotator.py"

3. Run `quotator --help` for seeing all the available functions and options

```
usage: quotator.py [-h] [-u UNIT] path

Get 3D print price quotations for a file or directory

positional arguments:
  path                  file or directory to be quoted

optional arguments:
  -h, --help            show this help message and exit
  -u UNIT, --unit UNIT  mesh units of the parts to be quoted (mm, cm or in)

```

## License

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.