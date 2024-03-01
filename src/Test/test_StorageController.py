from unittest import TestCase
from dbConfig import DBConfig
from StorageController import StorageController

class TestStorageController(TestCase):
    class Object:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    obj = Object('Giacomo', 24)
    dbConf = DBConfig('test', 'test', obj.__dict__.keys())
    def test_save(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.save(self.obj)


    def test_retrieveAll(self):
        st = StorageController(self.dbConf, type(self.obj))
        print(st.retrieveAll())

    def test_removeAll(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.removeAll()
        print(st.retrieveAll())

    def test_insertAndRemove(self):
        st = StorageController(self.dbConf, type(self.obj))
        st.removeAll()
        st.save(self.obj)
        retrieved_obj = st.retrieveAll()
        self.assertEqual(retrieved_obj[0][1], 'Giacomo') # first element is the id
        self.assertEqual(retrieved_obj[0][2], 24)
        st.removeAll()
        self.assertEqual(st.retrieveAll(), [])
        self.assertTrue(True)