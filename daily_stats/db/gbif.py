# !/usr/bin/env python
# encoding: utf-8

from datetime import date as dateclass
from typing import Optional

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from daily_stats.db.base import Base


class GBIFCitation(Base):
    __tablename__ = 'gbif_citation'

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    abstract: Mapped[Optional[str]]
    authors: Mapped[Optional[str]]
    countries_of_researcher: Mapped[Optional[str]]
    doi: Mapped[Optional[str]] = mapped_column(String(55))
    harvest_date: Mapped[Optional[dateclass]]
    language: Mapped[Optional[str]] = mapped_column(String(5))
    literature_type: Mapped[Optional[str]] = mapped_column(String(50))
    month: Mapped[Optional[int]]
    nhm_record_count: Mapped[Optional[int]]
    open_access: Mapped[Optional[str]] = mapped_column(String(50))
    peer_review: Mapped[Optional[str]] = mapped_column(String(50))
    pub_date: Mapped[Optional[dateclass]]
    publisher: Mapped[Optional[str]] = mapped_column(String(200))
    source: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    topics: Mapped[Optional[str]] = mapped_column(String(200))
    total_dataset_count: Mapped[Optional[int]]
    total_record_count: Mapped[Optional[int]] = mapped_column(BigInteger)
    update_date: Mapped[Optional[dateclass]]
    year: Mapped[Optional[int]]


class GBIFBibliometrics(Base):
    __tablename__ = 'gbif_bibliometrics'

    index: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    doi: Mapped[Optional[str]] = mapped_column(String(55))
    times_cited: Mapped[Optional[int]]
    field_citation_ratio: Mapped[Optional[float]]
    relative_citation_ratio: Mapped[Optional[float]]
    harvest_date: Mapped[Optional[dateclass]]
