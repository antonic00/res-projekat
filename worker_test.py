import socket
import unittest
from unittest.mock import patch, MagicMock
from unittest import mock

import collection_description
import database_functions
import worker

class TestWorker(unittest.TestCase):


    def test_dodaj_element_1(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 1
        test_code = 'CODE_ANALOG'
        test_value = 1
        test_timestamp = '12-2-2022'
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.dodaj_element(test_worker, test_id, test_dataset, test_code, test_value, test_timestamp))

    def test_dodaj_element_2(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 2
        test_code = 'CODE_CUSTOM'
        test_value = 1
        test_timestamp = '12-2-2022'
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.dodaj_element(test_worker, test_id, test_dataset, test_code, test_value, test_timestamp))

    def test_dodaj_element_3(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 3
        test_code = 'CODE_SINGLENODE'
        test_value = 1
        test_timestamp = '12-2-2022'
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.dodaj_element(test_worker, test_id, test_dataset, test_code, test_value, test_timestamp))

    def test_dodaj_element_4(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 4
        test_code = 'CODE_CONSUMER'
        test_value = 1
        test_timestamp = '12-2-2022'
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.dodaj_element(test_worker, test_id, test_dataset, test_code, test_value, test_timestamp))

    def test_update_element_1(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 1
        test_value = 1
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.update_element(test_worker, test_id, test_dataset, test_value))

    def test_update_element_2(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 2
        test_value = 1
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.update_element(test_worker, test_id, test_dataset, test_value))

    def test_update_element_3(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 3
        test_value = 1
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.update_element(test_worker, test_id, test_dataset, test_value))

    def test_update_element_4(self):
        test_worker = worker.Worker()
        test_id = 1
        test_dataset = 4
        test_value = 1
        test_baza = database_functions.konekcija()
        test_worker.baza = test_baza
        self.assertEqual(None, worker.Worker.update_element(test_worker, test_id, test_dataset, test_value))


    def test_izracunaj_deadband_ok(self):
        test_worker = worker.Worker()
        test_iz_baze = 20
        test_pristigla = 10

        self.assertEqual(50, worker.Worker.izracunaj_deadband(test_worker, test_iz_baze, test_pristigla))

    def test_izracunaj_deadband_error(self):
        test_worker = worker.Worker()
        test_iz_baze = 0
        test_pristigla = 20
        test_worker.side_effect = ZeroDivisionError

        self.assertEqual(100, worker.Worker.izracunaj_deadband(test_worker.side_effect, test_iz_baze, test_pristigla))

    def test_primi_podatke(self):
        test_baza = database_functions.konekcija()
        test_soket1 = MagicMock(socket.socket)
        test_soket2 = MagicMock(socket.socket)

        test_worker = worker.Worker()
        test_worker.baza = test_baza
        test_worker.worker_sa_load_balancerom = test_soket1
        test_worker.worker_sa_readerom = test_soket2

        with mock.patch('worker.pickle.loads', side_effect=[collection_description.Collection_Description(1, 2)]):
            assert worker.Worker.primi_podatke(test_worker) == None

if __name__ == '__main__':
    unittest.main()
