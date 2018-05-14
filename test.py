#!/usr/bin/env python3
from pool.loader import poolFactory

import logger
import logging
import time
from time import sleep

class test:
    def run(self):
        # chris found a program called figlet that makes BIG text and got a LITTLE excited.
        log = logging.getLogger("pool.test-runner")
        log.warn("==================================================")
        sleep(0.001)
        log.warn("||    ___           _        ______        __   ||")
        sleep(0.001)
        log.warn("||   / _ )___ ___ _(_)__    /_  __/__ ___ / /_  ||")
        sleep(0.001)
        log.warn("||  / _  / -_) _ `/ / _ \    / / / -_|_-</ __/  ||")
        sleep(0.001)
        log.warn("|| /____/\__/\_, /_/_//_/   /_/  \__/___/\__/   ||")
        sleep(0.001)
        log.warn("||          /___/                               ||")
        sleep(0.001)
        log.warn("==================================================")
        sleep(0.001)

        log.info("Loading Pools config")
        try:
            fac = poolFactory("./config/pools.yaml")
        except:
            log.error("Error loading pool config")
            raise
        
        pools = fac.getPools()
        for pool in pools:
            poolAlgos = pool.getAlgos()
            sleep(0.001)
            log.info("Pool '%s' containing %s available algo(s)", pool.PoolName(), len(poolAlgos))

        #Sleep for 1ms so our end banner is displayed correctly in logtrail.
        sleep(0.001)
        log.warn("=================================================")
        sleep(0.001)
        log.warn("||        ____        __  ______        __     ||")
        sleep(0.001)
        log.warn("||       / __/__  ___/ / /_  __/__ ___ / /_    ||")
        sleep(0.001)
        log.warn("||      / _// _ \/ _  /   / / / -_|_-</ __/    ||")
        sleep(0.001)
        log.warn("||     /___/_//_/\_,_/   /_/  \__/___/\__/     ||")
        sleep(0.001)
        log.warn("||                                             ||")
        sleep(0.001)
        log.warn("=================================================")

t = test()
t.run()
