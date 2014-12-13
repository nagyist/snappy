#!/usr/bin/python3
# -*- coding: utf-8 -*-


from twisted.internet import protocol #, # ClientFactory
from twisted.internet.protocol  import ClientFactory

from twisted.python import log
from twisted.web.client import getPage
from datetime import datetime
import json
import requests
from twisted.internet.threads import deferToThread
import time
from snAppyModules.snAppyConfig import *
#from requests import Request, Session
#from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory, ServerFactory




class Schedule(object):
    """ container class to contain schedule info for each cached data feed
        This gets the simpl dicts from the snApiConfig module"""#
    def __init__(self, schedule, ):

        self.schedule = schedule
        self.callFreq = schedule['callFreq']
        self.SNrequests = schedule['SNreqTypes']

        self.name = schedule['schedName']  # sched_GUIpoll['schedName']

        # these need to addressed explicitly by their names in the UC class,
        # and there the names must be known explicitly anyway
        self.target = schedule['target']
        self.lastCallTime = int(time.time() * 1000)



    def callMe(self):
        self.deltaT = int(time.time() * 1000 ) - self.lastCallTime
        #log.msg("callFreq schedule ", self.name," ???: ", self.deltaT ," > ", self.callFreq, self.deltaT > self.callFreq)
        if self.deltaT > self.callFreq:
            self.lastCallTime = int(time.time() * 1000 )
            return True
        else:
            return False







class UC_templateEXAMPLE(object):

    """

each UC can have MULTIPLE schedule timers!
each schedule timer can init different conditional request sequences of deferreds!
each t
        This handles scheduled tasks such as pulling XML data to update the local cache.


        We enter the Scheduled DATA by way of a structure form instantiation to be more flexible.

        A single schedule needs a name, a callFreq and a target. Then multiple schedules can be wrapped into an outer schedules dict.
        from this they are unwrapped here and the Scheduler instance can serve multiple schedules.

        So Schedulers have a callFreq, and Schedules have their own callFreq.

    Note: schedulers can use different methods to do their deferred work:
    1: use a client proxy to get stuff from the internet,
    2: use a simple deferredToThread to do local things like caching or SuperNET communication
    3: SuperNET controller apps have their business logic in classes of this type.

    Schedulers that use deferToThread do NOT need a Protocol!
    But a protocol CAN be used to organize internal logic.


    DESIGN:

    This allows to run MULTIPLPE timer schedules in ONE useCase!

    It may be better to build tailor made classes for specific tests and UCs
    instead of using one class and feed different schedules to it.

    These can either instantiate their own custom client protocols,
    or they can use the standard protocols that are provided in the main serveFactory.

    Or they don't use protocols at all.

    Many UCs will use cascading calls where the reply sequence is UC specific.
    Hence, it is better to make a Scheduler class for each UC,
    and use cascading deferreds to implement the use case logic.

    Thes UCs can be made with or without PROTOCOL/FACTORY.
    A Protocol provides a transport layer AND a deferred.
    When using python.requests, we do the transport and the deferred ourselves here.
    Both seems possible. Don't know if one is always better, so let's try both.

    """#
    def __init__(self, serverFactory , environ = {} ): # prepSchedules = {},

        self.environ = environ
        self.schedules = {}    # this contains the schedules


        #
        # This is just a template. If needed, all kind of things can be hardcoded into the UC class!
        # This provides facilities to take the schedules (PLURAL!) from the config,
        # and reqTypes if it is better to have those in the config.
        # can introduce the schedules explicitly here!!
        # because the UC classes do contain explicit and hard coded UC logic,
        # they can also unpack their schedules here explicitly!

        prepSchedules = environ['template'] # create a schedule in snAppyConfig.py !!!
        for sched in prepSchedules.keys():
            sched = prepSchedules[sched]
            self.schedules[ sched['schedName']   ] = Schedule( sched )

        self.lastCallTime = int(time.time() * 1000)
        # These obejcts may be used:
        # self.clientFactory = protocol.ClientFactory
        # self.qComp_777 = serverFactory.qComp_777
        # self.parser_777 = serverFactory.parser_777
        # self.parser_FOR_PRICEDATA = serverFactory.parser_FOR_PRICEDATA !!!!!!!!!!!!!!!!!!!!

        # we only keep the timers in the config file?!?!

    def periodic(self, ):
        """ this is the method that is called periodically by the twisted loopingTask.
         This contains the UseCase logic, ie needs to check what to do, and then do it. """#

        schedulesDue =[]
        print( "Scheduler ", self, " MAIN scheduled Heartbeat: ", datetime.now())

        for schedule in self.schedules.keys():
            schedule = self.schedules[schedule]

            if schedule.callMe():
                schedulesDue.append(schedule)



    def runSchedules(self,schedulesDue):

        for schedDue in schedulesDue:
            if 'uc1Start_settings' in schedDue.SNrequests.keys():
                reqData = schedDue.SNrequests['uc1Start_settings']
                self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqData), headers=POSTHEADERS)
                self.deferred.addCallback(self.rpl777_df1)
                self.deferred.addErrback(self.rpl777ERR)
            elif 'SPAM' == 'EGGS':
                pass
    #
    #
    # cascading deferreds here!
    #
    def rpl777_df1(self, dataFrom777):
        """ These deferreds are UseCase specific!  """#
        repl=dataFrom777.json()
        next_req_we_want_to_do_in_df1 =    {'requestType':'ping'}

        for thing in repl['whitelist']:
            next_req_we_want_to_do_in_df1['destip'] = thing
            self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(next_req_we_want_to_do_in_df1), headers=POSTHEADERS)
            self.deferred.addCallback(self.rpl777_df2)
            self.deferred.addErrback(self.rpl777ERR)

    def rpl777_df2(self, dataFrom777):

        # we do not have any requester to give anything back to.
        # either another part of the use case or just dump to screen or file.
        print( 1 * "\n---->rpl777 deferred here", dataFrom777)
        repl = dataFrom777.content.decode("utf-8")
        repl=eval(repl)
        for se in repl:
            print(se,repl[se])
        # etc
        #
        # from here we can continue with findnode etc
        #
        #

        ####################################################################
        # Important NOTE:
        # IT IS ALSO POSSIBLE TO MAKE CALLBACKS THAT CALL THEMSELVES!
        # this quickly degrades, BUT_ it can be done with an exit condition!
        #####################################################################


    def rpl777ERR(self, ERR777):
        raise RuntimeError

















##########################################################





class UCTEST_1_ping_whitelist_777(object):


    """



settings - ping whitelist

this also documents the api call params and return values



    """#


    def __init__(self, serverFactory , environ = {} ): # prepSchedules = {},



        self.environ = environ
        self.schedules = {}    # this contains the schedules

        prepSchedules = environ['UCTEST_1_ping_whitelist_777'] # create a schedule in snAppyConfig.py !!!
        for sched in prepSchedules.keys():
            sched = prepSchedules[sched]
            self.schedules[ sched['schedName']] = Schedule( sched )

        self.lastCallTime = int(time.time() * 1000)


    def periodic(self, ):
        """ this is the method that is called periodically by the twisted loopingTask.
         This contains the UseCase logic, ie needs to check what to do, and then do it. """#

        schedulesDue =[]
        #print( "Scheduler ", self, " MAIN scheduled Heartbeat: ", datetime.now())

        for schedule in self.schedules.keys():
            schedule = self.schedules[schedule]

            if schedule.callMe():
                schedulesDue.append(schedule)

        self.runSchedules(schedulesDue)


    def runSchedules(self,schedulesDue):


