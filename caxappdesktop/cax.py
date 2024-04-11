import time
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

CAX_FILE_HEADER = (';  _______________________________________________________________________\n'
                   '; |                                                                       |\n'
                   '; |                        Copyright © 2020-2021                          |\n'
                   '; |                              TestCompany Inc.                         |\n'
                   '; | _____________________________________________________________________ |\n'
                   '; |                                                                       |\n'
                   '; |                        http://www.testingABC.com                      |\n'
                   '; |                      contact: never@testABC.com                       |\n'
                   '; |_______________________________________________________________________|\n'
                   ';\n'
                   '; _________________________________________________________________________\n')


FieldValues = namedtuple('FieldValues', 'Name Unit Factor Offset StartAddr')
Axis = namedtuple('Axis', 'Name IdName Unit Factor Offset Radix bBackwards '
                          'bReciprocal bSigned Precision DataSrc DataHeader '
                          'DataAddr DataOrg SignatureByte SkipBytes')


@dataclass
class CAXEntry:
    """
    CAX File entry data class that conveniently stores all of the CAX data and
    formats them properly when called as a string.
    """

    id: str
    desc1: str
    desc2: str
    segment: int
    caption: str
    major: str
    minor: str
    vis: int  # 1 is security for v2 plugged in
    dis: int
    address: str
    bit_off: int
    bits: int
    byte_type: str
    byte_inv: int
    units: str
    factor: float
    offset: int  # Must be positive
    prec: int
    min_limit: int
    max_limit: int
    min_user: int
    max_user: int
    si_enum: str
    im_enum: str
    si_col: str
    si_row: str
    im_col: str
    im_row: str
    two_d: int = 0  # is always 0
    grp: int = 0  # is always 0
    body: str = '.'
    column: str = '.'
    row: str = '.'

    def __post_init__(self):
        self.name = self.desc1  # Here for convenience due to the mapping of the CSV
        self.idname = self.desc2  # ^

    def __str__(self):
        return (';\n'
                ';\n'
               f'[{self.id}]\n'
               f';         Description\n'
                ';         ---------------------------------------------------------------------------------------------------------------------------------\n'
                ';\n'
               f'DESC.001 =  {self.name}\n'
               f'DESC.002 = {self.idname}\n'
                ';         Seg Caption                                  Major              Minor              Vis Dis 2D Grp\n'
               f'VIEW =     {self.segment}    "{self.caption}"              "{self.major}"           "{self.minor}"      {self.vis}   {self.dis}  {self.two_d}  {self.grp}\n'
                ';         Address(es)                      BitOff Bits Typ Inv\n'
               f'ADDR =     {self.address}                                {self.bit_off}   {self.bits}  {self.byte_type}   {self.byte_inv}\n'
                ';         Unit Symbol            Factor         Offset Prec       MinLimit       MaxLimit        MinUser        MaxUser\n'
               f'SI_SLOT = {self.units}                     {self.factor}              {self.offset}    {self.prec}              {self.min_limit}          {self.max_limit}              {self.min_user}          {self.max_user}\n'
                ';    # Body            #Col              #Row\n'
                ';         -------------- -------------- --------------\n'
                ';ULABELS = .              .              .\n'
               f'ULABELS = {self.body}              {self.column}              {self.row}\n'
                ';           # Enumerations\n'
               f'SI_ENUM = "{self.si_enum}"\n'  # TODO: Sometimes there's a discrepency between using . or ""
               f'IM_ENUM = "{self.im_enum}"\n'
               f'SI_COL = .             "{self.si_col}"                \n'  # TODO: Check if spacing is accurate
               f'SI_ROW = .             "{self.si_row}"                \n'
               f'IM_COL =  .            "{self.im_col}"                \n'
               f'IM_ROW =  .            "{self.im_row}"                \n'
                '; ======================================================================================================\n')


def format_csv_to_cax(csv_file_path, cax_file_path):
    cax_file = Path(cax_file_path)
    cax_entries: str = get_cax_entries_from_csv(csv_file_path)
    cax_file.write_text(CAX_FILE_HEADER + cax_entries, encoding='utf-8', errors='ignore')


