# !/usr/bin/env python
# encoding: utf-8

from datetime import date as dateclass
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from daily_stats.db.base import Base


class PackageComp(Base):
    __tablename__ = 'package_comp'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Optional[dateclass]]
    pkg_name: Mapped[Optional[str]] = mapped_column(String(250))
    pkg_title: Mapped[Optional[str]] = mapped_column(String(250))
    pkg_type: Mapped[Optional[str]] = mapped_column(String(20))
    record_count: Mapped[int]
