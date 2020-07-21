from .base import Base

from .freedom import Freedom
from .harvey_norman import HarveyNorman
from .target import Target
from .treasure_box import TreasureBox
from .tsb_living import TsbLiving

SITE_NAMES = {
    "Freedom": Freedom,
    "Target": Target,
    "Harvey Norman": HarveyNorman,
    "Treasure Box": TreasureBox,
    "Tsb Living": TsbLiving
}
