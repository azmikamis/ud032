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
    data = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    tmp = [a for a in data["artists"] if a["name"]=="First Aid Kit"]
    result1 = len(tmp)

    data = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    tmp = [a for a in data["artists"] if a["name"]=="Queen"]
    tmp = [a.get("begin-area",{}) for a in tmp]
    tmp = [a for a in tmp if a != {} ]
    result2 = tmp[0]["name"]

    data = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    tmp = [a for a in data["aliases"] if a["name"]=="Beatles"]
    print(tmp)
#    artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
#    releases = artist_data["releases"]
#    print "\nONE RELEASE:"
#    pretty_print(releases[0], indent=2)
#    release_titles = [r["title"] for r in releases]
#
#    print "\nALL TITLES:"
#    for t in release_titles:
#        print t



if __name__ == '__main__':
    main()
