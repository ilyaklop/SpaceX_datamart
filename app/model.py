from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, ForeignKey, Text, Integer, Boolean, TIMESTAMP, Date
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Missions(Base):
    __tablename__ = 'missions'
    id = Column(String(50), primary_key=True, unique=True)
    name = Column(String(255))
    website = Column(String(255))
    twitter = Column(String(255))
    description = Column(Text)
    wikipedia = Column(String(255))

    def __init__(self, mission_data):
        self.id = mission_data['id']
        self.title = mission_data['name']
        self.website = mission_data['website']
        self.twitter = mission_data['twitter']
        self.description = mission_data['description']
        self.wikipedia = mission_data['wikipedia']


class MissionManufactures(Base):
    __tablename__ = 'mission_manufactures'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    mission_id = Column(String(50), ForeignKey('missions.id'))
    manufacturer = Column(String(255))

    mission = relationship("Missions")

    def __init__(self, mission_id, manufacturer):
        self.mission_id = mission_id
        self.manufacturer = manufacturer


class Payloads(Base):
    __tablename__ = 'payloads'
    id = Column(String(50), primary_key=True, unique=True)
    manufacturer = Column(String(255))
    orbit = Column(String(255))
    nationality = Column(String(255))
    mass_kg = Column(Float)
    mass_lbs = Column(Float)
    type = Column(String(255))
    reused = Column(Boolean)

    def __init__(self, payload_data):
        self.id = payload_data['id']
        self.manufacturer = payload_data['manufacturer']
        self.orbit = payload_data['orbit']
        self.nationality = payload_data['nationality']
        self.mass_kg = payload_data['payload_mass_kg']
        self.mass_lbs = payload_data['payload_mass_lbs']
        self.type = payload_data['payload_type']
        self.reused = payload_data['reused']


class MissionPayloads(Base):
    __tablename__ = 'mission_payloads'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    mission_id = Column(String(50), ForeignKey('missions.id'))
    payload_id = Column(String(50), ForeignKey('payloads.id'))
    payload = relationship("Payloads")
    mission = relationship("Missions")

    def __init__(self, mission_id, payload_id):
        """Связь many to many реализана именно так ввиду отсутствия у метода session.add() возможности добавлять строки
        с учетом первичного ключа"""
        self.mission_id = mission_id
        self.payload_id = payload_id


class Launches(Base):
    __tablename__ = 'launches'
    id = Column(Integer, primary_key=True)
    details = Column(Text)
    is_tentative = Column(Boolean)
    launch_date_local = Column(TIMESTAMP)
    launch_date_unix = Column(Integer)
    launch_date_utc = Column(TIMESTAMP)
    launch_success = Column(Boolean)
    launch_year = Column(String(10))
    mission_name = Column(String(255))
    static_fire_date_unix = Column(Integer)
    static_fire_date_utc = Column(TIMESTAMP)
    tentative_max_precision =Column(String(255))
    upcoming = Column(Boolean)

    def __init__(self, launches_data):
        self.id = launches_data['id']
        self.is_tentative = launches_data['is_tentative']
        self.tentative_max_precision = launches_data['tentative_max_precision']
        self.upcoming = launches_data['upcoming']
        self.static_fire_date_utc = launches_data['static_fire_date_utc']
        self.static_fire_date_unix = launches_data['static_fire_date_unix']
        self.mission_name = launches_data['mission_name']
        self.launch_year = launches_data['launch_year']
        self.launch_success = launches_data['launch_success']
        self.launch_date_utc = launches_data['launch_date_utc']
        self.launch_date_unix = launches_data['launch_date_unix']
        self.launch_date_local = launches_data['launch_date_local']
        self.details = launches_data['details']


class LaunchSites(Base):
    __tablename__ = 'launch_sites'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    launch_id = Column(Integer, ForeignKey('launches.id'))
    site_id = Column(String(255))
    site_name = Column(String(255))
    site_name_long = Column(String(255))

    launch = relationship("Launches")

    def __init__(self, launch_id, site_dict):
        self.launch_id = launch_id
        self.site_id = site_dict['site_id']
        self.site_name = site_dict['site_name']
        self.site_name_long = site_dict['site_name_long']


