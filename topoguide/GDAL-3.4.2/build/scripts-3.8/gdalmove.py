#!/Users/simon/EISC-209/topoguide-simon-beguin-groupe/venv/bin/python

import sys
# import osgeo_utils.gdalmove as a convenience to use as a script
from osgeo_utils.gdalmove import *  # noqa
from osgeo_utils.gdalmove import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdalmove')
sys.exit(main(sys.argv))
