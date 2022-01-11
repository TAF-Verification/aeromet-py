import re
from typing import List

from ..models import *


class Metar(Report):
    """Parser for METAR reports."""
