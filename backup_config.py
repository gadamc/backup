import ConfigParser


#a little class to hold the configuration and make it easier to pass around the info
#Note - backups are ALWAYS mediated by the fromserver

class appConfig:

  def __init__ (self, configfile):
    self.readconfig(configfile)

  def readconfig(self, configfile):
    #read credentials configuration
    config = ConfigParser.RawConfigParser()
    config.read(configfile)

    self.fromserver = config.get('backup', 'fromserver')
    self.fromusername = config.get('backup', 'fromusername')
    self.frompassword = config.get('backup', 'frompassword')
    self.toserver = config.get('backup', 'toserver')
    self.tousername = config.get('backup', 'tousername')
    self.topassword = config.get('backup', 'topassword')
    self.dbbackuplist = config.get('backup', 'dbbackuplist')

    self.headers = {'content-type': 'application/json'}
    self.auth = (self.fromusername, self.frompassword)

