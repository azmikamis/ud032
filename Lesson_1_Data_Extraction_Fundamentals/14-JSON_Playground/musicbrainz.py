# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    print("How many bands named 'First Aid Kit'?")
    data = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    artists = [a for a in data["artists"] if a["name"]=="First Aid Kit"]
    print(len(artists))

    print("Begin-area name for Queen")
    data = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    artists = [a for a in data["artists"] if a["name"]=="Queen"]
    artist_id = artists[0]["id"]
    artist_data = query_site(ARTIST_URL, query_type["simple"], artist_id)
    beginarea = artist_data["begin_area"]
    print(beginarea["name"])

    print("Spanish alias for Beatles")
    data = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    artists = [a for a in data["artists"] if a["name"]=="The Beatles"]
    artist_id = artists[0]["id"]
    artist_data = query_site(ARTIST_URL, query_type["aliases"], artist_id)
    aliases = artist_data["aliases"]
    spanishalias = [a for a in aliases if a["locale"]=="es"][0]["name"]
    print(spanishalias)

    print("Nirvana disambiguation")
    data = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    artists = [a for a in data["artists"] if a["name"]=="Nirvana"]
    artist_id = artists[0]["id"]
    artist_data = query_site(ARTIST_URL, query_type["simple"], artist_id)
    disambiguation = artist_data["disambiguation"]
    print(disambiguation)

    print("When was One Direction formed")
    data = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    artists = [a for a in data["artists"] if a["name"]=="One Direction"]
    artist_id = artists[0]["id"]
    artist_data = query_site(ARTIST_URL, query_type["simple"], artist_id)
    formed = artist_data["life-span"]["begin"]
    print(formed)


if __name__ == '__main__':
    main()
