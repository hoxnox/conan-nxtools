import os
from shutil import copy
from conans import tools

def retrieve(sha256, locations, saveas):
    vendor_dir = os.getenv("VENDOR_DIR", "~/.vendor")
    last_location = None
    for location in locations:
        try:
            if location[:4] == "http":
                tools.download(location, saveas)
            elif location[:9] == "vendor://":
                location = '{vendor_dir}/{location}'.format(location=location[9:],
                                                            vendor_dir=vendor_dir)
                copy(location, saveas)
            else:
                copy(location, saveas)
            last_location = location
            tools.check_sha256(saveas, sha256)
            break
        except:
            continue
    if not last_location:
        return
    tools.untargz(saveas)
    os.unlink(saveas)