#
# RUN GUIPOLL HERE ON A FASTER SCHEDULE THAN THE PAYLOAD CALLS!
#
#

        for schedDue in schedulesDue:
            if 'uc1Start_settings' in schedDue.SNrequests.keys():
                reqData = schedDue.SNrequests['uc1Start_settings']
                self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqData), headers=POSTHEADERS)
                self.deferred.addCallback(self.rpl777_df1)
                self.deferred.addErrback(self.rpl777ERR)
            elif 'SPAM' == 'EGGS':
                pass
    #
    # cascading deferreds here!
    #
    def rpl777_df1(self, dataFrom777):
        """"""#
        repl=dataFrom777.json()
        reqPing = {'requestType':'ping'}

        ipsToPing=repl['whitelist'] #[0] # singlecheck
        #ipsToPing = 10* ['178.62.185.131'] # stonefish['80.41.56.181'] # ['85.178.202.108']   #

        for node in ipsToPing:
            reqPing['destip']=node
            self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqPing), headers=POSTHEADERS)
            self.deferred.addCallback(self.rpl777_df2)
            self.deferred.addErrback(self.rpl777ERR)


    def rpl777_df2(self, dataFrom777):
        """"""#
        repl=dataFrom777.json()
        #log.msg( 1 * "\n---->rpl777 ping", dataFrom777)
        repl=dataFrom777.content.decode("utf-8")
        repl=eval(repl)
        # for se in repl:
        #     print(se,repl[se]) #85.178.200.167

        reqGUIpoll = {'requestType':'GUIpoll'}

        self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqGUIpoll), headers=POSTHEADERS)
        self.deferred.addCallback(self.rpl777_df3)
        self.deferred.addErrback(self.rpl777ERR)



    def rpl777_df3(self, dataFrom777):
        """
        Note : Use python assert in the future
                Use parse and format for the strings!

        """#

        if dataFrom777.content == b'{"result":"nothing pending"}':
            return {"result":"nothing pending"}

        #log.msg( 1 * "\n---->rpl777 GUIpoll", dataFrom777, type(dataFrom777))
        #log.msg( 1 * "\n---->rpl777 GUIpoll", dataFrom777.content)

        try:

            repl=dataFrom777.content.decode("utf-8")
            #repl=eval(repl)
            repl = json.loads(repl)

            # 1 decode bytes to utf8
            # 2 eval to dict
            # 3 separate dict into result, request, aux
            # 4 repeat on request for [ result, token ]
            # 5 repeat on result

            # repl=dataFrom777.json() #.decode("utf-8")
            # print("GUIpoll-->\n",repl)
            # BEFORE EVAL: {"result":"{\"result\":\"kademlia_pong\",\"NXT\":\"3571143576961987768\",\"ipaddr\":\"89.212.19.49\",\"port\":0\",\"lag\":251.188,\"numpings\":13,\"numpongs\":11,\"ave\":1062.435\"}","from":"89.212.19.49","port":0,"args":"[{\"requestType\":\"pong\",\"NXT\":\"3571143576961987768\",\"time\":1417702487,\"yourip\":\"85.178.200.167\",\"yourport\":61234,\"ipaddr\":\"89.212.19.49\",\"pubkey\":\"30d02aec153a5b7c4e606c2f50b7ac9e71ca814328189cac288650af3d114c30\",\"ver\":\"0.199\"},{\"token\":\"2nm2lk1gc177ompqlirl0brc8e0skscu52m9o61824uquk46tq11ec2cjag7fso1hs074kct6vk905lfbvv512adh3rk6hfau383o9vfilrgd3d1telilup7sdnfuce7h0c8nsd2k1kq4ec361d4d3hmf5ae8egr\"}]"}
            # print("GUIpoll-->\n",repl)
            # after eval
            # {'args': '[{"requestType":"pong","NXT":"3571143576961987768","time":1417702487,"yourip":"85.178.200.167","yourport":61234,"ipaddr":"89.212.19.49","pubkey":"30d02aec153a5b7c4e606c2f50b7ac9e71ca814328189cac288650af3d114c30","ver":"0.199"},{"token":"2nm2lk1gc177ompqlirl0brc8e0skscu52m9o61824uquk46tq11ec2cjag7fso1hs074kct6vk905lfbvv512adh3rk6hfau383o9vfilrgd3d1telilup7sdnfuce7h0c8nsd2k1kq4ec361d4d3hmf5ae8egr"}]', 'port': 0, 'result': '{"result":"kademlia_pong","NXT":"3571143576961987768","ipaddr":"89.212.19.49","port":0","lag":251.188,"numpings":13,"numpongs":11,"ave":1062.435"}', 'from': '89.212.19.49'}

            try:
                resultFull = repl['result']

            except:
                resultFull = {'result': 'no_Result_contained'}
                log.msg(resultFull)
                return {'result': 'no_Result_contained'}
            try:
                origRequest = repl['args']
            except:
                origRequest= ({"requestType":'0'}, {"token": '0'})
            try:
                fromPort = repl['port']
            except:
                fromPort = 0
            try:
                fromIp = repl['from']
            except:
                fromIp = '0'

            #print("args", args )
            #print("args type", type(args))

            try:
                origRequest=origRequest.lstrip('[')
                origRequest=origRequest.rstrip(']')
                fullRequest = origRequest.split('},{')[0] + '}'
                token =   '{'+ origRequest.split('},{')[1]
                # log.msg(fullRequest,type(fullRequest))#
                # log.msg(token,type(token))#
                token = json.loads(token)
                fullRequest = json.loads(fullRequest)


                print(fullRequest, type(fullRequest))

                # this eval produces a TUPLE?!?!      yes: '[ {origRequest:origRequest} , {token:token} ]' !!!!!
            except:
                #log.msg("problem with extracting args")#
                origRequest={'no':'args'}
                token = {'token':'NONE'}



# MAKE A GUIPOLL PARSER HERE
#
            #
            # after a really long time I giot a havendoe!
            #
            #
            #
            #

 #{"result":"kademlia_havenode from NXT.5624143003089008155 key.(5624143003089008155) value.([["5624143003089008155", "192.99.212.250", "7777", "0"], ["15178638394924629506", "167.114.2.206", "7777", "1417435953"], ["6249611027680999354", "80.41.56.181", "7777", "1417449705"], ["11910135804814382998", "167.114.2.94", "7777", "1417435991"], ["7581814105672729429", "187.153.194.200", "29693", "1417652256"], ["7108754351996134253", "167.114.2.171", "7777", "1417435991"], ["16196432036059823401", "167.114.2.203", "7777", "1417435957"]])"}

# {"result":"kademlia_havenode from NXT.5624143003089008155 key.(5624143003089008155) value.([["5624143003089008155", "192.99.212.250", "7777", "0"], ["15178638394924629506", "167.114.2.206", "7777", "1417435953"], ["6249611027680999354", "80.41.56.181", "7777", "1417449705"], ["11910135804814382998", "167.114.2.94", "7777", "1417435991"], ["7581814105672729429", "187.153.194.200", "29693", "1417652256"], ["16196432036059823401", "167.114.2.203", "7777", "1417435957"], ["7108754351996134253", "167.114.2.171", "7777", "1417435991"]])"}
            try:
                #log.msg("\n",fullRequest,"\n",)
                pubkey= fullRequest['pubkey'] # check that this is really pubkey and not DHT key
                requestType= fullRequest['requestType']
                ver =fullRequest['ver']
                yourip =fullRequest['yourip']
                yourport =fullRequest['yourport']

                NXT =fullRequest['NXT']
                time =fullRequest['time']
                ipaddr =fullRequest['ipaddr']


            except Exception as e:
                print("Error parsing fullRequest:  {0}".format(str(e)))
                #log.msg("problem with extracting fullRequest")#,fullRequest, type(fullRequest))
                fullRequest =  { "requestType" : "0" }

# result :
# {"result":"kademlia_havenode from NXT.8894667849638377372 key.(10694781281555936856) value.([["10694781281555936856", "209.126.70.170", "7777", "1417935711"], ["11910135804814382998", "167.114.2.94", "7777", "1417934979"], ["8894667849638377372", "209.126.70.156", "7777", "0"], ["6216883599460291148", "192.99.246.126", "7777", "1417935166"], ["15178638394924629506", "167.114.2.206", "7777", "1417934954"], ["13594896385051583735", "192.99.246.20", "7777", "1417934951"], ["2131686659786462901", "178.62.185.131", "7777", "1417943077"]])"}


            try:
                #resultFull = eval(resultFull) #<------------- YES this is a str too!
                resultFull = json.loads(resultFull) #<------------- YES this is a str too!

                port =  resultFull['port']
                numpings =  resultFull['numpings']
                lag  =  resultFull['lag']
                ipaddr  = resultFull['ipaddr']
                numpongs =  resultFull['numpongs']
                result =   resultFull['result']
                ave  =  resultFull['ave']
                NXT  = resultFull['NXT']
                #log.msg("resultFull", resultFull,type(resultFull))


            except:
                log.msg("resultFull oops- wrong GUIpoll!:", resultFull,type(resultFull) )
                resultFull={'wrong':'poll'}
                #log.msg(resultFull,type(resultFull) )



            ptt_PONG = {
                            'fullRequest': fullRequest , \
                            "token":token  ,\
                            'result':resultFull,\
                            'fromPort':fromPort,\
                            'fromIp' : fromIp
                            }

            print(3*"---------------*") #\n")
            for key in ptt_PONG.keys():


                if key == 'result':
                    for keyR in ptt_PONG[key].keys():
                        print( keyR, " - ",ptt_PONG[key][keyR])
                    continue
                print(1*"\n")
                if key == 'fullRequest':
                    for keyR in ptt_PONG[key].keys():
                        print( keyR, " - ",ptt_PONG[key][keyR])
                    continue

                print("\n", key, " - ",ptt_PONG[key], "\n")



        except Exception as e:
            print("Error {0}".format(str(e)))



    def rpl777ERR(self, ERR777):

        print(ERR777)

        raise RuntimeError





