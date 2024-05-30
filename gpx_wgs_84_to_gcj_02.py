# Copyright Ye Tian (yetiansh@[gmail.com,connect.hku.hk])
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xml.etree.ElementTree as ET

from pygcj.pygcj import GCJProj

ns = "http://www.topografix.com/GPX/1/1"
patterns = [
    f".//{{{ns}}}trk/{{{ns}}}trkseg/{{{ns}}}trkpt",
    f".//{{{ns}}}wpt",
]

def gpx_to_gcj02(gpx_file_path, output_file_path):
    """
    Converts the coordinates in a GPX file from WGS-84 system to GCJ-02 system.

    Args:
        gpx_file_path (str): The path to the input GPX file.
        output_file_path (str): The path to the output GPX file.

    Returns:
        None
    """
    # Parse the GPX file
    tree = ET.parse(gpx_file_path, parser=ET.XMLParser(target=ET.TreeBuilder()))
    # Register the namespace prefix
    ET.register_namespace("", ns)

    # Create a GCJProj object
    trans = GCJProj()

    # Iterate through all the lat/lon coordinates in the GPX file
    items = list()
    for pattern in patterns:
        items.extend(tree.findall(pattern))

    for item in items:
        # Extract the lat/lon values
        lat = float(item.attrib["lat"])
        lon = float(item.attrib["lon"])

        # Convert the coordinates to GCJ-02 system
        gcj02_lat, gcj02_lon = trans.wgs_to_gcj(lat, lon)

        # Update the trkpt element with the new coordinates
        item.attrib["lat"] = str(gcj02_lat)
        item.attrib["lon"] = str(gcj02_lon)

    # Save the modified GPX tree to a new file
    tree.write(output_file_path, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    # Set the input file path
    input_file = None
    # Set the output file path
    output_file = None
    gpx_to_gcj02(input_file, output_file)
