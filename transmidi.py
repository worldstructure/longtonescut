import midi
import re
import os
import sys
from numpy import *
os.chdir(sys.path[0])
pa=midi.read_midifile('0.mid')
matrix0=re.findall(r"NoteOnEvent[(]tick=(\d+), channel=0, data=\[(\d+), (\d+)\][)]",str(pa))
resolution=re.findall(r"resolution=(\d+)",str(pa))
tempo=re.findall(r"SetTempoEvent[(]tick=(\d+), data=\[(\d+), (\d+), (\d+)\][)]",str(pa))
timesign=re.findall(r"midi.TimeSignatureEvent[(]tick=(\d+), data=\[(\d+), (\d+), (\d+), (\d+)\][)]",str(pa))
matrix=mat(matrix0)
m,n=shape(matrix)
matrix=hstack((matrix,mat(zeros((m,1)))))
result=mat(zeros((int(m/2),5)))
matrix=matrix.astype(float)#转换数据类型
result=result.astype(float)
bound=int(resolution[0])*2#长音符阶段值，可适当调整一般*1或*2
while sum(matrix[:,3])!=m:
    start=0
    ending=0
    for i in range(0,m):
        if matrix[i,3]==0:
            start=i
            break
    for i in range(start+1,m):
        if matrix[start,1]==matrix[i,1]:
            ending=i;
            break;
    matrix[start,3]=1
    matrix[ending,3]=1
    ed=int(sum(matrix[:,3])/2)-1
    #print(ed,end=' ')
    #print(sum(matrix[:,3]),end=' ')
    #print(start,ending,end=' ')
    #if ed>922 and ed<925:
    #     print(start,ending,end=' ')
    result[ed,0]=matrix[start,1]
    result[ed,1]=sum(matrix[0:start+1,0])
    result[ed,2]=sum(matrix[0:ending+1,0])
    result[ed,3]=sum(matrix[start+1:ending+1,0])
    result[ed,4]=matrix[start,2]
#print(result[0:5,:])
for i in range(int(m/2)):
    if result[i,3]>bound:
        result[i,3]=bound
        result[i,2]=result[i,1]+bound
preout=mat(zeros((int(m),3)))
preout=preout.astype(float)
for i in range(int(m/2)):
    preout[2*i,0]=result[i,0]
    preout[2*i,1]=result[i,1]
    preout[2*i,2]=result[i,4]
    preout[2*i+1,0]=result[i,0]
    preout[2*i+1,1]=result[i,2]
    preout[2*i+1,2]=0
#print(preout[0:20,:])
preout=preout[lexsort([preout.T[1]])]
#print(preout[:,0:5])
#mj,i,j=shape(preout)
#print(i,j)
#print(resolution,tempo)
pattern=midi.Pattern(format=1,resolution=int(resolution[0]))
track=midi.Track()
pattern.append(track)
track.append(midi.SetTempoEvent(tick=int(tempo[0][0]), data=[int(tempo[0][1]), int(tempo[0][2]), int(tempo[0][3])]))
track.append(midi.TimeSignatureEvent(tick=int(timesign[0][0]), data=[int(timesign[0][1]), int(timesign[0][2]), int(timesign[0][3]), int(timesign[0][4])]))
track.append(midi.NoteOnEvent(tick=int(preout[0,0,1]), channel=0, data=[int(preout[0,0,0]), int(preout[0,0,2])]))
for i in range(m-1):
    track.append(midi.NoteOnEvent(tick=int(preout[0,i+1,1]-preout[0,i,1]), channel=0, data=[int(preout[0,i+1,0]), int(preout[0,i+1,2])]))
track.append(midi.EndOfTrackEvent(tick=1, data=[]))
#print(str(pattern))
midi.write_midifile("out.mid",pattern)

   

