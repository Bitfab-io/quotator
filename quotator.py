import os.path
import argparse

import trimesh


file_path_1 = "/Users/diegotrap/Desktop/otto_body.stl"
file_path_2 = "/Users/diegotrap/Desktop/CABEZA 1.stl"  # No watertigth
file_path_3 = "/Users/diegotrap/Desktop/otto_legs.stl"  # Several parts
file_path_4 = "/Users/diegotrap/Desktop"  # directory


SHELL_THICKNESS = 0.12  # cm
INFILL_RATIO = 0.20


FIXED_PRICE_PER_PART = 1.0  # €
DEFAULT_PPCM3 = 0.40  # €
# ppcm3 refers to the sliced volume, not the mesh volume


class PartQuotation():
    """Class for generating all the part mesh info and calculate the price."""

    def __init__(self, path, unit=None):
        """Populate the PartQuotation instance given a path and mesh units"""
        
        if unit == None:
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

        

        # Store the part name
        self.name = os.path.basename(path)


        # Load the mesh in trimesh and extract its parameters
        mesh = trimesh.load(path)

        self.volume = mesh.volume*conversion_factor**3 / 1000 #unit: cm3
        self.surface = mesh.area*conversion_factor**2 / 100   #unit: cm2
        self.is_watertight = mesh.is_watertight
        self.bounding_box_size = mesh.bounding_box.extents*conversion_factor #unit: mm
        self.number_of_bodies = mesh.split().size

        self.sliced_volume = self.surface*SHELL_THICKNESS + (self.volume - self.surface*SHELL_THICKNESS)*INFILL_RATIO #cm3

    def calculate_price(self, price_per_cm3=DEFAULT_PPCM3):
        price = FIXED_PRICE_PER_PART + self.sliced_volume * price_per_cm3
        return price

class OrderQuotation:
    def add_part_quotation(self, part_quotation):
        pass


def quotator(path, unit="mm", price_per_cm3=DEFAULT_PPCM3, debug=False):

    if debug:
        print("DEBUG INFO: unit = {}".format(unit))

    # Checking if the path provided is a file or a directory
    if os.path.isfile(path) :
        if debug:
            print("DEBUG INFO: `path` is file".format(unit))

        quoted_part = PartQuotation(path, unit)
        name = quoted_part.name
        price = quoted_part.calculate_price(price_per_cm3)

        print("{} - {:.2f}€".format(name, price))

    # if the path is a directory, quote all the files inside
    else:
        if debug:
            print("DEBUG INFO: `path` is dir".format(unit))

        files = os.listdir(path)

        for f in files:

            file_name, extension = os.path.splitext(f)

            if (extension == ".stl") or (extension == ".STL"):

                # Rebuild the part path
                if path[-1] == "/":
                    part_path = path + f
                else:
                    part_path = path + "/" + f


                quoted_part = PartQuotation(part_path, unit)
                name = quoted_part.name
                price = quoted_part.calculate_price(price_per_cm3)

                print("{} - {:.2f}€".format(name, price))


parser = argparse.ArgumentParser(description="Get 3D print price quotations for a file or directory")
parser.add_argument(
    "path",
    help="file or directory to be quoted")
parser.add_argument(
    "-u",
    "--unit",
    help="mesh units of the parts to be quoted (mm, cm or in)")

args = parser.parse_args()


if __name__ == "__main__":
    quotator(args.path, args.unit, debug=False)

