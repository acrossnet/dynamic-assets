import random
import string
import typing

from factory import DjangoModelFactory, Faker, SubFactory, post_generation, Sequence

from assets.models import Asset, Domain, AssetClass, Attribute

"""
information on Faker providers here:
https://faker.readthedocs.io/en/latest/providers/faker.providers.python.html
"""


class AssetFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Part %03d" % n)

    class Meta:
        model = Asset


class DomainFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Domain %03d" % n)

    class Meta:
        model = Domain


class AssetClassFactory(DjangoModelFactory):

    name = Sequence(lambda n: "AssetClass %03d" % n)

    class Meta:
        model = AssetClass


class AttributeFactory(DjangoModelFactory):

    name = Sequence(lambda n: "Attribute %03d" % n)

    class Meta:
        model = Attribute
