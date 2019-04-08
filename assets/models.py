from django.contrib.postgres.fields import JSONField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError

from django.db import models


class AttrWrapper(object):
    def __init__(self, asset):
        self.asset = asset

    def __getattr__(self, item):
        return self.asset.data[item]

    def __setattr__(self, key, value):
        if key == "asset":
            object.__setattr__(self, key, value)
            return
        # we rely on the caller to save, when all attrs updated
        self.asset.data[key] = value


class AssetManager(models.Manager):
    def create(self, *args, **kwargs):
        # grab the first postional params
        args = list(args)
        domain = args.pop(0)
        kls_name = args.pop(0)
        name = args.pop(0)

        # grab the kls, and build an asset
        kls = AssetClass.objects.filter(name=kls_name, domain=domain.pk).first()
        ass = super().create(*args, **dict(name=name, kls=kls))

        # add the attrs
        attrs = Attribute.objects.filter(asset_class=kls.pk).all()
        attr_names = [a.name for a in attrs]
        jdict = {}
        for k, v in kwargs.items():
            if k in attr_names:
                jdict[k] = v
        ass.data = jdict
        ass.save()
        return ass


class Asset(models.Model):
    objects = AssetManager()

    name = models.CharField(
        max_length=50, validators=[MinLengthValidator(1), MaxLengthValidator(50)]
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    kls = models.ForeignKey(
        "AssetClass", on_delete=models.CASCADE, related_name="instances"
    )
    data = JSONField(default=dict())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrapper = AttrWrapper(self)

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name) < 1:
            raise ValidationError({"name": "asset name not provided"})
        if self.parent == self:
            raise ValidationError({"parent": "asset contains itself"})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    @property
    def attr(self):
        return self.wrapper


class Domain(models.Model):
    name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1), MaxLengthValidator(20)]
    )

    def clean(self):
        if len(self.name) < 1:
            raise ValidationError({"name": "domain name not provided"})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def create_asset(self, kls_name, name, **kwargs):
        ass = Asset.objects.create(self, kls_name, name, vin="01")
        return ass


class AssetClass(models.Model):
    name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1), MaxLengthValidator(20)]
    )
    domain = models.ForeignKey(
        Domain, on_delete=models.CASCADE, null=True, related_name="asset_classes"
    )

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name) < 1:
            raise ValidationError({"name": "AssetClass name not provided"})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class Attribute(models.Model):
    name = models.CharField(
        max_length=20, validators=[MinLengthValidator(1), MaxLengthValidator(20)]
    )
    asset_class = models.ForeignKey(
        AssetClass, on_delete=models.CASCADE, null=True, related_name="attributes"
    )

    def __str__(self):
        return self.name

    def clean(self):
        if len(self.name) < 1:
            raise ValidationError({"name": "Attribute name not provided"})

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