class Parser(object):


    ptt_PONGstringStage1 = {
                    'args': '[ {"requestType":"pong", "NXT":"","time":,"yourip":"","yourport":,"ipaddr":"","pubkey":"","ver":"0.199"} , {"token":"" }]' ,\
                    'result': '{"result":"kademlia_pong","NXT":"","ipaddr":"","port":0","lag":0,"numpings":0,"numpongs":0,"ave":0}',\
                    'port':0,\
                    'from' : ''
                    }

    ptt_PONG = {
                    'fullRequest': {"requestType":"pong", "NXT":"","time":"","yourip":"","yourport":"","ipaddr":"","pubkey":"","ver":"0.199"} , \
                    "token":""  ,\
                    'result': {"result":"kademlia_pong","NXT":"","ipaddr":"","port":0 ,"lag":0,"numpings":0,"numpongs":0,"ave":0},\
                    'fromPort':0,\
                    'from' : ''
                    }



#  {'from': '192.99.246.126', 'port': 0, 'args': '[{"requestType":"havenode","NXT":"6216883599460291148","time":1418307717,"key":"5624143003089008155","data":[["5624143003089008155", "192.99.212.250", "7777", "1418256837"], ["15178638394924629506", "167.114.2.206", "7777", "1418256815"], ["11910135804814382998", "167.114.2.94", "7777", "1418256815"], ["6216883599460291148", "192.99.246.126", "7777", "0"], ["7108754351996134253", "167.114.2.171", "7777", "1418256939"], ["16196432036059823401", "167.114.2.203", "7777", "1418256827"], ["7581814105672729429", "187.153.143.36", "27190", "1418266908"]]},{"token":"7meqnnpffqh9272utch79ra8rvlih9mevl901qhml0phabmmuuv4a7blsqnoqh01pc3d6rgrmrrul935mv5fhk877p6mu0h8cfplsqs8e2p0njtuhj5oct8js9qlob3q3c7vggui0rej3bdsprtrtuajhvt8pjhs"}]', 'result': '{"result":"kademlia_havenode from NXT.6216883599460291148 key.(5624143003089008155) value.([["5624143003089008155", "192.99.212.250", "7777", "1418256837"], ["15178638394924629506", "167.114.2.206", "7777", "1418256815"], ["11910135804814382998", "167.114.2.94", "7777", "1418256815"], ["6216883599460291148", "192.99.246.126", "7777", "0"], ["7108754351996134253", "167.114.2.171", "7777", "1418256939"], ["16196432036059823401", "167.114.2.203", "7777", "1418256827"], ["7581814105672729429", "187.153.143.36", "27190", "1418266908"]])"}'} <class 'dict'>


    def __init__(self):
        pass





