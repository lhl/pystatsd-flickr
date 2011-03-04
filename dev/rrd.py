#!/usr/bin/env python                                                              
import corestats                                                                   

sequence = [1, 2.5, 7, 13.4, 8.0]                                                  
sats = corestats.Stats(sequence)                                                  
print 'avg', stats.avg()
print 'med', stats.median()
print 'min', stats.min()
print 'max', stats.max()
print 'p25', stats.percentile(25)
print 'p50', stats.percentile(50)
print 'p75', stats.percentile(75)
print 'sd ', stats.stdev()
print 'ct ', stats.count()


# Create Test RRD
import time
from pyrrd.rrd import DataSource, RRA, RRD


# Load Data
'''
rrd = RRD(filename, mode="w")
getData
'''


# Filename
filename = '/tmp/test.rrd'

dataSources = []
dataSources.append( DataSource(dsName='q1', dsType='GAUGE', heartbeat=600, minval=0) )
dataSources.append( DataSource(dsName='q2', dsType='GAUGE', heartbeat=600, minval=0) )
dataSources.append( DataSource(dsName='q3', dsType='GAUGE', heartbeat=600, minval=0) )
dataSources.append( DataSource(dsName='lo', dsType='GAUGE', heartbeat=600, minval=0) )
dataSources.append( DataSource(dsName='hi', dsType='GAUGE', heartbeat=600, minval=0) )
dataSources.append( DataSource(dsName='total', dsType='GAUGE', heartbeat=600, minval=0) )

roundRobinArchives = []
roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=1, rows=8640)) # 24h at 1 sample per 10 secs
roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=90, rows=2880)) # 1 month at 1 sample per 15 mins
roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=2880, rows=5475)) # 5 years at 1 sample per 8 hours

# starttime - now; step = resolution (10s)
myRRD = RRD(filename, step=10, ds=dataSources, rra=roundRobinArchives, start=int(time.time()))
myRRD.create()

# Test for file existence
import os
os.path.isfile(filename)

# Values
# myRRD.bufferValue(str(time.time()), 'q1:q2:q3:lo:hi:total')
myRRD.bufferValue(str(int(time.time())), '1:2:3:0:5:100')
myRRD.bufferValue(str(int(time.time())), '1.2:2.2:3.2:0.2:5.2:90')
myRRD.update()


# Information    
myRRD.info()


# Graph
from pyrrd.graph import DEF, CDEF, VDEF, LINE, AREA, GPRINT
def1 = DEF(rrdfile=myRRD.filename, vname='myspeed', dsName=dataSource.name)
cdef1 = CDEF(vname='kmh', rpn='%s,3600,*' % def1.vname)
cdef2 = CDEF(vname='fast', rpn='kmh,100,GT,kmh,0,IF')
cdef3 = CDEF(vname='good', rpn='kmh,100,GT,0,kmh,IF')
vdef1 = VDEF(vname='mymax', rpn='%s,MAXIMUM' % def1.vname)
vdef2 = VDEF(vname='myavg', rpn='%s,AVERAGE' % def1.vname)
    
line1 = LINE(value=100, color='#990000', legend='Maximum Allowed')
area1 = AREA(defObj=cdef3, color='#006600', legend='Good Speed')
area2 = AREA(defObj=cdef2, color='#CC6633', legend='Too Fast')
line2 = LINE(defObj=vdef2, color='#000099', legend='My Average', stack=True)
gprint1 = GPRINT(vdef2, '%6.2lf kph')
    

# Color    
from pyrrd.graph import ColorAttributes
ca = ColorAttributes()
ca.back = '#333333'
ca.canvas = '#333333'
ca.shadea = '#000000'
ca.shadeb = '#111111'
ca.mgrid = '#CCCCCC'
ca.axis = '#FFFFFF'
ca.frame = '#AAAAAA'
ca.font = '#FFFFFF'
ca.arrow = '#FFFFFF'
    
# Render Graph    
from pyrrd.graph import Graph
graphfile = "/tmp/rrdgraph.png"
g = Graph(graphfile, start=920805000, end=920810000, vertical_label='km/h', color=ca)
g.data.extend([def1, cdef1, cdef2, cdef3, vdef1, vdef2, line1, area1, area2, line2, gprint1])
g.write()
    
# There?    
os.path.isfile(graphfile)

    
# Cleanup
# os.unlink(filename)
# os.unlink(graphfile)




'''
`/usr/local/rrdtool-1.0.48/bin/rrdtool update ${PATH}/temptrax.rrd 
 "N:$TEMPS[0]:$TEMPS[1]:$TEMPS[2]:$TEMPS[3]"`;



  my $rrd_file = "$self->{opts}->{rrd_root}/$data->{c}.rrd";                            
                                                                                        
  unless (-f $rrd_file){                                                                
                                                                                        
    my $command = "$self->{opts}->{rrdtool} create $rrd_file ";                         
    $command .= " --step 10 ";                                                          
    $command .= " --start 1211478990 ";                                                 
    $command .= " DS:q1:GAUGE:600:0:U ";                                                
    $command .= " DS:q2:GAUGE:600:0:U ";                                                
    $command .= " DS:q3:GAUGE:600:0:U ";                                                
    $command .= " DS:lo:GAUGE:600:0:U ";                                                
    $command .= " DS:hi:GAUGE:600:0:U ";                                                
    $command .= " DS:total:GAUGE:600:0:U ";                                             
    $command .= " RRA:AVERAGE:0.5:1:8640 ";   # 24 hours at 1 sample per 10 secs        
    $command .= " RRA:AVERAGE:0.5:90:2880 ";  # 1 month at 1 sample per 15 mins         
    $command .= " RRA:AVERAGE:0.5:2880:5475 ";  # 5 years at 1 sample per 8 hours       
                                                                                        
    print "creating $rrd_file...";                                                      
    print `$command`;                                                                   
    print "done\n";                                                                     
  }
'''
