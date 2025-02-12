import unittest
import json
from __init__ import *


def read_exported_data(instrument_export_filename, text_export_filename):
    well_name_lookup = {}
    text_report_count = 0
    df = pd.read_csv(text_export_filename, sep="\t",low_memory=False)
    df.columns = [x.strip() for x in df.columns]
    for ii, row in df.iterrows():
        if row['Well'].strip() == '---':
            print('Warning: Condensed data (not usable) in %s' % fn)
            break
        well_no = code_to_well_no(row['Well'].strip().encode('utf-8'))
        if well_no < 1 or well_no > 96:
            raise ValueError("invalid Well number")
        well_name_lookup[well_no]  = str(row['Well Name']).strip()
    raw_df = pd.read_csv(instrument_export_filename, sep="\t", skiprows=1, engine='python')
    raw_df = raw_df[raw_df['Segment'] == 2]  #we only care about the amplification part, not the melting curve
    well_names = []
    for ii, row in raw_df.iterrows():
        try:
            well_name = well_name_lookup[row['Well']]
        except KeyError: # manual checking showed that these are empty wells indeed
            well_name = np.nan
        well_names.append(well_name)
    raw_df.insert(0, 'Well Name', well_names)
    return raw_df.reset_index()


def compare_mxp_and_exported(mxp_df, exported_df):
    mxp_df = mxp_df.copy()
    mxp_df.Well = mxp_df.Well + 1
    mxp_df = mxp_df.set_index(['Well','Cycle'])
    exported_df = exported_df.set_index(['Well','Cycle #']).copy()
    exported_df.loc[exported_df['Well Name'] == '---', 'Well Name'] = ''
    mxp_df = mxp_df.loc[exported_df.index]
    # print('fluorescence', (exported_df.Fluorescence == mxp_df.Fluorescence).all())
    # print('well name' ,(exported_df['Well Name'] == mxp_df['Well Name']).all())
    # print(exported_df['Well Name'])
    # print(mxp_df['Well Name'])
    # print('assay', (exported_df['Dye'] == mxp_df['Assay']) .all())
    return (
            (exported_df.Fluorescence == mxp_df.Fluorescence) & 
            (exported_df['Well Name'] == mxp_df['Well Name'].str.decode('utf-8', errors='replace')) &
        (exported_df['Dye'] == mxp_df['Assay'].str.decode('utf-8', errors='replace')) 
        ).all()
    
class MXPTests(unittest.TestCase):

    def test_format_3000(self):
        #anonymized test file, some empty wells, nothing fancy
        fn = 'testfiles/3000.mxp'
        data = read_mxp(fn)
        exported_data = read_exported_data(
            "testfiles/3000 - Instrument Data - Text Format 1.txt",
            "testfiles/3000 - Text Report Data.txt")
        self.assertTrue(compare_mxp_and_exported(data, exported_data))

    def test_format_3005(self):
        #anonymized test file, some empty wells, nothing fancy
        fn = 'testfiles/3005.mxp'
        data = read_mxp(fn)
        exported_data = read_exported_data(
            "testfiles/3005 - Instrument Data - Text Format 1.txt",
            "testfiles/3005 - Text Report Data.txt")
        self.assertTrue(compare_mxp_and_exported(data, exported_data))

    def test_rm_1(self):
        fn = 'testfiles/U937 cells ski and vector 7.05.2018.mxp'
        data = read_mxp(fn)

    def test_rm_2(self):
        fn = 'testfiles/HL60 SKI GFP 19.04.2018.mxp'
        data = read_mxp(fn)

    def test_set_numbers(self):
        fn = "testfiles/set_number_test.mxp"
        data = read_mxp(fn)
        with open('testfiles/set_number_test.should.json') as of:
            should = json.loads(of.read())
        assert (data['Assay'].str.decode('utf-8', errors='replace') == should['Assay']).all()
        assert (data['Well Name'].str.decode('utf-8', errors='replace') == should['Well Name']).all()
        assert (data['Set id'].str.decode('utf-8', errors='replace') == should['Set id']).all()


if __name__ == '__main__': 
    unittest.main()


