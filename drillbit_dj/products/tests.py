from django.test import TestCase, TransactionTestCase
from products.models import Rig

class RigTestCase(TransactionTestCase):

    def setUp(self):
        Rig.objects.create(
            make='Bitmain',
            model='S9',
            manufacturer='Bitmain',
            hash_rate=14,
            power=1350,
            buffer=0.1,
            price=900
        )

    def test_objects_created(self):
        rig = Rig.objects.get(make='Bitmain')
        self.assertEqual(rig.make, 'Bitmain')
        self.assertEqual(rig.model, 'S9')
        self.assertEqual(rig.manufacturer, 'Bitmain')
        self.assertEqual(rig.hash_rate, 14)
        self.assertEqual(rig.power, 1350)
        self.assertEqual(rig.buffer, 0.1)
        self.assertEqual(rig.price, 900)
        self.assertEqual(rig.name, 'Bitmain S9')

        self.assertEqual(rig.generation, None)
        self.assertEqual(rig.efficiency, 96.42857142857143)

    def test_unique_together(self):
        """
        unique_together for Rig model should be ('make', 'model', 'generation')
        """
        Rig.objects.create(
            make='Bitmain',
            model='S9',
            generation='i',
            manufacturer='Bitmain',
            hash_rate=14,
            power=1350,
            buffer=0.1,
            price=1000
        )

        with self.assertRaises(Exception):
            Rig.objects.create(
                make='Bitmain',
                model='S9',
                generation='i',
                manufacturer='Bitmain Fake',
                hash_rate=400,
                power=1200,
                buffer=0.25,
                price=123423
            )

class TestRigSerializer(TestCase):
    
        def setUp(self):
            self.rig = Rig.objects.create(
                make='Bitmain',
                model='S9',
                manufacturer='Bitmain',
                hash_rate=14,
                power=1350,
                buffer=0.1,
                price=900
            )
    
        def test_serialize(self):
            from products.serializers import RigSerializer
            serializer = RigSerializer(self.rig)
            
            self.assertEqual(serializer.data, {
                'name': 'Bitmain S9',
                'make': 'Bitmain',
                'model': 'S9',
                'manufacturer': 'Bitmain',
                'hash_rate': 14,
                'power': 1350,
                'buffer': 0.1,
                'price': 900,
            })

        def test_deserialize(self):
            from products.serializers import RigSerializer
            serializer = RigSerializer(data={
                'make': 'Bitmain',
                'model': 'S9',
                'manufacturer': 'Bitmain',
                'hash_rate': 14,
                'power': 1350,
                'buffer': 0.1,
                'price': 1000
            })
            self.assertTrue(serializer.is_valid())
            self.assertEqual(serializer.validated_data, {
                'make': 'Bitmain',
                'model': 'S9',
                'manufacturer': 'Bitmain',
                'hash_rate': 14,
                'power': 1350,
                'buffer': 0.1,
                'price': 1000
            })
            # Price should not be in validated_data b/c it is read_only

            serializer.save()
            self.assertEqual(Rig.objects.count(), 2)
            rig = Rig.objects.get(pk=2)
            self.assertEqual(rig.make, 'Bitmain')
            self.assertEqual(rig.model, 'S9')


