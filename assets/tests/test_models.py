from django.core.exceptions import ValidationError
from django.test import TestCase
import pytest

pytestmark = pytest.mark.django_db


# Asset ----------------------------


def test_can_import_asset():
    from ..models import Asset

    assert Asset


# naïve hierarchy behaviour


# def test_parent_field_defaults_to_none():
#     from .factories import AssetFactory
#
#     from assets.tests.factories import AssetClassFactory
#
#     thing_kls = AssetClassFactory(name='thing')
#     a = AssetFactory(name='some thing', kls=thing_kls)
#     assert a.parent is None
#
#
# def test_sub_assembly_can_be_added():
#     from .factories import AssetFactory
#     from assets.tests.factories import AssetClassFactory
#
#     part_kls = AssetClassFactory(name='part')
#
#     a = AssetFactory(name="car01", kls=part_kls)
#     b = AssetFactory(name="chassis", kls=part_kls)
#     b.parent = a
#     b.save()
#
#     assert b.parent == a
#     assert a.children.all()[0] == b
#     assert a.children.first() == b
#
#
# def test_asset_cannot_contain_itself():
#     from .factories import AssetFactory
#     from assets.tests.factories import AssetClassFactory
#
#     part_kls = AssetClassFactory(name='part')
#
#     a = AssetFactory(name="car01", kls=part_kls)
#     a.parent = a
#     with pytest.raises(ValidationError):
#         a.save()
#

# Domain ----------------------------


def test_can_import_domain():
    from ..models import Domain

    assert Domain


# naïve field-related behaviour


def test_domain_has_a_name():
    from ..models import Domain

    a = Domain.objects.create(name="Domain")
    assert a.name


def test_non_empty_domain_name_is_mandatory():
    from ..models import Domain

    a = Domain(name="")
    with pytest.raises(ValidationError):
        a.save()


# domain factory


def test_check_domain_factory_exists():
    from .factories import DomainFactory

    a = DomainFactory()
    assert a.name


# naïve hierarchy behaviour


def test_domain_has_asset_classes_attribute():
    from .factories import DomainFactory

    a = DomainFactory(name="vehicles")

    assert a.asset_classes.all().count() == 0
    assert a.asset_classes.first() is None


# AssetClass ----------------------------


def test_can_import_asset_class():
    from ..models import AssetClass

    assert AssetClass


# naïve field-related behaviour


def test_asset_class_has_a_name():
    from ..models import AssetClass

    a = AssetClass.objects.create(name="AssetClass")
    assert a.name


def test_non_empty_asset_class_name_is_mandatory():
    from ..models import AssetClass

    a = AssetClass(name="")
    with pytest.raises(ValidationError):
        a.save()


# assetClass factory


def test_check_asset_class_factory_exists():
    from .factories import AssetClassFactory

    a = AssetClassFactory()
    assert a.name


# naïve hierarchy behaviour


def test_asset_class_has_attributes_attr():
    from .factories import AssetClassFactory

    a = AssetClassFactory(name="automobile")

    assert a.attributes.all().count() == 0
    assert a.attributes.first() is None


# Attr ----------------------------


def test_can_import_attribute():
    from ..models import Attribute

    assert Attribute


# naïve field-related behaviour


def test_attribute_has_a_name():
    from ..models import Attribute

    a = Attribute.objects.create(name="Attribute")
    assert a.name


def test_non_empty_attribute_name_is_mandatory():
    from ..models import Attribute

    a = Attribute(name="")
    with pytest.raises(ValidationError):
        a.save()


# attribute factory


def test_check_attribute_factory_exists():
    from .factories import AttributeFactory

    a = AttributeFactory()
    assert a.name


# using the attribute system ----------------------


def build_automotive_domain():
    from assets.tests.factories import (
        DomainFactory,
        AssetClassFactory,
        AttributeFactory,
    )

    domain = DomainFactory(name="automotive")
    car_class = AssetClassFactory(name="car")
    domain.asset_classes.add(car_class)
    vin_attribute = AttributeFactory(name="vin")
    car_class.attributes.add(vin_attribute)
    return domain


def test_use_automotive_domain_to_create_minimal_car():
    domain = build_automotive_domain()
    car = domain.create_asset("car", "my-car")
    assert car


def test_use_automotive_domain_to_create_minimal_car_and_modify_attr_then_search():
    from ..models import Asset

    domain = build_automotive_domain()
    car = domain.create_asset("car", "my-car", vin="01")
    assert car
    assert car.attr.vin == "01"

    car.attr.vin = "02"
    car.save()
    assert car.attr.vin == "02"

    car = Asset.objects.filter(data__vin="02").first()
    assert car is not None


# TODO

# mandatory json attributes by class
# json attribute inheritance - acquisition
# detach
# break parent link
# attach
# set parent link
# remove location - because that will inherit from parent
# remove custodian - because that will inherit from parent

# car: length, width
# engine: type(diesel/petrol/electric), serial, location
