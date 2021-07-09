import unittest
import pandas as pd
import time

from phone_validation import get_data_from_api, create_dataframe
from phone_validation import put_values_dataframe, get_values


class PhoneNumTest(unittest.TestCase):

    def test_data_from_api(self):
        api_key = '2240019ef22443bf83b96d9fc4599e31'
        phone_number = '16156002012'
        response_json = get_data_from_api(phone_number, api_key)
        self.assertEqual(type(response_json), type({}))
        self.assertNotEqual(response_json, {})

    def test_dtfr_creation(self):
        dtfr = create_dataframe()
        self.assertEqual(type(dtfr), type(pd.DataFrame()))
        column_names = ['Phone Number', 'Validity', 'Country', 'Location',
                        'International Format', 'Type', 'Carrier']
        for i in range(len(column_names)):
            self.assertEqual(column_names[i], dtfr.columns[i])

    def test_values(self):
        api_key = '2240019ef22443bf83b96d9fc4599e31'
        phone_number = '16156002012'
        time.sleep(1)
        data = get_data_from_api(phone_number, api_key)
        values1 = get_values(data)
        values2 = ('16156002012', True, 'United States', 'Tennessee',
                   '+16156002012', 'mobile', 'T-Mobile USA, Inc.')
        self.assertEqual(values1, values2)


if __name__ == '__main__':
    unittest.main()
