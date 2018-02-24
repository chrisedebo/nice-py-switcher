import json
import urllib.request
from pool import PoolBase, Algo

class Zpool(PoolBase):
    def __init__(self):
        self.apiUrl = "https://zpool.ca/api/status"
        self.poolUrl = "{ALGO}.mine.zpool.ca:{PORT}"
        self.profitData = "estimate_last24h"
        self.currency="BTC"
        super().__init__()
    
    AlgoMap = {    
		"Bitcore":"bitcore",
		"Blake2S":"blake2s",
		"Blakecoin":"blakecoin",
		"C11":"c11",
		"Equihash":"equihash",
		"Groestl":"groestl",
		"HSR":"hsr",
		"Keccak":"keccak",
		"LBRY":"lbry",
		"Lyra2RE2":"lyra2v2",
		"Myriad-Groestl":"myr-gr",
		"NeoScrypt":"neoscrypt",
		"NIST5":"nist5",
		"Phi":"phi",
		"Polytimos":"polytimos",
		"Quark":"quark",
		"Qubit":"qubit",
		"Sib":"sib",
		"Skein":"skein",
		"Skunk":"skunk",
		"Timetravel":"timetravel",
		"Tribus":"tribus",
		"X11":"x11",
		"X11evo":"x11evo",
		"X13":"x13",
		"X14":"x14",
		"X17":"x17",
		"XEvan":"xevan"
	}

    AlgoMapRev={}
    for n in AlgoMap:
        AlgoMapRev[AlgoMap[n]] = n

    def getAlgos(self):
        algos=[]

        statusData = json.loads(downloadString(self.apiUrl))

        for n in statusData:
            algoname = statusData[n]["name"]
            profitRatio = adjustEstimate(algoname,statusData[n][self.profitData])
            try:
                algoCommonName = Zpool.AlgoMapRev[algoname]
                algos.append(Algo(algoCommonName,self.currency,profitRatio))                
            except:
                #TODO LOG!!!!!!!
                pass
        
        return algos

    def getAlgoConnection(self, algo):
        AlgoMap['blah']
        return ""

#Get JSON from URL
def downloadString(url):
    req=urllib.request.Request(url, None, {"User-Agent": "Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1", \
                                            "Pragma": "no-cache"})
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

#Adjust estimates so they are all in mBTC/GHs/Day
def adjustEstimate(algoname,estimate):
    if algoname == "sha256":
        newestimate=float(estimate)/1000000000

    elif algoname == "equihash":
        newestimate=float(estimate)*1000

    elif algoname in ["scrypt", "blakecoin", "blake2s", "decred", "x11", "quark", "qubit", "keccak"]:
        newestimate=float(estimate)/1000

    else:
        newestimate=float(estimate)

    return newestimate
