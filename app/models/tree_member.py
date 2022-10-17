from asyncio import FastChildWatcher
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Sequence, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, BIGINT

from models.tree_base import Base, TreeBase


class TreeMember(Base, TreeBase):

    __tablename__ = "TreeMember"

    id = Column(String(2048), primary_key=True)
    json = Column(JSONB)
    rdf = Column(Text)
    collection_id = Column("collection_id", ForeignKey("TreeCollection.id"))

    nr = Column(BIGINT, Sequence('seq_member_nr', schema='public'), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    #todo: Add PostGIS stuff (see https://geoalchemy.readthedocs.io/)

    def __repr__(self):
        return f"<{self.id}> a tree:member ."

