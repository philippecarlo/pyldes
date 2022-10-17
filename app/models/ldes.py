from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.tree_collection import TreeCollection

class Ldes(TreeCollection):

    def __repr__(self):
        return f"<{self.id}> a ldes:eventstream ."