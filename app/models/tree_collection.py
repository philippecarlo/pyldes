from enum import unique
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.tree_base import Base, TreeBase

class TreeCollection(Base, TreeBase):

    __tablename__ = "TreeCollection"

    id = Column(String(2048), primary_key=True)
    alias = Column(String(50), unique=True)
    title = Column(String(1024), nullable=True)
    shape = Column(Text, nullable=True)
    member_frame = Column(Text, nullable=True)

    # relationships
    views = relationship("TreeView")
    #members = relationship("TreeMember")

    def __repr__(self):
        return f"<{self.id}> a tree:collection ."

