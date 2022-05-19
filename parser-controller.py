#!/usr/bin/python3

from lib.PriceDataParser import PriceDataParser

priceDataParser = PriceDataParser('./config.json')
priceDataParser.run()