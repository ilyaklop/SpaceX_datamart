from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Table, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

missions_payloads = Table("missions_payloads", Base.metadata,
                          Column('mission_id', String, ForeignKey('missions.id')),
                          Column('payload_id', String, ForeignKey('payloads.id')))

class Missions(Base):
    __tablename__ = 'missions'
    id = Column(String(50), primary_key=True, unique=True)
    name = Column(String(255))
    website = Column(String(255))
    twitter = Column(String(255))
    description = Column(Text)
    wikipedia = Column(String(255))
    payload_id = relationship("Payloads", secondary=missions_payloads, backref=backref('payloads', lazy='dynamic'),
                              single_parent=True)

    def __init__(self, mission_data):
        self.id = mission_data['id']
        self.title = mission_data['name']
        self.website = mission_data['website']
        self.twitter = mission_data['twitter']
        self.description = mission_data['description']
        self.wikipedia = mission_data['wikipedia']

class Mission_manufactures(Base):
    __tablename__ = 'mission_manufactures'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    mission_id = Column(String(50), ForeignKey('missions.id'))
    manufacturer = Column(String(255))

    mission = relationship("Missions")

    def __init__(self, mission_id, manufacturer):
        self.mission_id = mission_id
        self.manufacturer = manufacturer

#class Mission_payloads(Base):
#    __tablename__ = 'mission_payloads'
#    mission_id = Column(String, ForeignKey('missions.id'))
#    payload_id = Column(String)
#
#    def __init__(self, mission_id, payload_dict):
#        self.mission_id = mission_id
#        self.payload_id = payload_dict['id']

class Payloads(Base):
    __tablename__ = 'payloads'
    id = Column(String(50), primary_key=True, unique=True)
    manufacturer = Column(String(255))
    orbit = Column(String(255))
    nationality = Column(String(255))
    mass_kg = Column(Float)
    mass_lbs = Column(Float)
    type = Column(String(255))
    reused = Column(String(255))

    def __init__(self, payload_data):
        self.id = payload_data['id']
        self.manufacturer = payload_data['manufacturer']
        self.orbit = payload_data['orbit']
        self.nationality = payload_data['nationality']
        self.mass_kg = payload_data['payload_mass_kg']
        self.mass_lbs = payload_data['payload_mass_lbs']
        self.type = payload_data['payload_type']
        self.reused = payload_data['reused']