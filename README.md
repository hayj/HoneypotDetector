# HoneypotDetector

This tool can recognize honeypot urls using selenium to prevent bot detection.

## Installation

	git clone git@github.com:hayj/HoneypotDetector.git
	pip install ./HoneypotDetector/wm-dist/*.tar.gz

## Vocabulary

 * href : a string url
 * link : a selenium element which is a "a" markup

## Usage

	from honeypotdetector.detector import *
	honeypotDetector = HoneypotDetector()
	# Get all links on the page (this method takes a lot of processing time,
	# depending on the number of links in the page, see below for more informations):
    (safeHref, honeypotHref) = honeypotDetector.getHrefs(seleniumDriver, removeExternal=True)
    # Or check a unique link element:
    honeypotDetector.isHoneypot(seleniumDriver.find_elements_by_css_selector("#id a"))
    # Or check a unique href giving the driver (if this href does not exist on the
    # page, the method will return False (i.e. not a honeypot)):
    honeypotDetector.isHoneypot("http://test.com", seleniumDriver)


## Multiprocessing

At this day we are not able to run in parallel the feature extraction on selenium links because selenium drivers (or elements) are not pickable, even with Dill and Pathos.

 * <https://stackoverflow.com/questions/25208188/pickling-selenium-webdriver-objects>
 * <https://stackoverflow.com/questions/47275036/cant-pickle-local-object-while-trying-multiprocessing>
 * <https://github.com/uqfoundation/dill/issues/178>
 * <https://stackoverflow.com/questions/8804830/python-multiprocessing-pickling-error>

The feature extraction is very slow but a cache mechanism is implemented in the class so you can quickly re-execute getLinks() several time. But it seems ajax content load will re-alloc new links element in the selenium object so the cache feature is no reliable in the case the page's DOM change.