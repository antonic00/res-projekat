import socket
import unittest
from unittest.mock import patch, MagicMock
from unittest import mock

import collection_description
import database_functions
import reader

class TestReader(unittest.TestCase):
    def test_citanje_iz_baze_1(self):
        test_reader = reader.Reader()
        test_code = 'CODE_CUSTOM'
        test_baza = database_functions.konekcija()
        test_reader.baza = test_baza
        self.assertEqual([(1, 2, 'CODE_CUSTOM', 1, '12-2-2022')], reader.Reader.citanje_iz_baze(test_reader, test_baza, test_code))

    def test_citanje_iz_baze_2(self):
        test_reader = reader.Reader()
        test_code = 'CODE_ANALOG'
        test_baza = database_functions.konekcija()
        test_reader.baza = test_baza
        self.assertEqual([(1, 1, 'CODE_ANALOG', 1, '12-2-2022')], reader.Reader.citanje_iz_baze(test_reader, test_baza, test_code))

    def test_citanje_iz_baze_3(self):
        test_reader = reader.Reader()
        test_code = 'CODE_SINGLENODE'
        test_baza = database_functions.konekcija()
        test_reader.baza = test_baza
        self.assertEqual([(1, 3, 'CODE_SINGLENODE', 1, '12-2-2022')], reader.Reader.citanje_iz_baze(test_reader, test_baza, test_code))

    def test_citanje_iz_baze_4(self):
        test_reader = reader.Reader()
        test_code = 'CODE_CONSUMER'
        test_baza = database_functions.konekcija()
        test_reader.baza = test_baza
        self.assertEqual([(1, 4, 'CODE_CONSUMER', 1, '12-2-2022')], reader.Reader.citanje_iz_baze(test_reader, test_baza, test_code))

    def test_primi_podatke(self):
        test_baza = database_functions.konekcija()
        test_soket1 = MagicMock(socket.socket)

        test_reader = reader.Reader()
        test_reader.baza = test_baza
        test_reader.reader_to_worker = test_soket1

        with mock.patch('reader.pickle.loads', side_effect=[collection_description.Collection_Description(1, 2)]):
            assert reader.Reader.primi_podatke(test_reader, test_soket1) == None

if __name__ == '__main__':
    unittest.main()
