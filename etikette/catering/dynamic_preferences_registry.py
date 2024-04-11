from decimal import Decimal

from dynamic_preferences.types import StringPreference, DecimalPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

credits = Section('Credits')
tiers = Section('Tiers')

