#!/usr/bin/python

import time
import socket
from nsone import NSONE
from datadog import initialize, api

def dd_send(zone, metric):
        options = {
                'api_key':'DD_API_KEY_GOES_HERE',
                'url':'https://app.datadoghq.com/api/v1/series?api_key=DD_API_KEY_GOES_HERE'
        }
        initialize(**options)
        now = time.time()
        api.Metric.send(metric='dns.qps', points=(now, metric), tags=["zone:" + zone], host=None, type='gauge')

def get_zones(nsone):
        zones = nsone.zones()
        zoneslist = zones.list()
        zonenames=[]
        for i in range(0, len(zoneslist)):
            zonenames.append(zoneslist[i].get('zone'))
        return zonenames

def get_qps(nsone, domain):
        zone = nsone.loadZone(domain)
        qps = zone.qps()
        return qps['qps']

def main():
        nsone = NSONE(apiKey='NSONE_API_KEY_GOES_HERE')
        zonenames = get_zones(nsone)
        for i in range(0, len(zonenames)):
            qps = get_qps(nsone, zonenames[i])
            #print(zonenames[i] + ': ' + str(qps))
            dd_send(zonenames[i], qps)

if __name__ == '__main__':
        main()
