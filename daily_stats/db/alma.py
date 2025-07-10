# !/usr/bin/env python
# encoding: utf-8

from datetime import date as dt

from sqlalchemy.orm import Mapped, mapped_column

from daily_stats.db.base import Base


class AlmaCsfPackageComp(Base):
    __tablename__ = 'alma_csf_package_comp'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bib_level: Mapped[str]
    collection: Mapped[str]
    date: Mapped[dt]
    record_count: Mapped[int] = mapped_column(default=0)