class UCTEST_2_ping_findnode(object):

    """



settings - ping whitelist and do findnode

this also documents the api call params and return values

differentiate two types of replies:

1- the replies that are given back by the SuperNET server regularly
2- the replies that are taken from the internal GUIpoll


    """#


    def __init__(self, serverFactory , environ = {} ): # prepSchedules = {},



        self.environ = environ
        self.schedules = {}    # this contains the schedules

        self.nodeDi = {}
        self.peers = {}

        prepSchedules = environ['UCTEST_1_ping_whitelist_777'] # can use same as UC1 for now- extends it
        for sched in prepSchedules.keys():
            sched = prepSchedules[sched]
            self.schedules[ sched['schedName']] = Schedule( sched )

        self.lastCallTime = int(time.time() * 1000)


    def periodic(self, ):
        """ This is the method that is called periodically by the twisted loopingTask.
         It iterates over all schedules in the UseCase class, checks if they are due to be called,
         adds the ones due to a list and passes that list on to runSchedules(). """#

        schedulesDue =[]



        for schedule in self.schedules.keys():
            schedule = self.schedules[schedule]

            if schedule.callMe():
                schedulesDue.append(schedule)

        self.runSchedules(schedulesDue)


    def runSchedules(self,schedulesDue):
        """ here we get through all the due schedules and call them on SuperNET server
             Here we explicitly check the name and send them to the first callback of their callback sequence."""#


        for schedDue in schedulesDue:
            if 'uc1Start_settings' in schedDue.SNrequests.keys():
                log.msg("nodeDi: IPs ", self.nodeDi.keys())
                log.msg("nodeDi: NXTs", self.nodeDi.values())

                reqData1 = schedDue.SNrequests['uc1Start_settings']
                self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqData1), headers=POSTHEADERS)
                self.deferred.addCallback(self.rpl777_settings_df1)
                self.deferred.addErrback(self.rpl777ERR)

                reqData2 = {"requestType":"getpeers"}
                self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqData2), headers=POSTHEADERS)
                self.deferred.addCallback(self.rpl777_getpeers_df1) #rpl777_pingDB_df1
                self.deferred.addErrback(self.rpl777ERR)

                #self.rpl777_pingDB_df1() # ping all peers collected here!


            elif 'GUIpoll' in schedDue.SNrequests.keys():
                log.msg("do GUIpoll")
                reqData = schedDue.SNrequests['GUIpoll'] # this has 0.9 sec
                self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqData), headers=POSTHEADERS)
                self.deferred.addCallback(self.rpl777_df0_GUIpoll)
                self.deferred.addErrback(self.rpl777ERR)




    def rpl777_df0_GUIpoll(self, dataFrom777):
        """
         Distribute to their processing points!

         list what we can catch here from the GUIpoll

        This is the jump point to direct the returns from GUIpoll to their specific parsing functions.
        The formats sometimes change, and the parsing is better done individually!
        This has been a source of confusion!

-------------------

kademlia_store


GUIpoll ---> kademlia_store {'result': '{"result":"kademlia_store","key":"5420018378925390393","data":"489b81f54869a9bd7986d5e938fecc5677fdd3f8d389ce2f5616f1927f602a725038a2457abd5ff58aa3b3245bbaf3342b6cf9dd08ea93a721727aac165a77c0b79c0b28080440350af365aa","len":76,"txid":"3283676187569738843"}', 'port': 0, 'from': '184.175.25.117', 'args': '[{"requestType":"store","NXT":"17265504311777286118","time":1418334721,"key":"5420018378925390393","data":76},{"token":"4sjc45u1mu6lfbkt4crqchc8440s7coei94dt438hvsn919qv0js487fatka3981br5ro6n0gcq4nq8b9c4q2ioj8d33sggln4uo7kafj61gf7nr5rp5q8q5o49becep1sjr6atj9ih4vhto8jfrn68vd24g6iol"}]'} <class 'dict'>


-----------------------

kademlia_havenode


GUIpoll ---> kademlia_havenode {'result': '{"result":"kademlia_havenode from NXT.16196432036059823401 key.(16196432036059823401) value.([["16196432036059823401", "167.114.2.203", "7777", "0"], ["15178638394924629506", "167.114.2.206", "7777", "1418308962"], ["7108754351996134253", "167.114.2.171", "7777", "1418308926"], ["12315166155634751985", "167.114.2.205", "7777", "1418308932"], ["11634703838614499263", "69.90.132.106", "7777", "1418309115"], ["11910135804814382998", "167.114.2.94", "7777", "1418308909"], ["5624143003089008155", "192.99.212.250", "7777", "1418308915"]])"}', 'from': '167.114.2.203', 'port': 0, 'args': '[{"requestType":"havenode","NXT":"16196432036059823401","time":1418318194,"key":"16196432036059823401","data":[["16196432036059823401", "167.114.2.203", "7777", "0"], ["15178638394924629506", "167.114.2.206", "7777", "1418308962"], ["7108754351996134253", "167.114.2.171", "7777", "1418308926"], ["12315166155634751985", "167.114.2.205", "7777", "1418308932"], ["11634703838614499263", "69.90.132.106", "7777", "1418309115"], ["11910135804814382998", "167.114.2.94", "7777", "1418308909"], ["5624143003089008155", "192.99.212.250", "7777", "1418308915"]]},{"token":"ratb2fdulus9a3mr7nqvbseibjgnr0vnadt9vs0k8svpki0suvjj6go5j619p2816f3621bm9ncmp0auu5ojtoive3rp9tg5ecd8cv05pn10098dumvlvotqskq62339il35eo1tq8e304lioj4u80f88lc0ve5g"}]'} <class 'dict'>



----------------------

If findnode is in the GUIpoll internally, that means that the findnode came form another node!

GUIpoll ---> findnode {'result': '{"result":"kademlia_findnode from.(7108754351996134253) previp.(167.114.2.171) key.(2131686659786462901) datalen.0 txid.4621598500260051131"}', 'from': '167.114.2.171', 'port': 0, 'args': '[{"requestType":"findnode","NXT":"7108754351996134253","time":1418318210,"key":"2131686659786462901"},{"token":"j8edkcsu69k3e3e0ru9p4f6fepega7dijt24dh71h9kfqsg6uvjk4vp3jm6i0m0101ag1me1dubc7cere1tmhahvcc11scjkbmv37ql6gm40vr3gem13gt7jt33l71ro32eu3c37kd90e51cddlb9tnb9eacmgu9"}]'} <class 'dict'>


parsing the GUIpoll is a two step process:

1  extract the standard contents and its standard sub contents
1
2
3
4
5

2 extract the specifics form the sub contents
details




         """#

        # test on string and send there!
        # maybe this can be done more elegant later, but probably not.

        #log.msg("GUIpoll entry--->  ",dataFrom777, type(dataFrom777),"\n")

        rpl777=dataFrom777.json()
        #log.msg("GUIpoll entry--->  ",rpl777, type(rpl777),"\n")

        if 'nothing pending' in str(rpl777):
            pass#log.msg("GUIpoll --->  ",rpl777, type(rpl777),"\n")

        elif 'kademlia_store' in str(rpl777):
            self.rpl777_GUIpoll_kademlia_store(rpl777)
            #log.msg("GUIpoll ---> kademlia_store",rpl777, type(rpl777),"\n")

        elif 'kademlia_pong' in str(rpl777):
            #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            self.rpl777_GUIpoll_kademlia_pong(rpl777)

        elif 'kademlia_havenode' in str(rpl777):
            #log.msg("GUIpoll ---> kademlia_havenode",rpl777, type(rpl777),"\n")
            self.rpl777_GUIpoll_kademlia_havenode(rpl777)

        elif 'kademlia_findnode' in str(rpl777):
            #log.msg("GUIpoll ---> findnode",rpl777, type(rpl777),"\n")
            self.rpl777_GUIpoll_findnode(rpl777)


        else:
            log.msg(20*"GUIpoll ---> CALL not caught yet: ",rpl777, type(rpl777),"\n")

        return 0







    def rpl777_GUIpoll_kademlia_store(self, rpl777): #dataFrom777):
        pass #print(5*"\n+++++rpl777_GUIpoll_kademlia_store ")






    def rpl777_GUIpoll_findnode(self, rpl777): #dataFrom777):
        """
        GUIpoll --->   {'result': '{"result":"kademlia_findnode from.(7067340061344084047) previp.(94.102.50.70) key.(2131686659786462901) datalen.0 txid.12611969529750120048"}', 'port': 0, 'from': '94.102.50.70', 'args': '[{"requestType":"findnode","NXT":"7067340061344084047","time":1418391191,"key":"2131686659786462901"},{"token":"197njl2bp54ijkjnfadmvua4irii342267l8taa4n53vqhg5v425eg3455h836g1in2v8sunh9j9mf4hnr7fmhsbdhsb8qk1kp18m6a77gq0d6s57151c1mejh29j3fcpg3jsvidjkbva8g896hjbss5ub7482ms"}]'} <class 'dict'>
        GUIpoll --->   {'from': '167.114.2.171', 'result': '{"result":"kademlia_findnode from.(7108754351996134253) previp.(167.114.2.171) key.(2131686659786462901) datalen.0 txid.14645060032929148909"}', 'port': 0, 'args': '[{"requestType":"findnode","NXT":"7108754351996134253","time":1418320475,"key":"2131686659786462901"},{"token":"j8edkcsu69k3e3e0ru9p4f6fepega7dijt24dh71h9kfqsg6uvo1ovp37gquc4g1ssnvc81804v9pipdo8al5iihmpmls4n9ici5hbe5m0rgveg8fek61lpihnn5k9cne28m9p8b71o918vkeelei1lpaljpn8n4"}]'} <class 'dict'>
        """#
        #log.msg("GUIpoll ---> rpl777_GUIpoll_findnode",rpl777, type(rpl777),"\n")
        pass
        note=""" here we can answer with a findnode or a ping """


 # rpl777_GUIpoll_findnode
 # # {
 # 'from': '167.114.2.94',
 # 'args': '[{"requestType":"findnode","NXT":"11910135804814382998","time":1418385453,"key":"2131686659786462901"},{"token":"crhllp9ko5ehtcf8j46plskln4hn2lkp2ph4kbm0e9edtp00v3muqttr8v90ma81pb3iaqaft4vb3qqp1739i4c98a41885d60ba3mpqd6mg78i8cf6nmp1fsdcrjpi1gs9beh4kvlpq5fq7nscmo6n6dsegr00v"}]',
 # 'port': 0,
 # 'result': '{"result":"kademlia_findnode from.(11910135804814382998) previp.(167.114.2.94) key.(2131686659786462901) datalen.0 txid.9930066001546457017"}'} <class 'dict'>




    def rpl777_GUIpoll_kademlia_pong(self, rpl777): #dataFrom777):
        """
        Note : Use python assert in the future
see PONG details in snAppy_doku


        """#

        #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")

        try:
            fromIp = rpl777['from']
            port = rpl777['port']
            args = rpl777['args']
            #log.msg(args, type(args))
            rpl777 = rpl777['result'] # this is a string!
            rpl777 = json.loads(rpl777)


        except Exception as e:
            #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            log.msg("Error rpl777_GUIpoll_kademlia_pong {0}".format(str(e)))


        rplArgs = json.loads(args) # <class 'list'> !!
        rplArgsRQ = rplArgs[0] # <class 'dict'>
        rplArgsTK = rplArgs[1]   #<class 'dict'>


        try:
            #log.msg(1*"\n~~~~ rplArgsRQ", rplArgsRQ)
            pubkey= rplArgsRQ['pubkey'] # check that this is really pubkey and not DHT key
            requestType= rplArgsRQ['requestType']
            ver =rplArgsRQ['ver']
            yourip =rplArgsRQ['yourip']
            yourport =rplArgsRQ['yourport']

            NXT =rplArgsRQ['NXT']
            time =rplArgsRQ['time']
            ipaddr =rplArgsRQ['ipaddr']

        except Exception as e:
            log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            log.msg("Error rplArgsRQ {0}".format(str(e)))
            #
            # occasional EXCEPT here!! check!
            #
            #

        try:
            port =  rpl777['port']
            numpings =  rpl777['numpings']
            lag  =  rpl777['lag']
            ipaddr  = rpl777['ipaddr']
            numpongs =  rpl777['numpongs']
            result =   rpl777['result']
            ave  =  rpl777['ave']
            NXT  = rpl777['NXT']
            log.msg("rpl777", rpl777,type(rpl777))

        except Exception as e:
            #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            log.msg("Error rpl777 {0}".format(str(e)))

        # further ACTION from here
        note= """ from here, we can go the next step, which is the findnode  TODO"""
        reqFindnode = {'requestType':'findnode'}


        reqFindnode['key']= NXT # the rea conf will be the havenode in uipoll
        self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqFindnode), headers=POSTHEADERS)
        self.deferred.addCallback(self.rpl777_df3_findnode ) # this is just for conf that we sent it
        self.deferred.addErrback(self.rpl777ERR)








    def rpl777_GUIpoll_kademlia_havenode(self, rpl777): #parse777_step1
        """

#got HAVENODE.([["7108754351996134253", "167.114.2.171", "7777", "0"], ["8566622688401875656", "37.59.108.92", "7777", "1418355409"], ["16196432036059823401", "167.114.2.203", "7777", "1418355386"], ["7067340061344084047", "94.102.50.70", "7777", "1418355591"], ["11634703838614499263", "69.90.132.106", "7777", "1418356230"], ["13594896385051583735", "192.99.246.20", "7777", "1418355386"], ["1978065578067355462", "89.212.19.49", "7777", "1418355370"]]) for key.(7108754351996134253) from 7108754351996134253



 GUIpoll ---> kademlia_havenode {'args': '[{"requestType":"havenode","NXT":"11910135804814382998","time":1418378252,"key":"11910135804814382998","data":[["11910135804814382998", "167.114.2.94", "7777", "0"], ["2131686659786462901", "85.178.204.233", "61312", "1418374115"], ["11634703838614499263", "69.90.132.106", "7777", "1418355887"], ["10694781281555936856", "209.126.70.170", "7777", "1418355569"], ["17265504311777286118", "184.175.25.117", "7777", "1418355277"], ["5624143003089008155", "192.99.212.250", "7777", "1418355253"], ["8894667849638377372", "209.126.70.156", "7777", "1418355643"]]},{"token":"crhllp9ko5ehtcf8j46plskln4hn2lkp2ph4kbm0e9edtp00v38sqttrls1eh801smc20bj8ebllvob2qn9vnotj5i4952fl450o08pmsbr03liiaftu4ljmbh7ofajod0tvl87edal1k5drbeemj4ul4b42j99c"}]', 'result': '{"result":"kademlia_havenode from NXT.11910135804814382998 key.(11910135804814382998) value.([["11910135804814382998", "167.114.2.94", "7777", "0"], ["2131686659786462901", "85.178.204.233", "61312", "1418374115"], ["11634703838614499263", "69.90.132.106", "7777", "1418355887"], ["10694781281555936856", "209.126.70.170", "7777", "1418355569"], ["17265504311777286118", "184.175.25.117", "7777", "1418355277"], ["5624143003089008155", "192.99.212.250", "7777", "1418355253"], ["8894667849638377372", "209.126.70.156", "7777", "1418355643"]])"}', 'port': 0, 'from': '167.114.2.94'} <class 'dict'>


  {"result":"kademlia_havenode from NXT.5624143003089008155 key.(5624143003089008155) value.([["5624143003089008155", "192.99.212.250", "7777", "0"], ["15178638394924629506", "167.114.2.206", "7777", "1417435953"], ["6249611027680999354", "80.41.56.181", "7777", "1417449705"], ["11910135804814382998", "167.114.2.94", "7777", "1417435991"], ["7581814105672729429", "187.153.194.200", "29693", "1417652256"], ["7108754351996134253", "167.114.2.171", "7777", "1417435991"], ["16196432036059823401", "167.114.2.203", "7777", "1417435957"]])"}


  {"result":"kademlia_havenode from NXT.12315166155634751985 key.(12315166155634751985) value.([["12315166155634751985", "167.114.2.205", "7777", "0"], ["13594896385051583735", "192.99.246.20", "7777", "1418309439"], ["16196432036059823401", "167.114.2.203", "7777", "1418308928"], ["8923034930361863607", "192.99.246.33", "7777", "1418308929"], ["7581814105672729429", "187.153.143.36", "27190", "1418308969"], ["7108754351996134253", "167.114.2.171", "7777", "1418308950"], ["11634703838614499263", "69.90.132.106", "7777", "1418308973"]])"} <class 'str'>


# make ad hoc here, put into nice class later.
# b'{"result":"kademlia_findnode from.(2131686659786462901) previp.() key.(3571143576961987768) datalen.0 txid.1496458648985206585"}'


GUIpoll ---> kademlia_havenode



{'port': 0, 'args': '[{"requestType":"havenode","NXT":"11910135804814382998","time":1418378474,"key":"11910135804814382998","data":[["11910135804814382998", "167.114.2.94", "7777", "0"], ["2131686659786462901", "85.178.204.233", "61312", "1418374115"], ["11634703838614499263", "69.90.132.106", "7777", "1418355887"], ["10694781281555936856", "209.126.70.170", "7777", "1418355569"], ["17265504311777286118", "184.175.25.117", "7777", "1418355277"], ["5624143003089008155", "192.99.212.250", "7777", "1418355253"], ["8894667849638377372", "209.126.70.156", "7777", "1418355643"]]},{"token":"crhllp9ko5ehtcf8j46plskln4hn2lkp2ph4kbm0e9edtp00v39akttr3oogmkg1nadgia072k06a9nggjaab7fj8mkhl0bqr364sskelrk0gihn85f3rqlriekbdub8vudcs1k27kkgetsmq8u53qoedjgaujep"}]', 'result': '{"result":"kademlia_havenode from NXT.11910135804814382998 key.(11910135804814382998) value.([["11910135804814382998", "167.114.2.94", "7777", "0"], ["2131686659786462901", "85.178.204.233", "61312", "1418374115"], ["11634703838614499263", "69.90.132.106", "7777", "1418355887"], ["10694781281555936856", "209.126.70.170", "7777", "1418355569"], ["17265504311777286118", "184.175.25.117", "7777", "1418355277"], ["5624143003089008155", "192.99.212.250", "7777", "1418355253"], ["8894667849638377372", "209.126.70.156", "7777", "1418355643"]])"}', 'from': '167.114.2.94'} <class 'dict'>


so for the recipient of the find node, the result is havenode

to the sender of the find, it comes back as a new havenode command


 {'args': '[{"requestType":"havenode","NXT":"7108754351996134253","time":1418479724,"key":"5624143003089008155","data":[["5624143003089008155", "192.99.212.250", "7777", "1418404010"], ["15178638394924629506", "167.114.2.206", "7777", "1418404020"], ["11910135804814382998", "167.114.2.94", "7777", "1418404026"], ["6216883599460291148", "192.99.246.126", "7777", "1418404037"], ["7108754351996134253", "167.114.2.171", "7777", "0"], ["16196432036059823401", "167.114.2.203", "7777", "1418404056"], ["10694781281555936856", "209.126.70.170", "7777", "1418404083"]]},{"token":"j8edkcsu69k3e3e0ru9p4f6fepega7dijt24dh71h9kfqsg6v9f2qvp32o45gi01i19t5ioutef3te5fccvmnb91tuv0edt4tm2t4oq5ba9gfllceq7v3i63qptb79nbsfta194mr47nftrkgs257oimekhcmmtb"}]', 'from': '167.114.2.171', 'result': '{"result":"kademlia_havenode from NXT.7108754351996134253 key.(5624143003089008155) value.([["5624143003089008155", "192.99.212.250", "7777", "1418404010"], ["15178638394924629506", "167.114.2.206", "7777", "1418404020"], ["11910135804814382998", "167.114.2.94", "7777", "1418404026"], ["6216883599460291148", "192.99.246.126", "7777", "1418404037"], ["7108754351996134253", "167.114.2.171", "7777", "0"], ["16196432036059823401", "167.114.2.203", "7777", "1418404056"], ["10694781281555936856", "209.126.70.170", "7777", "1418404083"]])"}', 'port': 0} <class 'dict'>


    """#

        log.msg("\nGUIpoll ---> kademlia_havenode",rpl777, type(rpl777),"\n")

        try:
            fromIp = rpl777['from']
            port = rpl777['port']
            rplArgs = rpl777['args']
            try:
                rplArgs=json.loads(rplArgs)

            except Exception as e:
                log.msg("Error args {0}".format(str(e)))
                log.msg("args NOT ok",rplArgs, type(rplArgs))

            rpl777 = rpl777['result'] # this is a string!

            try:
                #print(5*"\n~rpl777_GUIpoll_kademlia_havenode ~+>", rpl777, type(rpl777))
                rpl777SPL=rpl777.split('([')
                prefix = rpl777SPL[0]
                #'{"result":"kademlia_havenode from NXT.11910135804814382998 key.(11910135804814382998) value.'
                # can extract NXT and key from here if need be
                havenodesStr=rpl777SPL[1].split('])')[0]
                # nice str now:
                #'["11910135804814382998", "167.114.2.94", "7777", "0"], ["2131686659786462901", "85.178.204.233", "61312", "1418374115"], ["10694781281555936856", "209.126.70.170", "7777", "1418355569"], ["11634703838614499263", "69.90.132.106", "7777", "1418355887"], ["17265504311777286118", "184.175.25.117", "7777", "1418355277"], ["5624143003089008155", "192.99.212.250", "7777", "1418355253"], ["8894667849638377372", "209.126.70.156", "7777", "1418355643"]'
                rpl777Li=eval(havenodesStr)
                # list now:
                # (['11910135804814382998', '167.114.2.94', '7777', '0'],
                #  ['2131686659786462901', '85.178.204.233', '61312', '1418374115'],
                #  ['10694781281555936856', '209.126.70.170', '7777', '1418355569'],
                #  ['11634703838614499263', '69.90.132.106', '7777', '1418355887'],
                #  ['17265504311777286118', '184.175.25.117', '7777', '1418355277'],
                #  ['5624143003089008155', '192.99.212.250', '7777', '1418355253'],
                #  ['8894667849638377372', '209.126.70.156', '7777', '1418355643'])
                rpl777 = {'havenodes':rpl777Li}

            except Exception as e:
                log.msg("Error args {0}".format(str(e)))
                log.msg("2",rpl777, type(rpl777))

        except Exception as e:
            #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            log.msg("Error rpl777_GUIpoll_kademlia_havenode {0}".format(str(e)))

        rplArgsRQ = rplArgs[0]
        rplArgsTK = rplArgs[1]
        #log.msg(5*"\nargs ----> ",rplArgsRQ, type(rplArgsRQ))

        # There are two types of havendoe

        # for key in rplArgsRQ.keys():
        #     print(key, " - " , rplArgsRQ[key])

         #{'time': 1418380620, 'requestType': 'havenode', 'NXT': '5624143003089008155', 'key': '5624143003089008155', 'data': [['5624143003089008155', '192.99.212.250', '7777', '0'], ['7067340061344084047', '94.102.50.70', '7777', '1418355322'], ['15178638394924629506', '167.114.2.206', '7777', '1418355261'], ['6249611027680999354', '80.41.56.181', '7777', '1418375808'], ['11910135804814382998', '167.114.2.94', '7777', '1418355255'], ['6216883599460291148', '192.99.246.126', '7777', '1418355291'], ['16196432036059823401', '167.114.2.203', '7777', '1418355258']]}

        try:
            data = rplArgsRQ['data']

        except Exception as e:
            #log.msg("GUIpoll ---> kademlia_pong",rpl777, type(rpl777),"\n")
            log.msg("Error data = rplArgsRQ['data']   {0}".format(str(e)))

        #log.msg(rplArgsTK, type(rplArgsTK))
        #log.msg(5*"\n++++++++++++++++kademlia_havenode",rpl777, type(rpl777))
        #log.msg(1*"\n              data",data, type(data))

        reqPing = {'requestType':'ping'}
        reqFindnode = {'requestType':'findnode'}
        log.msg(1*"\n FINDNODE & PING all:", rpl777Li)
        for node in rpl777Li:
        #            ping and findnode!

            if node[1] not in self.nodeDi.keys():
                self.nodeDi[node[1]] = node[0] # add this to the internal list of known nodes

        reqPing['destip']=node[1]
        self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqPing), headers=POSTHEADERS)
        self.deferred.addCallback(self.rpl777_df2_ping)
        self.deferred.addErrback(self.rpl777ERR)

        reqFindnode['key']=node[0]
        self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqFindnode), headers=POSTHEADERS)
        self.deferred.addCallback(self.rpl777_df2_ping)
        self.deferred.addErrback(self.rpl777ERR)


        note=""" data in RQ is the same as in havenodes! ?!?!?! : now do the findonde and poing thing fronm here! """









