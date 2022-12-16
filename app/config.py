DB_NAME = 'spaceX'
USER = 'iliaklop'
PASS = 'postpass'
HOST = 'postgres'
PORT = '5432'

QUERY_MISSIONS = """{
  missions {
    payloads {
      id
      manufacturer
      nationality
      orbit
      payload_mass_kg
      payload_mass_lbs
      payload_type
      reused
    }
    id
    description
    name
    manufacturers
    twitter
    website
    wikipedia
  }
}
"""

QUERY_LAUNCHES = """{
  launches {
    details
    id
    is_tentative
    launch_date_local
    launch_date_unix
    launch_date_utc
    launch_success
    launch_year
    mission_id
    mission_name
    static_fire_date_unix
    static_fire_date_utc
    tentative_max_precision
    upcoming
    rocket {
      rocket {
        id
      }
    }
    launch_site {
      site_id
      site_name
      site_name_long
    }
    links {
      article_link
      flickr_images
      mission_patch
      mission_patch_small
      presskit
      reddit_campaign
      reddit_launch
      reddit_media
      video_link
      wikipedia
      reddit_recovery
    }
  }
}
"""

QUERY_ROCKETS = """{
  rockets {
    active
    boosters
    company
    cost_per_launch
    country
    description
    diameter {
      feet
      meters
    }
    first_flight
    height {
      feet
      meters
    }
    id
    landing_legs {
      material
      number
    }
    mass {
      kg
      lb
    }
    name
    stages
    success_rate_pct
    type
    wikipedia
  }
}
"""