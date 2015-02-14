#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" this is a configuration repo. this is th eplace where as much as possible of the configuration data is supposed
to be placed in order to NOT hardcode it into the code.
 """#


LISTEN_PORT_SNT = 7800 #


environ = {}
# Note: this dict has currently four levels of nesting.
# The top level contains immediate configuraiton informatin for launching the app,
#
# It also contains UC_schedules that contain info for timer driven looping calls.
# These Have three nesting levels to accommodate flexibility in UC design.
#
# This dict can also contain informatin on XML data sources.
# It can be extended t use an sqlite db later.

##################################################################
#
# SuperNET configuration

STONEFISH_IP = '178.62.185.131'   #
BOXFISH_IP   = '85.xx'   #

#SERVER_ADDR_jl777 = 'localhost'
SERVER_ADDR_jl777 =  STONEFISH_IP


SERVER_PORT_SUPERNETHTTP = 7778 # http  14632 twisted wants int

SCHEME = 'http://'
FULL_URL = SCHEME + SERVER_ADDR_jl777 + ":" + str(SERVER_PORT_SUPERNETHTTP)
POSTHEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}


##################################################################
#
# BitcoinDarkd configuration

SERVER_PORT_BTCD_RPC = 14632    # going thorugh BTCT RPC
BitcoinDarkRPCCreds = {'user' : 'azure', 'rpcPw' : 'Ir9qDmicntTxH8C'}
environ['BitcoinDarkRPCCreds'] = BitcoinDarkRPCCreds


###################################################################
#
#
#
# The top environ {dict} contains all configuration information.
# 
#  environ['whatIsNeeded'] = 'whatIsNeeded'
#
#


CACHE_DIR = '/localCache/' # use dedicated install subdir later

environ['CACHE_DIR'] = CACHE_DIR
environ['CACHE_FILENAMES'] = {
                                'soccer_schedule' : 'soccer_schedule.xml',\
                                'other_schedule' : 'other_schedule.xml',\
                                'more' : 'more.csv'
                                }

###################################################################


# The Use Cases need control schedulers that contain the calling frequency
# and the requestTypes to be called.
#
# For each frequency, multiple calls can be registered.
#
# Each UC scheduler has three levels of dict:
#
# UC_scheduler_xy {}  <------ is the master scheduler for the whole UseCase.
#  TIMER_Freq inits the UC class
#   
#     UC_schedule_1 - one Frequency {}
#          schedRequestTypes          {}
#
#
#     UC_schedule_2 - one Frequency {}
#          schedRequestTypes          {}
#
#     ....

# These triplets are cointained in the top environ dict



TIMER_850 = 0.850 # how often the the base timer is called for loopedCall
TIMER_5000 = 5.0
TIMER_15000 = 15.0  #  beware of millisec vs. secs !

TIMER1_SportsdataLLC_SECS = 5000.0

###################################################################
###################################################################
###################################################################
# UC schedulers
#
#
#

UCsched_1={}

#----------------------------------------

sched_GUIpoll ={}
sched_GUIpoll['schedName'] = 'GUIpoll'
sched_GUIpoll['callFreq'] = 1500               # ms!!

schedReqTypes={}

schedReqTypes['GUIpoll'] = {'requestType':'GUIpoll'}
sched_GUIpoll['schedReqTypes']  = schedReqTypes
sched_GUIpoll['target'] = 'this Uses requests!'

#----------------------------------------
sched_settings={}
sched_settings['schedName'] = 'uc_settings'
sched_settings['callFreq'] = 12500               # ms!!

schedReqTypes={}

schedReqTypes['uc_settings'] = {'requestType':'settings'}
schedReqTypes['ping'] = {'requestType':'ping'}

sched_settings['schedReqTypes']  = schedReqTypes
sched_settings['target'] = 'this Uses requests!'

#----------------------------------------
sched_getPeers ={}
sched_getPeers['schedName'] = 'uc_getpeers'
sched_getPeers['callFreq'] = 16500               # ms!!

schedReqTypes={}

schedReqTypes['uc_getpeers'] = {'requestType':'getpeers'}
sched_getPeers['schedReqTypes']  = schedReqTypes
sched_getPeers['target'] = 'this Uses requests!'



#+++++++++++++++++++++++++++++++++++++++++++++++++
# plug the schedules into the environment

UCsched_1[sched_GUIpoll['schedName']] = sched_GUIpoll
UCsched_1[sched_settings['schedName']] = sched_settings
UCsched_1[sched_getPeers['schedName']] = sched_getPeers


environ['UCsched_1'] = UCsched_1

                    # used by UCs:
                    #
                    # UC1_pingPong
                    # UC2_havenode
                    # UC4_sendMSG
                    # UC5_sendBIN
                    # UC6_checkMSG




##################################################################

UCsched_2 = {}


#----------------------------------------
sched_BTCDpoll ={}
sched_BTCDpoll['schedName'] = 'BTCDpoll'
sched_BTCDpoll['callFreq'] = 500             # ms!!

schedReqTypes={}

schedReqTypes['BTCDpoll'] = {'requestType':'BTCDpoll'}
sched_BTCDpoll['schedReqTypes']  = schedReqTypes
sched_BTCDpoll['target'] = 'this Uses requests!'

#----------------------------------------
sched_GUIpoll ={}
sched_GUIpoll['schedName'] = 'GUIpoll'
sched_GUIpoll['callFreq'] = 900              # ms!!

schedReqTypes={}

schedReqTypes['GUIpoll'] = {'requestType':'GUIpoll'}
sched_GUIpoll['schedReqTypes']  = schedReqTypes
sched_GUIpoll['target'] = 'this Uses requests!'

#----------------------------------------
sched_settings={}
sched_settings['schedName'] = 'uc_settings'
sched_settings['callFreq'] = 12500               # ms!!

schedReqTypes={}

schedReqTypes['uc_settings'] = {'requestType':'settings'}
schedReqTypes['ping'] = {'requestType':'ping'}

sched_settings['schedReqTypes']  = schedReqTypes
sched_settings['target'] = 'this Uses requests!'

#----------------------------------------
sched_getPeers ={}
sched_getPeers['schedName'] = 'uc_getpeers'
sched_getPeers['callFreq'] = 16500               # ms!!

schedReqTypes={}

schedReqTypes['uc_getpeers'] = {'requestType':'getpeers'}
sched_getPeers['schedReqTypes']  = schedReqTypes
sched_getPeers['target'] = 'this Uses requests!'


#+++++++++++++++++++++++++++++++++++++++++++++++++
# plug the schedules into the environment

UCsched_2[sched_BTCDpoll['schedName']] = sched_BTCDpoll
UCsched_2[sched_GUIpoll['schedName']] = sched_GUIpoll
UCsched_2[sched_settings['schedName']] = sched_settings
UCsched_2[sched_getPeers['schedName']] = sched_getPeers


environ['UCsched_2'] = UCsched_2






#############################################################


UC_sched_3={}


#----------------------------------------
sched_findvalue ={}
sched_findvalue['schedName'] = 'uc_findvalue'
sched_findvalue['callFreq'] = 14500               # ms!!

schedReqTypes={}
schedReqTypes['uc_findvalue'] = {'requestType':'findvalue'}
sched_findvalue['schedReqTypes']  = schedReqTypes
sched_findvalue['target'] = 'this Uses requests!'
### ++++++
#----------------------------------------
sched_store ={}
sched_store['schedName'] = 'sched_store'
sched_store['callFreq'] = 16500               # ms!!

schedReqTypes={}
schedReqTypes['sched_store'] = {'requestType':'store'}
sched_store['schedReqTypes']  = schedReqTypes
sched_store['target'] = 'this Uses requests!'
### ++++++

#----------------------------------------
sched_GUIpoll ={}
sched_GUIpoll['schedName'] = 'GUIpoll'
sched_GUIpoll['callFreq'] = 500               # ms!!

schedReqTypes={}
schedReqTypes['GUIpoll'] = {'requestType':'GUIpoll'}
sched_GUIpoll['schedReqTypes']  = schedReqTypes
sched_GUIpoll['target'] = 'this Uses requests!'

#----------------------------------------
sched_settings={}
sched_settings['schedName'] = 'uc_settings'
sched_settings['callFreq'] = 22500               # ms!!

schedReqTypes={}
schedReqTypes['uc_settings'] = {'requestType':'settings'}
schedReqTypes['ping'] = {'requestType':'ping'}

sched_settings['schedReqTypes']  = schedReqTypes
sched_settings['target'] = 'this Uses requests!'

#----------------------------------------
sched_getPeers ={}
sched_getPeers['schedName'] = 'uc_getpeers'
sched_getPeers['callFreq'] = 21500               # ms!!

schedReqTypes={}
schedReqTypes['uc_getpeers'] = {'requestType':'getpeers'}
sched_getPeers['schedReqTypes']  = schedReqTypes
sched_getPeers['target'] = 'this Uses requests!'

# plug the schedules into the environment

UC_sched_3[sched_GUIpoll['schedName']] = sched_GUIpoll
UC_sched_3[sched_findvalue['schedName']] = sched_findvalue
UC_sched_3[sched_store['schedName']] = sched_store

UC_sched_3[sched_settings['schedName']] = sched_settings
UC_sched_3[sched_getPeers['schedName']] = sched_getPeers



environ['UC3_store_findvalue'] = UC_sched_3


#
#                      used by UCs:
#
#                        UC3_store_findvalue
###################################################################











###################################################################

###################################################################

###################################################################








###################################################################
# sportdsdataLLC scheduler
#

schedSportsData={}
SERVER_ADDR_xmlFeed1 = "api.sportsdatallc.org"
SERVER_PORT_xmlFeed1 = 80



schedReqTypes={}

schedReqTypes['xml1'] = {'requestType':'get1'}
schedReqTypes['xml2'] = {'requestType':'get2'}


sched1={}
sched1['schedName'] = 'matchesSchedule'
sched1['callFreq'] = 6000000
sched1['reqType'] = 'xml'
sched1['target'] = 'http://api.sportsdatallc.org/soccer-t2/eu/schema/matches-schedule.xml?api_key=fv37s4rd2arqqxav774wb2kc'

sched1['schedReqTypes']  = schedReqTypes
schedSportsData[sched1['schedName']] = sched1


sched2={}
sched2['schedName'] = 'sched_matchSumm1'
sched2['callFreq'] = 1100000
sched2['reqType'] = 'xml'
sched2['target'] = 'http://api.sportsdatallc.org/soccer-t2/eu/matches/2014/08/22/summary.xml?api_key=fv37s4rd2arqqxav774wb2kc'

sched2['schedReqTypes']  = schedReqTypes
schedSportsData[sched2['schedName']] = sched2


sched3={}
sched3['schedName'] = 'sched_matchSumm2'
sched3['callFreq'] = 1700000
sched3['reqType'] = 'xml'
sched3['target'] = 'http://api.sportsdatallc.org/soccer-t2/eu/matches/2014/08/21/summary.xml?api_key=fv37s4rd2arqqxav774wb2kc'

sched3['schedReqTypes']  = schedReqTypes
schedSportsData[sched3['schedName']] = sched3


environ['envSportsData'] = schedSportsData





################################################################



#
#
#
#

