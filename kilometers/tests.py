from datetime import datetime

from django.test import TestCase

from kilometers.models import Location, Trip


class LocationTestCase(TestCase):

    def setUp(self):
        Location.objects.create(name='Domtoren', zip_code='3512 jc',
                                city='should_be_overwritten')

    def test_save_location(self):
        """
        Location should be saved correctly.
        """
        location = Location.objects.get(name='Domtoren')
        self.assertEqual(location.zip_code, '3512JC')
        self.assertEqual(location.city, 'Utrecht')
        self.assertEqual(location.lat, '52.0910473858882')
        self.assertEqual(location.lon, '5.12155287407166')

    def test_update_name(self):
        """
        Location name should be update correctly.
        """
        location = Location.objects.get(name='Domtoren')
        location.name = 'Domplein'
        location.save()
        self.assertEqual(location.name, 'Domplein')

    def test_update_zip(self):
        """
        Location zip code must not be updated.
        """
        location = Location.objects.get(name='Domtoren')
        location.zip_code = '9999xx'
        location.save()
        self.assertEqual(location.zip_code, '3512JC')


class TripTestCase(TestCase):
    fixtures = ['tests']

    def setUp(self):
        pass

    def test_save_trip(self):
        """
        Trip should be saved correctly.
        """
        origin = Trip.objects.first().origin
        destination = Location.objects.get(name='Grolsch Veste')
        trip = Trip.objects.create(date=datetime(2019, 6, 1).date(),
                                   origin=origin, destination=destination, is_return=False,
                                   description='Test trip')

        self.assertEqual(trip.date, datetime(2019, 6, 1).date())
        self.assertEqual(trip.year, 2019)
        self.assertEqual(trip.quarter, '2019-Q2')
        self.assertEqual(trip.origin.name, 'Domtoren')
        self.assertEqual(trip.destination.name, 'Grolsch Veste')
        self.assertEqual(trip.is_return, False)
        if trip.api_return_code == 200:
            self.assertEqual(trip.distance, 139)  # 139km one way
        else:
            self.fail('API return code {} not OK, please rerun test!'.format(
                trip.api_return_code))

    def test_update_date(self):
        """
        Trip should be updated correctly
        """
        trip = Trip.objects.first()
        trip.date = datetime(2018, 6, 1).date()
        trip.save()

        self.assertEqual(trip.date, datetime(2018, 6, 1).date())
        self.assertEqual(trip.year, 2018)
        self.assertEqual(trip.quarter, '2018-Q2')

    def test_update_is_return(self):
        """
        Trip is_return should be updated correctly.
        """
        trip = Trip.objects.first()
        self.assertEqual(trip.is_return, True)

        trip.is_return = False
        trip.save()

        self.assertEqual(trip.is_return, False)
        self.assertEqual(trip.distance, 3)  # 3km one way

    def test_update_destination(self):
        """
        Trip is_return should be updated correctly.
        """
        trip = Trip.objects.first()
        destination = Location.objects.get(name='Grolsch Veste')
        trip.destination = destination
        trip.save()

        self.assertEqual(trip.destination.name, 'Grolsch Veste')
        self.assertEqual(trip.is_return, True)
        if trip.api_return_code == 200:
            self.assertEqual(trip.distance, 2 * 139)  # 139km one way
        else:
            self.fail('API return code {} not OK, please rerun test!'.format(
                trip.api_return_code))
