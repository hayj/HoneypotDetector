# Description

This tool can recognize honeypot urls using selenium to prevent bot detection.

# Dependencies

    pip install ./wm-dist/*.tar.gz

# Usage

	from honeypotdetector.detector import *
	honeypotDetector = HoneypotDetector()
    (safeLinks, honeypotLinks) = honeypotDetector.getLinks(seleniumDriver, removeExternal=True)