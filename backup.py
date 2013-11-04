#backup.py
import backup_config
import argparse
import requests
import json

'''
This script fires off a one-off replication for each database in the configuration
'''

def getReplicationDoc(source, target):
  return {
    "source":source,
    "target":target,
    "create_target":True
  }


def postReplication(aConfig, timeframe):

  sourcedbs = aConfig.dbbackuplist.split(' ')


  for adb in sourcedbs:
    source_url = 'https://{0}:{1}@{2}/{3}'.format(
      aConfig.fromusername, 
      aConfig.frompassword, 
      aConfig.fromserver,
      adb
    )

    target_url = 'https://{0}:{1}@{2}/{3}_{4}'.format(
      aConfig.tousername, 
      aConfig.topassword, 
      aConfig.toserver,
      adb, 
      timeframe 
    )

    repdoc = getReplicationDoc(source_url, target_url)

    print 'setting up replication'
    print json.dumps(repdoc, indent=1)

    auth = (aConfig.fromusername, aConfig.frompassword)
    headers = {'Content-type': 'application/json'}

    post_url = 'https://{0}/_replicator'.format(aConfig.fromserver)

    r = requests.post(
      post_url,
      auth=auth,
      headers = headers,
      data=json.dumps(repdoc)
    )


if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  
  parser.add_argument('config', help='[required] new status',default='config.ini')
  parser.add_argument('timeframe', help='[required] new status')

  args = parser.parse_args()

  postReplication(backup_config.appConfig(args.config), args.timeframe)