def get_cax_entries_from_csv(csv_file_path) -> str:
    NULL_VALUES = {'$0', '$-1', 'nan'}
    result_list = []
    csv_data = pd.read_csv(csv_file_path, delimiter=';', encoding='cp1252', nrows=1000)
    for row in csv_data.itertuples():
        field_values = FieldValues(*row[21:26])
        x_axis, y_axis = Axis(*row[26:42]), Axis(*row[42:])
        count = 9000 + row.Index
        y_axis_columns = '.'
        x_axis_list = '.'

        # Step 1: If Y Data exists, write Y entry and update default si_row to it's reference id
        if y_axis.DataAddr not in NULL_VALUES:
            y_axis_columns = ','.join(str(num) for num in range(1, int(row.Columns) + 1))
            bits, byte_type = get_bits_and_byte_type(y_axis.DataOrg, row)
            y_cax_entry = CAXEntry(id=f'{count}_y',
                                   desc1=y_axis.IdName,
                                   desc2=y_axis.Name,
                                   segment=2,
                                   caption=f'{y_axis.Name}y-axis',
                                   major="Custom Folder",
                                   minor='Y Axis Defined',
                                   vis=1,
                                   dis=2,
                                   address=str(y_axis.DataAddr).strip('$'),
                                   bit_off=0,
                                   bits=bits,
                                   byte_type=byte_type,
                                   byte_inv=0,
                                   units=y_axis.Unit,
                                   factor=y_axis.Factor,
                                   offset=abs(y_axis.Offset),
                                   prec=y_axis.Precision,
                                   min_limit=-65535,
                                   max_limit=65535,
                                   min_user=-65535,
                                   max_user=65535,
                                   si_enum='.',
                                   im_enum='.',
                                   si_row=y_axis_columns,
                                   si_col='',
                                   im_row=y_axis_columns,
                                   im_col='')
            result_list.append(str(y_cax_entry))
            si_row = f'@{y_cax_entry.id}'
        else:
            si_row = ''

        # Step 2: If X Data exists, write X entry and update default si_col to it's reference id
        if x_axis.DataAddr not in NULL_VALUES:
            x_axis_list = ','.join([str(num) for num in range(1, int(row.Rows) + 1)])
            bits, byte_type = get_bits_and_byte_type(x_axis.DataOrg, row)
            x_cax_entry = CAXEntry(id=f'{count}_x',
                                   desc1=x_axis.IdName,
                                   desc2=x_axis.Name,
                                   segment=2,
                                   caption=f'{row.Name}x-axis',
                                   major='Custom Folder',
                                   minor='X Axis Defined',
                                   vis=1,
                                   dis=2,
                                   address=x_axis.DataAddr.strip('$'),
                                   bit_off=abs(x_axis.Offset),
                                   bits=bits,
                                   byte_type=byte_type,
                                   byte_inv=0,
                                   units=x_axis.Unit,
                                   factor=x_axis.Factor,
                                   offset=abs(x_axis.Offset),
                                   prec=x_axis.Precision,
                                   min_limit='',
                                   max_limit='',
                                   min_user='',
                                   max_user='',
                                   si_enum='.',
                                   im_enum='.',
                                   si_row=x_axis_list,
                                   im_row=x_axis_list,
                                   si_col='',
                                   im_col='')
            result_list.append(str(x_cax_entry))
            si_col = f'@{x_cax_entry.id}'
        else:
            si_col = ''

        # Step 3: Write the default entry
        bits, byte_type = get_bits_and_byte_type(row.DataOrg, row)
        dis = 3 if y_axis.DataAddr not in NULL_VALUES else 2 if x_axis.DataAddr not in NULL_VALUES else 1
        default_entry = CAXEntry(id=f'C{count}',
                                 desc1=row.IdName.replace("\\", ""),
                                 desc2=row.Name.replace("\\", ""),
                                 segment=2,
                                 caption=row.Name,
                                 major='Custom Folder',
                                 minor=row.Name, 
                                 vis=1,
                                 dis=dis,
                                 address=field_values.StartAddr.strip('$'),
                                 bit_off=0,
                                 bits=bits,
                                 byte_type=byte_type,
                                 byte_inv=0,
                                 units=field_values.Unit,
                                 factor=field_values.Factor,
                                 offset=abs(field_values.Offset),
                                 prec=row.Precision,
                                 min_limit=-65535,
                                 max_limit=65535,
                                 min_user=-65535,
                                 max_user=65535,
                                 si_enum=x_axis_list,
                                 im_enum=y_axis_columns,
                                 si_row=si_col,
                                 si_col=si_row,
                                 im_row='',
                                 im_col='')
        result_list.append(str(default_entry))
    cax_entries = ''.join(result_list)
    return cax_entries


def get_bits_and_byte_type(data_org, row):
    data_orgs = {
        'eByte': (8, 'SED'),
        'eLoHiLoHi': (32, 'FTL'),
        'eHiLoHiLo': (32, 'FTL'),
        'eFloatHiLo': (32, 'FLT'),
        'eDataOrgNone': (16, 'UNM'),
    }
    if data_org in data_orgs.keys():
        bits, byte_type = data_orgs[data_org]
# TODO: Figure out whether or not to add Error if the data_org is nothing defined in the data_orgs keys
    else:
        bits = 16
        byte_type = 'UNM' if row.bReciprocal == 0 else 'SNM'
    return bits, byte_type 


def valid_software():
    """
    Validate software is using an installer before using the software.
    This is to make sure that this is installed only on one machine.
    """

    secrets_file = Path.home() / '.tcmconv' / 'secrets.txt'
    if not secrets_file.exists():
        print('You do not have access to this software.')
        return False
    return True


if __name__ == '__main__':
    csv = Path('testdata/csv') / '31140302-DELETE.csv'
    cax = Path('testdata/cax') / '31140302.cax'
    start = time.time()
    format_csv_to_cax(csv, cax)
    end = time.time()
    print(end - start)

