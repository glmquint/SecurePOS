from unittest import TestCase
from src.Storage.dbConfig import DBConfig
from src.Storage.StorageController import StorageController


class TestStorageController(TestCase):
    class Object:
        def __init__(self, name, age):
            print('Here')
            self.name = name
            self.age = age
    obj = Object('Giacomo', 24)
    dbConf = DBConfig('test', 'test', obj.__dict__.keys())

    def test_save(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.save(self.obj)

    def test_retrieveAll(self):
        st = StorageController(self.dbConf, type(self.obj))
        print(st.retrieve_all())

    def test_removeAll(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.remove_all()
        print(st.retrieve_all())

    def test_insertAndRemove(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.remove_all()
        st.save(self.obj)
        retrieved_obj = st.retrieve_all()
        self.assertEqual(
            retrieved_obj[0][1],
            'Giacomo')  # first element is the id
        self.assertEqual(retrieved_obj[0][2], 24)
        st.remove_all()
        self.assertEqual(st.retrieve_all(), [])
        self.assertTrue(True)
