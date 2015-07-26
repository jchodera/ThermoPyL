import os
import feedparser
from utils import make_path
from six.moves import urllib_parse, urllib

THERMOML_FEEDS = {
"jced":"http://trc.nist.gov/RSS/jced.xml",
"jct":"http://trc.nist.gov/RSS/jct.xml",
"fpe":"http://trc.nist.gov/RSS/fpe.xml",
"tca":"http://trc.nist.gov/RSS/tca.xml",
"ijt":"http://trc.nist.gov/RSS/ijt.xml"
}


def update_archive(thermoml_path=None):
    """Use RSS feeds to find and download any missing ThermoML XML files
    from the ThermoML archive.

    Parameters
    ----------
    thermoml_path : str, optional, default=None
        If specified, use this path to store ThermoML XML files.  If None,
        use the THERMOML_PATH environment variable.
    """
    if thermoml_path is None:
        # Try to obtain the path to the local ThermoML Archive mirror from an environment variable.
        try:
            # Check THERMOML_PATH environment variable
            XML_PATH = os.environ["THERMOML_PATH"]
        except:
            # Use default path of ~/.thermoml
            XML_PATH = os.path.join(os.environ["HOME"], '.thermoml')

    # Update local repository according to feeds.
    for key, url in THERMOML_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed["entries"]:
            link = entry["link"]
            base_filename = urllib_parse.urlsplit(link).path
            base_filename = base_filename[1:]  # Strip off preceeding backslash character so os.path.join will work
            filename = os.path.join(thermoml_path, base_filename)
            make_path(filename)
            if os.path.exists(filename):
                print("Already downloaded %s from %s" % (filename, link))
            else:
                print("Fetching %s from %s" % (filename, link))
                urllib.request.urlretrieve (link, filename)