###################################
###################################
###################################
###################################
###################################
###################################

        #
        #
        # non GUIpoll api talk here
        #
        #


    def rpl777_getpeers_df1(self, dataFrom777): #these are the basic pings from the whitlist
        """

         peers [{'pubkey': '05a7612d54d14c21be9baa654ad50b4ba423eea0735185ac732ada2332315c3f', 'RS': 'NXT-8AF7-ESB7-GHFM-896JY', 'privateNXT': '8016556209183334821'}, {'RS': 'NXT-7PPP-R6AJ-VSJ7-37C7V', 'pserver': {'recv': 8, 'lastrecv': 14.0111578, 'lastsent': 14.01127447, 'pings': 1, 'sent': 8}, 'srvipaddr': '178.62.185.131', 'recv': 8, 'srvNXT': '2131686659786462901', 'pubkey': '849c97e5b1e8c50429249eff867de5e6ded39d34a6ccc9c42ea720d927a12d18', 'sent': 8}, {'RS': 'NXT-EZJ4-8F5T-8VX4-FVCB7', 'pserver': {'lastrecv': 0.6551996, 'lastsent': 0.06295793, 'pingtime': 231, 'avetime': 3893.46431672, 'recv': 155, 'pings': 63, 'pongs': 63, 'sent': 178}, 'srvipaddr': '167.114.2.206', 'recv': 155, 'srvNXT': '15178638394924629506', 'pubkey': '52e3524b5392a2ecba9e702a0c9c04d3d73dc4f93008977e1bcd15ea5bd5b376', 'sent': 178}, {'RS': 'NXT-5TU8-78XL-W2CW-32WWQ', 'pserver': {'lastrecv': 0.07671293, 'lastsent': 0.00977127, 'pingtime': 176.5, 'avetime': 18793.97457429, 'recv': 188, 'pings': 83, 'pongs': 84, 'sent': 205}, 'srvipaddr': '89.212.19.49', 'recv': 188, 'srvNXT': '1978065578067355462', 'pubkey': 'c269a8b4567c0b3062e6c4be859d845c4b808a405dd03d0d1ac7b4d9cb725b40', 'sent': 205}, {'RS': 'NXT-A4NA-7P8Y-MDMZ-3K4AZ', 'pserver': {'lastrecv': 0.07303403, 'lastsent': 0.07965903, 'pingtime': 327.75, 'avetime': 33324.18828125, 'recv': 35, 'pings': 9, 'pongs': 11, 'sent': 81}, 'srvipaddr': '167.114.2.204', 'recv': 35, 'srvNXT': '2278910666471639688', 'pubkey': '47faa8a876ae56be36a1d214515d0ef3f9ff99b06f4d2702acf0380cab7ccc5e', 'sent': 81}, {'RS': 'NXT-JNLE-Q9XW-MG8P-7GQKE', 'pserver': {'lastrecv': 0.05130237, 'lastsent': 0.0543357, 'pingtime': 36882.25, 'avetime': 13861.70690789, 'recv': 127, 'pings': 47, 'pongs': 48, 'sent': 174}, 'srvipaddr': '192.99.246.126', 'recv': 127, 'srvNXT': '6216883599460291148', 'pubkey': '2fdfab9d3d5e1c91a27e48ed7422ebcea628ebdf36ea0052fdd62e1533a8751d', 'sent': 174}, {'RS': 'NXT-YPWQ-F7SB-WCD7-CFCLC', 'pserver': {'lastrecv': 0.01943838, 'lastsent': 0.02329255, 'pingtime': 295, 'avetime': 7594.5688101, 'recv': 104, 'pings': 38, 'pongs': 40, 'sent': 131}, 'srvipaddr': '167.114.2.94', 'recv': 104, 'srvNXT': '11910135804814382998', 'pubkey': '34e55ae366e8b11e5dc195f29a0d9999567123b9c02e4a621600e4de5c72bb77', 'sent': 131}, {'RS': 'NXT-NHBB-5ZF3-4WTB-GBCK3', 'pserver': {'lastrecv': 2.37580073, 'lastsent': 0.0236049, 'pingtime': 52420.75, 'avetime': 7924.83104292, 'recv': 193, 'pings': 84, 'pongs': 82, 'sent': 181}, 'srvipaddr': '167.114.2.203', 'recv': 193, 'srvNXT': '16196432036059823401', 'pubkey': 'be3db1badadb0e95b8afd2f1f5f53df7837de15c14f09f7a531c489a3f470543', 'sent': 181}, {'RS': 'NXT-Y5FR-ZSRB-BQWC-9W9PR', 'pserver': {'lastrecv': 1.36517293, 'lastsent': 0.03602293, 'pingtime': 93572, 'avetime': 20840.15337171, 'recv': 96, 'pings': 37, 'pongs': 39, 'sent': 104}, 'srvipaddr': '192.99.246.33', 'recv': 96, 'srvNXT': '8923034930361863607', 'pubkey': 'ea83e39d553470725960180afb25afffe3de1fe0019979236b96536e22e1ed29', 'sent': 104}, {'RS': 'NXT-VSVF-FFF5-M4EX-8YUB7', 'pserver': {'lastrecv': 0.04354165, 'lastsent': 0.00936665, 'pingtime': 36595.5, 'avetime': 9679.23729884, 'recv': 188, 'pings': 90, 'pongs': 77, 'sent': 224}, 'srvipaddr': '167.114.2.171', 'recv': 188, 'srvNXT': '7108754351996134253', 'pubkey': '9e33da1c9ac00d376832cf3c9293dfb21d055d76e1c446449f0672fd688a237f', 'sent': 224}, {'RS': 'NXT-DGHK-DUWA-2MRL-C44UP', 'pserver': {'lastrecv': 1.73030202, 'lastsent': 0.00871452, 'pingtime': 45173.25, 'avetime': 9300.74114583, 'recv': 134, 'pings': 62, 'pongs': 58, 'sent': 130}, 'srvipaddr': '167.114.2.205', 'recv': 134, 'srvNXT': '12315166155634751985', 'pubkey': 'eef155b7c8c50dc62ae45f40c30d2b1a0874ca5f5f11adeef7637933d863583b', 'sent': 130}, {'RS': 'NXT-WXJV-AFNK-YW5D-6S95W', 'pserver': {'lastrecv': 1.77902338, 'lastsent': 0.02744422, 'pingtime': -156179, 'avetime': 10604.32024083, 'recv': 114, 'pings': 63, 'pongs': 46, 'sent': 157}, 'srvipaddr': '192.99.212.250', 'recv': 114, 'srvNXT': '5624143003089008155', 'pubkey': 'ecea0d22fca77e28210c0b4c05b8bd16ff8003e5065c09f4e73105398e31840f', 'sent': 157}, {'RS': 'NXT-VT9R-9GYM-YLJF-D8QCT', 'pserver': {'lastrecv': 1.15555233, 'lastsent': 0.01185233, 'pingtime': 223334, 'avetime': 39925.74770221, 'recv': 123, 'pings': 50, 'pongs': 52, 'sent': 134}, 'srvipaddr': '192.99.246.20', 'recv': 123, 'srvNXT': '13594896385051583735', 'pubkey': '430695694b02bb71e8222e1e5d20b1c985afd9ba899e25fe2d52ee1be92f532c', 'sent': 134}, {'RS': 'NXT-UE4H-CXMN-HR75-8W376', 'pserver': {'lastrecv': 4.86252565, 'lastsent': 0.02568398, 'pingtime': -3670675.75, 'avetime': 12546.13709677, 'recv': 14, 'pings': 30, 'pongs': 1, 'sent': 158}, 'srvipaddr': '94.102.50.70', 'recv': 14, 'srvNXT': '7067340061344084047', 'pubkey': '4bd4794f0a77d22949c944f96f9b7a429021e59644a98eea310546fd47b96440', 'sent': 158}, {'RS': 'NXT-XSQA-YBXH-CW2M-93QSF', 'pserver': {'lastrecv': 1.1530546, 'lastsent': 0.05522543, 'pingtime': 371363.25, 'avetime': 83528.03227459, 'recv': 54, 'pings': 41, 'pongs': 20, 'sent': 143}, 'srvipaddr': '37.59.108.92', 'recv': 54, 'srvNXT': '8566622688401875656', 'pubkey': '5a1c33c1e00cec3beecb9a9fcd8379fe61d6a661566875cf0cff89726b27b76f', 'sent': 143}]
         peers is a LIST!

         [

         {'pubkey': '05a7612d54d14c21be9baa654ad50b4ba423eea0735185ac732ada2332315c3f', 'RS': 'NXT-8AF7-ESB7-GHFM-896JY', 'privateNXT': '8016556209183334821'},

         {'RS': 'NXT-7PPP-R6AJ-VSJ7-37C7V', 'pserver': {'recv': 8, 'lastrecv': 14.0111578, 'lastsent': 14.01127447, 'pings': 1, 'sent': 8},
         'srvipaddr': '178.62.185.131', 'recv': 8, 'srvNXT': '2131686659786462901', 'pubkey': '849c97e5b1e8c50429249eff867de5e6ded39d34a6ccc9c42ea720d927a12d18', 'sent': 8},

         {'RS': 'NXT-EZJ4-8F5T-8VX4-FVCB7', 'pserver': {'lastrecv': 0.6551996, 'lastsent': 0.06295793, 'pingtime': 231, 'avetime': 3893.46431672, 'recv': 155, 'pings': 63, 'pongs': 63, 'sent': 178},
          'srvipaddr': '167.114.2.206', 'recv': 155, 'srvNXT': '15178638394924629506', 'pubkey': '52e3524b5392a2ecba9e702a0c9c04d3d73dc4f93008977e1bcd15ea5bd5b376', 'sent': 178},

          {'RS': 'NXT-5TU8-78XL-W2CW-32WWQ', 'pserver': {'lastrecv': 0.07671293, 'lastsent': 0.00977127, 'pingtime': 176.5, 'avetime': 18793.97457429, 'recv': 188, 'pings': 83, 'pongs': 84, 'sent': 205}, 'srvipaddr': '89.212.19.49', 'recv': 188, 'srvNXT': '1978065578067355462', 'pubkey': 'c269a8b4567c0b3062e6c4be859d845c4b808a405dd03d0d1ac7b4d9cb725b40', 'sent': 205},
          {'RS': 'NXT-A4NA-7P8Y-MDMZ-3K4AZ', 'pserver': {'lastrecv': 0.07303403, 'lastsent': 0.07965903, 'pingtime': 327.75, 'avetime': 33324.18828125, 'recv': 35, 'pings': 9, 'pongs': 11, 'sent': 81}, 'srvipaddr': '167.114.2.204', 'recv': 35, 'srvNXT': '2278910666471639688', 'pubkey': '47faa8a876ae56be36a1d214515d0ef3f9ff99b06f4d2702acf0380cab7ccc5e', 'sent': 81},
          {'RS': 'NXT-JNLE-Q9XW-MG8P-7GQKE', 'pserver': {'lastrecv': 0.05130237, 'lastsent': 0.0543357, 'pingtime': 36882.25, 'avetime': 13861.70690789, 'recv': 127, 'pings': 47, 'pongs': 48, 'sent': 174}, 'srvipaddr': '192.99.246.126', 'recv': 127, 'srvNXT': '6216883599460291148', 'pubkey': '2fdfab9d3d5e1c91a27e48ed7422ebcea628ebdf36ea0052fdd62e1533a8751d', 'sent': 174},
        {'RS': 'NXT-YPWQ-F7SB-WCD7-CFCLC', 'pserver': {'lastrecv': 0.01943838, 'lastsent': 0.02329255, 'pingtime': 295, 'avetime': 7594.5688101, 'recv': 104, 'pings': 38, 'pongs': 40, 'sent': 131}, 'srvipaddr': '167.114.2.94', 'recv': 104, 'srvNXT': '11910135804814382998', 'pubkey': '34e55ae366e8b11e5dc195f29a0d9999567123b9c02e4a621600e4de5c72bb77', 'sent': 131},
        {'RS': 'NXT-NHBB-5ZF3-4WTB-GBCK3', 'pserver': {'lastrecv': 2.37580073, 'lastsent': 0.0236049, 'pingtime': 52420.75, 'avetime': 7924.83104292, 'recv': 193, 'pings': 84, 'pongs': 82, 'sent': 181}, 'srvipaddr': '167.114.2.203', 'recv': 193, 'srvNXT': '16196432036059823401', 'pubkey': 'be3db1badadb0e95b8afd2f1f5f53df7837de15c14f09f7a531c489a3f470543', 'sent': 181},
         {'RS': 'NXT-Y5FR-ZSRB-BQWC-9W9PR', 'pserver': {'lastrecv': 1.36517293, 'lastsent': 0.03602293, 'pingtime': 93572, 'avetime': 20840.15337171, 'recv': 96, 'pings': 37, 'pongs': 39, 'sent': 104}, 'srvipaddr': '192.99.246.33', 'recv': 96, 'srvNXT': '8923034930361863607', 'pubkey': 'ea83e39d553470725960180afb25afffe3de1fe0019979236b96536e22e1ed29', 'sent': 104},
         {'RS': 'NXT-VSVF-FFF5-M4EX-8YUB7', 'pserver': {'lastrecv': 0.04354165, 'lastsent': 0.00936665, 'pingtime': 36595.5, 'avetime': 9679.23729884, 'recv': 188, 'pings': 90, 'pongs': 77, 'sent': 224}, 'srvipaddr': '167.114.2.171', 'recv': 188, 'srvNXT': '7108754351996134253', 'pubkey': '9e33da1c9ac00d376832cf3c9293dfb21d055d76e1c446449f0672fd688a237f', 'sent': 224},
          {'RS': 'NXT-DGHK-DUWA-2MRL-C44UP', 'pserver': {'lastrecv': 1.73030202, 'lastsent': 0.00871452, 'pingtime': 45173.25, 'avetime': 9300.74114583, 'recv': 134, 'pings': 62, 'pongs': 58, 'sent': 130}, 'srvipaddr': '167.114.2.205', 'recv': 134, 'srvNXT': '12315166155634751985', 'pubkey': 'eef155b7c8c50dc62ae45f40c30d2b1a0874ca5f5f11adeef7637933d863583b', 'sent': 130},
         {'RS': 'NXT-WXJV-AFNK-YW5D-6S95W', 'pserver': {'lastrecv': 1.77902338, 'lastsent': 0.02744422, 'pingtime': -156179, 'avetime': 10604.32024083, 'recv': 114, 'pings': 63, 'pongs': 46, 'sent': 157}, 'srvipaddr': '192.99.212.250', 'recv': 114, 'srvNXT': '5624143003089008155', 'pubkey': 'ecea0d22fca77e28210c0b4c05b8bd16ff8003e5065c09f4e73105398e31840f', 'sent': 157},
         {'RS': 'NXT-VT9R-9GYM-YLJF-D8QCT', 'pserver': {'lastrecv': 1.15555233, 'lastsent': 0.01185233, 'pingtime': 223334, 'avetime': 39925.74770221, 'recv': 123, 'pings': 50, 'pongs': 52, 'sent': 134}, 'srvipaddr': '192.99.246.20', 'recv': 123, 'srvNXT': '13594896385051583735', 'pubkey': '430695694b02bb71e8222e1e5d20b1c985afd9ba899e25fe2d52ee1be92f532c', 'sent': 134},
         {'RS': 'NXT-UE4H-CXMN-HR75-8W376', 'pserver': {'lastrecv': 4.86252565, 'lastsent': 0.02568398, 'pingtime': -3670675.75, 'avetime': 12546.13709677, 'recv': 14, 'pings': 30, 'pongs': 1, 'sent': 158}, 'srvipaddr': '94.102.50.70', 'recv': 14, 'srvNXT': '7067340061344084047', 'pubkey': '4bd4794f0a77d22949c944f96f9b7a429021e59644a98eea310546fd47b96440', 'sent': 158},
         {'RS': 'NXT-XSQA-YBXH-CW2M-93QSF', 'pserver': {'lastrecv': 1.1530546, 'lastsent': 0.05522543, 'pingtime': 371363.25, 'avetime': 83528.03227459, 'recv': 54, 'pings': 41, 'pongs': 20, 'sent': 143}, 'srvipaddr': '37.59.108.92', 'recv': 54, 'srvNXT': '8566622688401875656', 'pubkey': '5a1c33c1e00cec3beecb9a9fcd8379fe61d6a661566875cf0cff89726b27b76f', 'sent': 143}

          ]


        """#
        repl=dataFrom777.json()
        #log.msg(1*"\nrpl777_getpeers_df1", type(repl))
        #log.msg(repl.keys())

        Numnxtaccts = repl['Numnxtaccts']
        peers = repl['peers']
        Numpservers = repl['Numpservers']
        num = repl['num']
        log.msg("Numnxtaccts", Numnxtaccts)
        #log.msg("peers", peers)
        log.msg("Numpservers", Numpservers)
        log.msg("num", num)


        #print(12*"\ncollected here: ", self.nodeDi)



        for peer in peers:
            pass#print(peer)
        #
        # for peer in repl.keys():
        #     log.msg(peer , " - ", repl[peer], "\n")
        #print("+++++++++++++++++++")



    def rpl777_settings_df1(self, dataFrom777): #these are the basic pings from the whitlist
        """"""#
        repl=dataFrom777.json()
        reqPing = {'requestType':'ping'}

        # self.nodeDi[node[1]] = node[0]
        #'one' in dict.values() easy

        ipsToPing=repl['whitelist'] #[0] # singlecheck
        #ipsToPing = 10* ['178.62.185.131'] # stonefish['80.41.56.181'] # ['85.178.202.108']   #

        for node in ipsToPing:
            reqPing['destip']=node
            self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqPing), headers=POSTHEADERS)
            self.deferred.addCallback(self.rpl777_df2_ping)
            self.deferred.addErrback(self.rpl777ERR)

