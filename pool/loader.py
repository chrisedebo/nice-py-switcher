import yaml
import logging
from pool.yiimp import Yiimp

class poolFactory:
    
    def __init__(self, yamlFile):
        self.log = logging.getLogger(__name__)
        self.log.debug("factory loading config '%s'", yamlFile)
        with open(yamlFile) as fd:
            yamlconfig = yaml.load(fd)
            self.config = yamlconfig["pools"]

    def getPools(self):
        poolDefs = self.config["poolDefs"]
        self.log.debug("getting pools from config, have %s pool Def(s)", len(poolDefs))
        pools= []
        for poolDef in poolDefs:               
            poolType = poolDef["class"]
            poolName = poolDef["name"]
            self.log.debug("found pool definintion %s for pool %s",poolType, poolName)
            if poolType == "pool.yiimp":                 
                pools.append(Yiimp(poolDef))
                self.log.debug("added Yiimp pool %s", poolName)
        return pools



    def get_class( kls ):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m


