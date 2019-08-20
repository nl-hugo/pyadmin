import logging
from functools import wraps

from django.db.models.signals import pre_save
from django.dispatch import receiver

from kilometers.geocoders import geo_code, get_driving_distance
from kilometers.models import Trip, Location

logger = logging.getLogger(__name__)


def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)

    return wrapper


@receiver(pre_save, sender=Location)
@disable_for_loaddata
def pre_save_location_receiver(sender, instance, **kwargs):
    """Disable zip code updates for Location objects."""
    logger.debug('Saving Location {} ...'.format(instance))
    do_geocode = instance.pk is None  # update existing location?

    if not do_geocode:  # location exists
        logger.info('Location already exists')
        current = Location.objects.get(pk=instance.pk)
        if current.zip_code != instance.zip_code:
            logger.warning('Zip codes cannot be changed')
            instance.zip_code = current.zip_code
        else:
            logger.info('Some other field changed')
            # do_geocode = True

    logger.info('Geocode? {}'.format(do_geocode))

    if do_geocode:
        logger.info('Geocode ...')
        instance.zip_code = instance.zip_code.replace(' ', '').upper()
        # FIXME: breaks if zipcode does not exist 
        loc = geo_code(instance.zip_code)
        instance.lon = loc.longitude
        instance.lat = loc.latitude
        instance.city = loc.address.split(',')[0]


@receiver(pre_save, sender=Trip)
@disable_for_loaddata
def pre_save_trip_receiver(sender, instance, **kwargs):
    """
    Recompute distance and allowance when required.
    """
    recompute = instance.pk is None  # recompute for new instances
    logger.info('New trip? {}'.format(recompute))

    logger.info(Location.objects.all())
    logger.info(Trip.objects.all())
    logger.info(sender)
    logger.info(instance)
    logger.info(instance.pk)

    # TODO: if is_return has changed, then distance/2 and recompute rate!!

    if not recompute:  # instance already there

        current = Trip.objects.get(pk=instance.pk)
        logger.info('Api status: {}'.format(current.api_return_code))

        if not (current.origin == instance.origin and current.destination == instance.destination):
            logger.info('Locations have changed, recalculate distance...')
            recompute = True

        elif current.is_return != instance.is_return:
            logger.info('Is return modified...')
            instance.distance = current.distance * 2 if instance.is_return else current.distance / 2

        elif current.api_return_code != '200':
            logger.info('Previous error, recalculate distance...')
            recompute = True

    else:
        logger.info('New trip...')

    if recompute:
        logger.info('Calculating distance ...')
        distance, instance.api_return_code, instance.api_message = get_driving_distance(
            instance.origin.as_geo_location(), instance.destination.as_geo_location())
        instance.distance = distance * 2 if instance.is_return else distance
    else:
        logger.info('No recompute needed')
