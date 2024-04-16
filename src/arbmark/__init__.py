"""SSB Arbeidsmarked og lønn Fag-fellesfunksjoner."""

from arbmark.functions.aggregation import proc_sums
from arbmark.functions.files import read_latest
from arbmark.functions.interval import pinterval
from arbmark.functions.merge import indicate_merge
from arbmark.functions.quarter import first_last_date_quarter
from arbmark.functions.reference import ref_day
from arbmark.functions.reference import ref_week
from arbmark.functions.workdays import count_holidays
from arbmark.functions.workdays import count_weekenddays
from arbmark.functions.workdays import count_workdays
from arbmark.groups.age import alder_5grp
from arbmark.groups.age import alder_grp
from arbmark.groups.company_size import virk_str_8grp
from arbmark.groups.country_origin import landbakgrunn_grp
from arbmark.groups.nace import nace_sn07_47grp
from arbmark.groups.nace import nace_to_17_groups
from arbmark.groups.sector import sektor2_grp
from arbmark.groups.shift_work import turnuskoder

__all__ = [
    "proc_sums",
    "read_latest",
    "pinterval",
    "indicate_merge",
    "first_last_date_quarter",
    "ref_day",
    "ref_week",
    "count_workdays",
    "count_holidays",
    "count_weekenddays",
    "alder_grp",
    "alder_5grp",
    "virk_str_8grp",
    "landbakgrunn_grp",
    "nace_to_17_groups",
    "nace_sn07_47grp",
    "sektor2_grp",
    "turnuskoder",
]
