"""Command line quoting app for 3D printed parts"""
import os.path
import argparse

import trimesh


## FDM slicing parameters
SHELL_THICKNESS = 0.12  # cm
INFILL_RATIO = 0.20


DEFAULT_FIXED_PRICE_PER_PART = 1.0  # €
DEFAULT_PPCM3 = 0.40  # €
# ppcm3 refers to the sliced volume, not the mesh volume


class PartQuotation(object):
    """Class for generating all the part mesh info and calculating the price."""

    def __init__(self, path, unit=None, fixed_price=None, ppcm3=None):
        """Populate the PartQuotation instance given a path and mesh units"""

        # Checking  and cleaning `unit` argument input
        if unit is None:
            unit = "mm"
        self.unit = unit

        # Setting conversion factors to convert the file units to mm
        if unit == "mm":
            conversion_factor = 1
        elif unit == "cm":
            conversion_factor = 10
        elif unit == "in":
            conversion_factor = 25.4
        else:
            raise Exception("Cannot recognize the unit code argument provided.")

        # Checking fixed_price argunment and setting default value
        if fixed_price is None:
            self.fixed_price = DEFAULT_FIXED_PRICE_PER_PART
        elif not isinstance(fixed_price, float):
            raise Exception("Wrong type provided as `fixed_price`. Float required.")
        else:
            self.fixed_price = fixed_price

        # Checking ppcm3 argunment and setting default value
        if ppcm3 is None:
            self.ppcm3 = DEFAULT_PPCM3
        elif not isinstance(ppcm3, float):
            raise Exception("Wrong type provided as `ppcm3`. Float required.")
        else:
            self.ppcm3 = ppcm3


        # Store the part name
        self.name = os.path.basename(path)


        # Load the mesh in trimesh and extract its parameters
        mesh = trimesh.load(path)

        self.volume = mesh.volume*conversion_factor**3 / 1000 #unit: cm3
        self.surface = mesh.area*conversion_factor**2 / 100   #unit: cm2
        self.is_watertight = mesh.is_watertight
        self.bounding_box_size = mesh.bounding_box.extents*conversion_factor #unit: mm
        self.number_of_bodies = mesh.split().size


class FDMPartQuotation(PartQuotation):
    """FDM part quotation."""

    def __init__(self, path, unit=None, fixed_price=None, ppcm3=None):
        super().__init__(path, unit=None, fixed_price=None, ppcm3=None)
        self.sliced_volume = self.surface*SHELL_THICKNESS + (self.volume - self.surface*SHELL_THICKNESS)*INFILL_RATIO #cm3

    def calculate_price(self):
        """Calculate the part price using fixed_price and ppcm3 from self"""

        price = self.fixed_price + self.sliced_volume * self.ppcm3

        return price

    def part_line(self):
        """Returns a string with the name and price of the part."""

        return "{} (FDM) - {:.2f}€".format(self.name, self.calculate_price())


class SLAPartQuotation(PartQuotation):
    """SLA/DLP part quotation."""

    def calculate_price(self):
        """Calculate the part price using fixed_price and ppcm3 from self"""

        price = self.fixed_price + self.volume * self.ppcm3

        return price

    def part_line(self):
        """Returns a string with the name and price of the part."""

        return "{} (SLA) - {:.2f}€".format(self.name, self.calculate_price())


class OrderQuotation(object):
    """Class to create and represent customer orders"""

    parts = []

    def add_part_quotation(self, part_quotation):
        """Add a new PartQuotation object to the order."""
        self.parts.append(part_quotation)

    def calculate_total(self):
        """Calculate the total price of the order"""

        total = 0.0
        for part in self.parts:
            total += part.calculate_price()

        return total

    def print_order(self):
        """Print out the text of the order"""


        print("Part list, price per unit")
        print("-------------------------")

        for part in self.parts:
            print(part.part_line())

        print("-------------------------")
        print("Total: {:.2f}€   ".format(self.calculate_total()))



def quotator(path, unit="mm", technology=None, debug=False):
    """Function for quotating a file or directory of 3D printed parts."""

    if technology is None:
        technology = "FDM"

    if debug:
        print("DEBUG INFO: unit = {}".format(unit))

    # Checking if the path provided is a file or a directory
    # If path points to a file we only quote the individual file
    if os.path.isfile(path):
        if debug:
            print("DEBUG INFO: `path` is file")

        if technology == "FDM":
            quoted_part = FDMPartQuotation(path, unit)
        elif technology == "SLA":
            quoted_part = SLAPartQuotation(path, unit)
        else:
            raise Exception("Cannot recognize the technology code argument provided.")

        print(quoted_part.part_line())

    # if the path is a directory, quote all the files inside
    else:
        if debug:
            print("DEBUG INFO: `path` is dir")

        files = os.listdir(path)
        order_quotation = OrderQuotation()

        for f in files:

            extension = os.path.splitext(f)[1]

            if (extension == ".stl") or (extension == ".STL"):

                # Rebuild the part path
                if path[-1] == "/":
                    part_path = path + f
                else:
                    part_path = path + "/" + f

                if technology == "FDM":
                    quoted_part = FDMPartQuotation(part_path, unit)
                elif technology == "SLA":
                    quoted_part = SLAPartQuotation(part_path, unit)
                else:
                    raise Exception("Cannot recognize the technology code argument provided.")

                order_quotation.add_part_quotation(quoted_part)

        order_quotation.print_order()


parser = argparse.ArgumentParser(description="Get 3D print price quotations for a file or directory")
parser.add_argument(
    "path",
    help="file or directory to be quoted")
parser.add_argument(
    "-u",
    "--unit",
    help="mesh units of the parts to be quoted (mm, cm or in)")
parser.add_argument(
    "-t",
    "--technology",
    help="3D printing technology (FDM or SLA)")

args = parser.parse_args()


if __name__ == "__main__":
    quotator(args.path, args.unit, args.technology, debug=False)


    #part = PartQuotation(args.path, fixed_price=10.0)
    #price = part.calculate_price()
    #print(price)