#        self.rpl777_pingDB_df1()




    def rpl777_pingDB_df1(self, ):#dataFrom777):
        """"""#
        #repl=dataFrom777.json()
        reqPing = {'requestType':'ping'}

        # create internal peerlist,
        # init that with the whitelist and extend

        #'one' in dict.values() easy


        # create internal peerlist,
        #log.msg(1*"\npinging these nodeDi",self.nodeDi.keys())
        for node in self.nodeDi.keys():
            reqPing['destip']=node
            self.deferred = deferToThread(requests.post, FULL_URL, data=json.dumps(reqPing), headers=POSTHEADERS)
            self.deferred.addCallback(self.rpl777_df2_ping)
            self.deferred.addErrback(self.rpl777ERR)




    def rpl777_df2_ping(self, dataFrom777):
        """
        ---->rpl777 ping {'result': 'kademlia_ping to 100.79.14.220', 'txid': '0'}
        when we have done ping it does not init a callback, because that is PONG we have to wait for

        """#
        repl=dataFrom777.json()
        repl=dataFrom777.content.decode("utf-8")
        repl=eval(repl)
        #log.msg( 1 * "ping sent", repl)




    def rpl777_df3_findnode(self, dataFrom777):
        """
        ---->rpl777_df3_findnode

        """#
        repl=dataFrom777.json()
        repl=dataFrom777.content.decode("utf-8")
        repl=eval(repl)
        log.msg( 1 * "\ndone findnode", repl)



    def rpl777ERR(self, ERR777):

        print(ERR777)

        raise RuntimeError






