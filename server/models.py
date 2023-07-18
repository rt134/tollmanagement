from django.db import models
from django.utils import timezone
from datetime import timedelta


class Pricing(models.Model):
    PASS_CHOICES = (
        (1, "Single Pass"),
        (2, "Return Pass"),
        (3, "Seven Day Pass")
    )
    pass_type = models.IntegerField(
        choices=PASS_CHOICES,
        unique=True
    )
    fare = models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )

    def __str__(self):
        return str(self.pass_type)


class Toll(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    location = models.CharField(
        max_length=100,
        null=False,
        blank=False,
    )
    
    def __str__(self):
        return self.name


class Booth(models.Model):
    parent = models.ForeignKey(
        Toll, 
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
    )
    
    def __str__(self):
        return str(self.id) + " - " +self.parent.name


class Vehicle(models.Model):
    VEHICLE_CHOICES = (
        (1, "Two Wheeler"),
        (2, "Four Wheeler"),
    )
    reg_no = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
    )
    vehicle_type = models.IntegerField(
        choices=VEHICLE_CHOICES,
        null=False,
        blank=False,
    )
    
    def __str__(self):
        return self.reg_no


class Pass(models.Model):
    PASS_CHOICES = (
        (1, "Single Pass"),
        (2, "Return Pass"),
        (3, "Seven Day Pass")
    )

    pass_type = models.IntegerField(
        choices=PASS_CHOICES,
        null=False,
        blank=False
    )
    toll = models.ForeignKey(
        Toll, 
        on_delete=models.CASCADE
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        null=True,
        blank=True, 
        editable=True
    )

    created_at = models.DateTimeField(
        default=timezone.now, 
        editable=False
    )

    valid_till = models.DateTimeField(
        null=True, 
        blank=True, 
        editable=True
    )
    
    def __str__(self):
        return str(self.pass_type) + " - " + str(self.vehicle.reg_no)

    def save(self, *args, **kwargs):
        pricing_factor = Pricing.objects.get(pass_type=self.pass_type).fare
        if self.pass_type == 1:
            self.price = pricing_factor * self.vehicle.vehicle_type
            self.valid_till = timezone.now()
        elif self.pass_type == 2:
            self.price = pricing_factor * self.vehicle.vehicle_type
            self.valid_till = timezone.now() + timedelta(days=1)
        else:
            self.price = pricing_factor * self.vehicle.vehicle_type
            self.valid_till = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)


class Leaderboard(models.Model):
    booth = models.OneToOneField(
        Booth, 
        on_delete=models.CASCADE
    )
    vehicles_passed = models.PositiveIntegerField(
        default=0
    )
    toll_charges_collected = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    
    def __str__(self):
        return f"Leaderboard for {self.booth}"
