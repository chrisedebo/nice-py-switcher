#!/usr/bin/env python3
from pool.yiimp import Yiimp
import logger
import logging

print dir(logger)
logging.config = logger.logging
log.info("Testing Yiimp Pool")

z=Yiimp()
print(z.getAlgos())