#./BitcoinDarkd SuperNET '{"requestType":"store","key":"116876777391303227","data":"deadbee32f"}'
#./BitcoinDarkd SuperNET '{"requestType":"findvalue","key":"116876777391303227"}'
# havenodeB ???






class UC_Scheduler_XML(object):
    """
    demo for xml. fetches three hardcoded xml oages from sportsdatallc.

    """#

    def __init__(self, serverFactory ,  environ = {} ):

        # ToDo: the schedules and their details must be registered in the ENVIROINMENT! - including the filenames where they go to
        #
        self.environ = environ
        self.schedules = {} #schedules # this contains the schedules

        prepSchedules = environ['envSportsData']
        for sched in prepSchedules.keys():
            sched = prepSchedules[sched]
            self.schedules[ sched['schedName']   ] = Schedule( sched )

        self.proxyServerFactory = serverFactory #probably not needed

        self.ucFactory = ClientFactory()

        self.qComp_XML = serverFactory.qComp_XML
        self.parser_XML = serverFactory.parser_XML
        # self.schedulerProtocol_XML = SchedulerProtocol_XML(self)
        # this probably only gets me ONE self.schedulerProtocol_XML ONLY! ?!?!



    def periodic(self, ):
        """ this is the method that is called periodically by the twisted loopingTask.
         This contains the UseCase logic, ie needs to check what to do, and then do it. """#

        scheduledReqs =[]
        #print( "Scheduler ", self, " MAIN scheduled Heartbeat: ", datetime.now())

        for schedule in self.schedules.keys():
            schedule = self.schedules[schedule]

            if schedule.callMe():
                scheduledReqs.append(schedule)

        self.makeScheduledRequests(scheduledReqs)


    def makeScheduledRequests(self,scheduledReqs):

        for req in scheduledReqs:

            time.sleep(1.01) # constraint on demo account sportsdataLLC
            requestOUT = req.schedule['target'].encode("utf-8")
            #
            self.uc_Factory = ClientFactory()
            self.uc_Factory.protocol = SchedulerProtocol_XML()
            self.uc_Factory.protocol.connectionMade(requestOUT)
            #self.schedulerProtocol_XML.connectionMade(requestOUT)# only using a proto may yield errs?!


    def receiveFromProtocol(self, dataFromProto):

        print(1 * "\nscheduled refresh of data here. update to file by saving it")
        self.result = dataFromProto
        log.msg(1 * "----> **** SchedulerProtocol_XML dataReceived - from remoteServer: ", dataFromProto[:200], str(len(dataFromProto)),"\n-----",time.time(),"\n\n")
        # ToDo SAVE HERE TO FILES- look up files in environ


