#!/Users/simon/EISC-209/topoguide-simon-beguin-groupe/venv/bin/python

import sys
# import osgeo_utils.gdalattachpct as a convenience to use as a script
from osgeo_utils.gdalattachpct import *  # noqa
from osgeo_utils.gdalattachpct import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdalattachpct')
sys.exit(main(sys.argv))