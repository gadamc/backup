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
  
  parser.add_argument('config', help='[required] The configuration file',default='config.ini')
  parser.add_argument('timeframe', help='[required] The timeframe is a word that describes how often this backup is run. For example, "weekly", "monthly", "daily" might be appropriate. The name of the backup database will be appened with this name. For example, if the source backup is "datadb", the backup for a timeframe="monthly" will be "datadb_monthly". It is up to the user to execute this script on a schedule that matches the timeframe value given on the command line.')

  args = parser.parse_args()

  postReplication(backup_config.appConfig(args.config), args.timeframe)