class Links(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    launch_id = Column(Integer, ForeignKey('launches.id'))
    article_link = Column(String)
    mission_patch = Column(String)
    mission_patch_small = Column(String)
    presskit = Column(String)
    reddit_campaign = Column(String)
    reddit_launch = Column(String)
    reddit_media = Column(String)
    reddit_recovery = Column(String)
    video_link = Column(String)
    wikipedia = Column(String)

    launch = relationship('Launches')
    def __init__(self, launch_id, links_object):
        self.launch_id = launch_id
        self.article_link = links_object['article_link']
        self.mission_patch = links_object['mission_patch']
        self.mission_patch_small = links_object['mission_patch_small']
        self.presskit = links_object['presskit']
        self.reddit_campaign = links_object['reddit_campaign']
        self.reddit_launch = links_object['reddit_launch']
        self.reddit_media = links_object['reddit_media']
        self.reddit_recovery = links_object['reddit_recovery']
        self.video_link = links_object['video_link']
        self.wikipedia = links_object['video_link']


class LaunchMissions(Base):
    """Возможно сюда следует добавить имена миссий для сравнения. Они отличаются от запуска к запуску.
    Решение - добавить витрину с миссиями по запускам"""
    __tablename__ = 'launch_missions'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    launch_id = Column(Integer, ForeignKey('launches.id'))
    mission_id = Column(String(50), ForeignKey('missions.id'))

    launch = relationship('Launches')
    mission = relationship('Missions')

    def __init__(self, launch_id, mission_id):
        self.launch_id = launch_id
        self.mission_id = mission_id


class LaunchPhotos(Base):
    __tablename__ = 'launch_photos'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    launch_id = Column(Integer, ForeignKey('launches.id'))
    flickr_images = Column(String(255))

    launch = relationship("Launches")
    def __init__(self, launch_id, image):
        self.launch_id = launch_id
        self.flickr_images = image


class Rockets(Base):
    __tablename__ = 'rockets'
    id = Column(String(50), primary_key=True)
    active = Column(Boolean)
    boosters = Column(Integer)
    company = Column(String(255))
    cost_per_launch = Column(Float)
    country = Column(String(255))
    description = Column(Text)
    diameter_feet = Column(Float)
    diameter_meters = Column(Float)
    first_flight = Column(Date)
    height_feet = Column(Float)
    height_meters = Column(Float)
    landing_legs_number = Column(Integer)
    landing_legs_material = Column(String(255), nullable=True)
    mass_kg = Column(Float)
    mass_lb = Column(Float)
    name = Column(String(255))
    stages = Column(Integer)
    success_rate_pct = Column(Integer)
    type = Column(String(255))
    wikipedia = Column(String(255))

    def __init__(self, rocket_data):
        self.id = rocket_data['id']
        self.active = rocket_data['active']
        self.boosters = rocket_data['boosters']
        self.company = rocket_data['company']
        self.cost_per_launch = rocket_data['cost_per_launch']
        self.country = rocket_data['country']
        self.description = rocket_data['description']
        self.diameter_feet = rocket_data['diameter']['feet']
        self.diameter_meters = rocket_data['diameter']['meters']
        self.first_flight = rocket_data['first_flight']
        self.height_feet = rocket_data['height']['feet']
        self.height_meters = rocket_data['height']['meters']
        self.landing_legs_number = rocket_data['landing_legs']['number']
        self.landing_legs_material = rocket_data['landing_legs']['material']
        self.mass_kg = rocket_data['mass']['kg']
        self.mass_lb = rocket_data['mass']['lb']
        self.name = rocket_data['name']
        self.stages = rocket_data['stages']
        self.success_rate_pct = rocket_data['success_rate_pct']
        self.type = rocket_data['type']
        self.wikipedia = rocket_data['wikipedia']


class LaunchRocket(Base):
    __tablename__ = 'launch_rocket'
    id = Column(Integer, primary_key=True, autoincrement="auto")
    launch_id = Column(Integer, ForeignKey('launches.id'))
    rocket_id = Column(String(50), ForeignKey('rockets.id'))

    launch = relationship('Launches')
    rocket = relationship('Rockets')

    def __init__(self, launch_id, rocket_id):
        self.launch_id = launch_id
        self.rocket_id = rocket_id
