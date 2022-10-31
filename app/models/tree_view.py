from importlib.metadata import requires
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.tree_base import Base, TreeBase


class TreeView(Base, TreeBase):

    __tablename__ = "TreeView"

    id = Column(String(2048), primary_key=True)
    collection_id = Column("collection_id", ForeignKey("TreeCollection.id"))
    
    fragmentation_kind = Column(String(2048))
    max_node_size = Column(Integer, nullable=True)
    path = Column(String(2048))
    alias = Column(String(50), unique=True)
    sequence_type = Column(String(50))

    # relationships
    collection = relationship("TreeCollection", back_populates="views")

    def __repr__(self):
        return f"<{self.id}> a tree:collection ."
