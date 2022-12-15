DB_NAME = 'spaceX'
USER = 'iliaklop'
PASS = 'postpass'
HOST = 'db'
PORT = '5432'

QUERY_MISSIONS ="""{
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