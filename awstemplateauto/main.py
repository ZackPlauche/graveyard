import json
from pathlib import Path

import yaml

def filter_vpcs_by_tag(vpcs, value) -> list:
    """Filter through a vpc_list (vpcs) to find the ones that have a tag that 
    contains the given search value (value).
    
    Example usage:
    >>> vpcs = yaml.safe_load(yaml_file.read_text())['Vpcs']
    >>> new_vpcs = filter_vpcs_by_tag(vpc_list, 'DMZ')
    >>> first_vpc = new_vpcs[0]
    >>> vpc['Tags'][0]['Value']
    'DMZ'
    """

    filtered_vpcs = [vpc for vpc in vpcs if vpc_has_tag(vpc, value)]
    return filtered_vpcs
                

def vpc_has_tag(vpc, value):
    """Looks inside of a VPC and see if any of the tags contain a given value."""
    return any(tag for tag in vpc['Tags'] if tag['Value'] == value)
        

if __name__ == '__main__':
    # NOTE: The following 2 variables are in all caps because that's how you express variables are supposed to be constants (variables that don't change)
    # 1. Load the data template for the rest of the files that you want to make.
    TEMPLATE_FILE = Path('template.json')  # 1.1 Get the template file
    TEMPLATE_DATA = json.loads(TEMPLATE_FILE.read_text())  # 1.2 Extract the data from it

    # 2. Pick the source file you want to use and have the new file ready to write to.
    yaml_source_file = Path('source.yaml')  # 2.1 Have the source file available as a variable
    new_file = Path('newfile.yaml')  # 2.2 Have the new file ready to load data to.

    # 3. Create and edit a template instance and write it to a new file.
    vpcs = yaml.safe_load(yaml_source_file.read_text())['Vpcs']  # 3.1 Load the vpc list (or array) from the source file
    filtered_vpcs = filter_vpcs_by_tag(vpcs, 'DMZ')  #  3.2 Create a list of only the VPCs that contain a tag with a certain value.
    vpc_id = filtered_vpcs[0]['VpcId']  # 3.3 Get the first instance from the list of filtered VPCs.
    template_data_instance = TEMPLATE_DATA.copy()  # 3.4 Create an instance of the copied template data so you don't mess with the intial template. This creates a Python dictionary. Do this as many times as you need. DO NOT EDIT THE "TEMPLATE_DATA" AS THIS IS A CONSTANT.
    template_data_instance['Parameters']['EnvType']['VPC'] = vpc_id  # 3.5 Edit the instance of the template data to be the way you want it.
    new_file.write_text(yaml.dump(template_data_instance))  # 3.6 Write that instance to a file.