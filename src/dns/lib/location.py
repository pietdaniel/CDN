import urllib2, json, math
import src.config as conf

GEOIP_API = "http://www.telize.com/geoip/"
replicas = conf.config().replica_map

def get_location(ip_address):
    try:
        response = urllib2.urlopen(GEOIP_API + ip_address)
        blob = json.load(response)
        return blob
    except urllib2.HTTPError as e:
        print "Failed to get location, I am sorry master"
        return False

def get_lat_long(ip_address):
    ip_response = get_location(ip_address)
    if ip_response:
        try:
            latip, lngip = (ip_response['latitude'], ip_response['longitude'])
            return (latip, lngip)
        except:
            print "Failed to get latitude, longitude from response"
            return False

def get_closest(ip_address):
    latip, lngip = (None, None)
    llpair = get_lat_long(ip_address)

    if llpair:
        latip, lngip = llpair
    else:
        return False

    min_dist = 100000000000000
    closest = (None, None)

    for key in replicas:
        lat, lng = replicas[key][2]
        new_dist = geo_dist(lat, lng, latip, lngip)
        if new_dist < min_dist:
            min_dist = new_dist
            closest = {key: replicas[key]}

    return closest

def geo_dist(lat1, long1, lat2, long2, km=True):
    to_radians = math.pi/180.0

    phi1 = (90.0 - lat1) * to_radians
    phi2 = (90.0 - lat2) * to_radians

    theta1 = long1 * to_radians
    theta2 = long2 * to_radians

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
            math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    if km:
        return arc * 6373
    else:
        return arc * 3960
