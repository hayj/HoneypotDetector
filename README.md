# Description

This tool can recognize honeypot urls using selenium to prevent bot detection.

# Installation

    pip install ./wm-dist/*.tar.gz

# Vocabulary

 * href : a string url
 * link : a selenium element which is a "a" markup

# Usage

	from honeypotdetector.detector import *
	honeypotDetector = HoneypotDetector()
	# Get all links on the page (this method take a lot of processing time, depending on the number of links in the page, see below for more informations):
    (safeHref, honeypotHref) = honeypotDetector.getLinks(seleniumDriver, removeExternal=True)
    # Or check a unique link element:
    honeypotDetector.isHoneypot(driver.find_elements_by_css_selector("#id a"))
    # Or check a unique href giving the driver (if this href does not exist on the page, the method will return False (= not a honeypot)):
    honeypotDetector.isHoneypot("http://test.com", driver)


# Multiprocessing

At this day we are not able to run the feature extraction on selenium links because selenium drivers (or elements) are not pickable, even with Dill and Pathos.

 * <https://stackoverflow.com/questions/25208188/pickling-selenium-webdriver-objects>
 * <https://stackoverflow.com/questions/47275036/cant-pickle-local-object-while-trying-multiprocessing>
 * <https://github.com/uqfoundation/dill/issues/178>
 * <https://stackoverflow.com/questions/8804830/python-multiprocessing-pickling-error>

The feature extraction is very slow but a cache mechanism is implemented in the class so you can quickly re-execute getLinks() several time, for example in the case you get ajax content...