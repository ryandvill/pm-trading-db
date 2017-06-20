from abc import ABCMeta, abstractmethod
from relationaldb.serializers import (
    CentralizedOracleSerializer, ScalarEventSerializer, CategoricalEventSerializer,
    UltimateOracleSerializer, MarketSerializer, OutcomeTokenInstanceSerializer,
    CentralizedOracleInstanceSerializer, OutcomeTokenIssuanceSerializer,
    OutcomeTokenRevocationSerializer
)

from celery.utils.log import get_task_logger
from json import dumps

logger = get_task_logger(__name__)


class AbstractEventReceiver(object):
    """Abstract EventReceiver class."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def save(self, decoded_event, block_info): pass


class CentralizedOracleFactoryReceiver(AbstractEventReceiver):

    def save(self, decoded_event, block_info):
        serializer = CentralizedOracleSerializer(data=decoded_event, block=block_info)
        if serializer.is_valid():
            serializer.save()
            logger.info('Centralized Oracle Factory Result Added: {}'.format(dumps(decoded_event)))
        else:
            logger.warning('INVALID Centralized Oracle Factory Result: {}'.format(dumps(decoded_event)))
            logger.warning(serializer.errors)


class EventFactoryReceiver(AbstractEventReceiver):

    events = {
        'ScalarEventCreation': ScalarEventSerializer,
        'CategoricalEventCreation': CategoricalEventSerializer
    }

    def save(self, decoded_event, block_info):
        if self.events.get(decoded_event.get('name')):
            serializer = self.events.get(decoded_event.get('name'))(data=decoded_event, block=block_info)
            if serializer.is_valid():
                serializer.save()
                logger.info('Event Factory Result Added: {}'.format(dumps(decoded_event)))
            else:
                logger.warning('INVALID Event Factory Result: {}'.format(dumps(decoded_event)))
                logger.warning(serializer.errors)


class UltimateOracleFactoryReceiver(AbstractEventReceiver):

    def save(self, decoded_event, block_info):
        serializer = UltimateOracleSerializer(data=decoded_event, block=block_info)
        if serializer.is_valid():
            serializer.save()
            logger.info('Ultimate Oracle Factory Result Added: {}'.format(dumps(decoded_event)))
        else:
            logger.warning('INVALID Ultimate Oracle Factory Result: {}'.format(dumps(decoded_event)))
            logger.warning(serializer.errors)


class MarketFactoryReceiver(AbstractEventReceiver):

    def save(self, decoded_event, block_info):
        serializer = MarketSerializer(data=decoded_event, block=block_info)
        if serializer.is_valid():
            serializer.save()
            logger.info('Market Factory Result Added: {}'.format(dumps(decoded_event)))
        else:
            logger.warning('INVALID Market Factory Result: {}'.format(dumps(decoded_event)))
            logger.warning(serializer.errors)


class MarketOrderReceiver(AbstractEventReceiver):
    def save(self, decoded_event, block_info):
        logger.info("Market Order Captured: {}".format(dumps(decoded_event)))


# contract instances
class CentralizedOracleInstanceReceiver(AbstractEventReceiver):

    def save(self, decoded_event, block_info):
        serializer = CentralizedOracleInstanceSerializer(data=decoded_event, block=block_info)
        if serializer.is_valid():
            serializer.save()
            logger.info('Centralized Oracle Instance Added: {}'.format(dumps(decoded_event)))
        else:
            logger.warning('INVALID Centralized Oracle Instance: {}'.format(dumps(decoded_event)))
            logger.warning(serializer.errors)


class EventInstanceReceiver(AbstractEventReceiver):

    # TODO, develop serializers
    events = {
        'Issuance': OutcomeTokenIssuanceSerializer, # sum to totalSupply, update data
        'Revocation': OutcomeTokenRevocationSerializer, # subtract from total Supply, update data
        'OutcomeTokenCreation': OutcomeTokenInstanceSerializer
    }

    def save(self, decoded_event, block_info=None):
        if block_info:
            serializer = self.events.get(decoded_event.get('name'))(data=decoded_event, block=block_info)
        else:
            serializer = self.events.get(decoded_event.get('name'))(data=decoded_event)

        if serializer.is_valid():
            serializer.save()
            logger.info('Event Instance Added: {}'.format(dumps(decoded_event)))
        else:
            logger.warning('INVALID Event Instance: {}'.format(dumps(decoded_event)))
            logger.warning(serializer.errors)


# TODO remove
# class OutcomeTokenReceiver(AbstractEventReceiver):
#
#     def save(self, decoded_event, block_info):
#         serializer = OutcomeTokenInstanceSerializer(data=decoded_event)
#         if serializer.is_valid():
#             serializer.save()
#             logger.info('Outcome Token Added: {}'.format(dumps(decoded_event)))
#         else:
#             logger.warning('INVALID Outcome Token: {}'.format(dumps(decoded_event)))
#             logger.warning(serializer.errors)
