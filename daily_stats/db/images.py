# !/usr/bin/env python
# encoding: utf-8

from datetime import date as dateclass
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from daily_stats.db.base import Base


class SpecimenImages(Base):
    __tablename__ = 'specimen_images'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[Optional[dateclass]]
    image_count: Mapped[int] = mapped_column(default=0)
    imaged_specimens: Mapped[int]
    resource_id: Mapped[Optional[str]] = mapped_column(String(50))
