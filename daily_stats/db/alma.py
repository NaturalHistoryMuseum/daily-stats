# !/usr/bin/env python
# encoding: utf-8

from datetime import date as dateclass
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from daily_stats.db.base import Base


class AlmaCsfPackageComp(Base):
    __tablename__ = 'alma_csf_package_comp'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bib_level: Mapped[Optional[str]]
    collection: Mapped[Optional[str]]
    date: Mapped[Optional[dateclass]]
    record_count: Mapped[int] = mapped_column(default=0)
