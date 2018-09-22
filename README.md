# Quotator

## How to install quotator

Quotator is in prototyping stage and it is run as a script from the command line and uses system Python and libraries.

1. Clone and unzip the repo
2. Install the required packages

		pip install trimesh

3. Create an alias if you want a shorter access to the script


		cd ~
		sudo nano .bash_profile

		alias quotator="python /path/to/quotator.py"

3. Run `quotator --help` for seeing if the script is working. You can also see the options and usage.

## How to use quotator

Use quotator to get prices for 3D printing parts. You can use it on a single `stl`file or in a directory, in which case it will iterate over all the files in the directory and price the `stl`files.

For example, to quote all the `stl`files in the current directory, run this in the console:
	
	quotator .
	
Or to quote a part:

	quotator /path/to/part.stl

You can change the script variables such as `DEFAULT_FIXED_PRICE_PER_PART` or `DEFAULT_PPCM3` to adapt it to your own pricing system.

## How is the price calculated

To be documented. Check the code for the complete algorithm.

## License

This work is licensed under the Creative Commons Attribution 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