# ENABLE THE SCHEDULERS TO OPERATE THE SERVERFACTORY JUST AS REQUESTS
# make a new class for each scheduler.
# maybe later concentrae functionality in a superclass to be subclassed





#
#
# class SchedulerProtocol_777(protocol.Protocol):
#     """ this can be used for scheduled SuperNET tasks
#     """#
#
#     def __init__(self,  scheduler):
#         super(SchedulerProtocol_777, self).__init__()
#         self.scheduler = scheduler
#
#
#     def connectionMade(self, requestOUT = None):
#         """ connection made here means that we are called by the scheduler  """#
#         print(1*"\n++++++++++SchedulerProtocol_777 connectionMade - Scheduled Check")
#         try:
#             self.requestOUT = requestOUT
#         except:
#             self.transport.loseConnection()
#             return None
#         self.getPage_deferred =  getPage(self.requestOUT)
#         print(1*"\n++++++++++SchedulerProtocol_777 connectionMade - Scheduled Check", self.requestOUT)
#         self.getPage_deferred.addCallback(self.pageReceived)
#         self.getPage_deferred.addErrback(self.handleFailure)
#         self.requestOUT = ''
#
#     # Server => Proxy
#     def handleFailure(self, err):
#         raise RuntimeError(str(err))
#
#     # this will be the deferreed
#     def pageReceived(self, data):
#         log.msg(1*"\n scheduled pageReceived - from remoteServer: ", data[:200], str(len(data)),"\n\n")
#         self.scheduler.receiveFromProtocol(data)
#         return None









class SchedulerProtocol_XML(protocol.Protocol):
    """
    This works but there is a number of things I am unsure about.
        I don't know if this is a singleton or throwaway Proto like with the others.
        Also, I don't quite know about the contorl flow, I call a method on the scheduler to get rid of the data
        that has jus tbeen recevied, and I don't know if we ever get back in to the deferred 'pagereceived.
        Normally, Protocols use the 'loseConnection'. When I do this I get execptions because I jump out of here when throwing out the data,
        and the connection is not not closed. so if we just do it like this it may be hunky dory. lets see.
        Maybe it IS neccessary to loseconnection() ???? it does not appear so atm"""#

    def __init__(self,  ):#scheduler):
        super(SchedulerProtocol_XML, self).__init__()
        #self.scheduler = scheduler

# SchedulerProtocol_XML connectionMade:  None b'http://api.sportsdatallc.org/soccer-t2/eu/schema/matches-schedule.xml?api_key=fv37s4rd2arqqxav774wb2kc'

    def connectionMade(self, requestOUT ):
        """ connection made here means that we are called by the scheduler  """#
        print(10*"\nSchedulerProtocol_XML connectionMade: ", requestOUT, self )
        try:
            self.requestOUT = requestOUT
        except:
            self.transport.loseConnection()
            return None

        self.getPage_deferred =  getPage(self.requestOUT)
        print(3*"\nSchedulerProtocol_XML connectionMade - Scheduled Check", self.requestOUT)

        self.getPage_deferred.addCallback(self.pageReceived)
        self.getPage_deferred.addErrback(self.handleFailure)
        self.requestOUT = ''
        self.query_xmlFeed1 = False
        #log.msg("-SchedulerProtocol_XML-- sending scheduled request out----->:", self.requestOUT) # only for GET , ppOST is different

    # Server => Proxy
    def handleFailure(self, err):
        raise RuntimeError(str(err))

    # this will be the deferreed
    def pageReceived(self, data):
        log.msg(12*"\n scheduled pageReceived - from remoteServer: ", data[:1200], str(len(data)),"\n\n")
        #self.scheduler.receiveFromProtocol(data)
        #b'http://api.sportsdatallc.org/soccer-t2/eu/matches/2014/08/21/summary.xml?api_key=fv37s4rd2arqqxav774wb2kc'>
        return None
