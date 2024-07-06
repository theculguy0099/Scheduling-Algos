# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:00:13 2020

@author: Miguel Rizzo
"""

##single server 

#Importing Libraries
import pandas as pd ,seaborn as sns, numpy as np ,matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# set seed for reproducibility
np.random.seed(0)

#Single server, single queue simulation
l = 5 # average number of arrivals per minute
µ =10 # average number of people served per minute
ncust =100# number of customers
c=1 # number of servers
utilization={}
service_times = [] # list of service times once they reach the front
queue = []
currtime = 0
resp_fifo = []
resp_lifo = []
resp_lifo_pr = []
resp_rr = [0 for i in range(ncust)]

 #generating inter arrival times using exponential distribution
while c<=1:
    if c==1:
        inter_arrival_times = list(np.random.exponential(scale=1/l,size=ncust))
    
    arrival_times= []# list of arrival times of a person joining the queue
    finish_times = [] # list of finish times after waiting and being served
        
    arrival_times = [0 for i in range(ncust)]
    finish_times = [0 for i in range(ncust)]
        
    arrival_times[0]=round(inter_arrival_times[0],4)#arrival of first customer
        
        #Generate arrival times
      
    for i in range(1,ncust):
        arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),4)
        
            
        # Generate random service times for each customer 
    if c==1:
        service_times = list(np.random.exponential(scale=1/µ,size=ncust))
    
    
    # #Generate finish times
    finish_times[0]= round((arrival_times[0]+service_times[0]),4)
    for i in range(1,ncust):
        previous_finish=finish_times[:i]
        previous_finish.sort(reverse=True)
        previous_finish=previous_finish[:c]
        # if i< c:
        #     finish_times[i] = round(arrival_times[i] + service_times[i],4)
        # else:
        finish_times[i]=round((max(arrival_times[i],min(previous_finish))+service_times[i]),4)

        
    
           # Total time spent in the system by each customer
    total_times =[abs(round((finish_times[i]-arrival_times[i]),4)) for i in range(ncust)]
    
    
    
         # Time spent@waiting before being served (time spent in the queue)
    wait_times = [abs(round((total_times[i] - service_times[i]),4)) for i in range(ncust)]
    resp_fifo=wait_times
    # print(resp_fifo) 
    
        #creating a dataframe with all the data of the model
    data = pd.DataFrame(list(zip(arrival_times,finish_times,service_times,total_times,wait_times,inter_arrival_times)), 
                   columns =['arrival_times','finish_times', 'service_times','total_times','wait_times','inter_arrival_times']) 
    
    #generating the timeline , and their description (arrivals, departures)
    
    tbe=list([0])
    timeline=['simulation starts']
    for i in range(0,ncust):
        tbe.append(data['arrival_times'][i])
        tbe.append(data['finish_times'][i])
        timeline.append('customer ' +str(i+1)+' arrived')
        timeline.append('customer ' +str(i+1)+' left')
        
    
    #generating a dataframe with the timeline and description of events
    
    timeline = pd.DataFrame(list(zip(tbe,timeline)), 
                   columns =['time','Timeline']).sort_values(by='time').reset_index()
    timeline=timeline.drop(columns='index')
    
    #generating the number of customers inside the system at any given time of the simulation
    # and recording idle and working times
    
    timeline['n']=0
    x=0
    for i in range(1,(2*ncust)-1):
        if len(((timeline.Timeline[i]).split()))>2:
            z=str(timeline['Timeline'][i]).split()[2]
        else:
            continue
        if z =='arrived':
            x = x+1
            timeline['n'][i]=x
        else:
            x=x-1
            if x==-1:
                x=0
            timeline['n'][i]=x
        
    
    
    #computing time between events
    t= list()
    for i in timeline.index:
       if i == (2*ncust) -2 :
           continue
       if i < 2*ncust:
           x=timeline.time[i+1]
       else:
           x=timeline.time[i]
       y=timeline.time[i]
       t.append(round((x-y),4))
    
    t.append(0) 
    timeline['tbe']=t
    
    #computing the probability of 'n' customers being in the system
    
    Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)
    Tn=timeline.groupby('n').tbe.agg('count')
    
      
    #checking central tendency measures and dispersion of the data
    timeline.n.describe()
    
    
    #computing expected number of customers in the system
    Ls=(sum(Pn*Pn.index))
    
    
    #computing expected customers waiting in line
    Lq=sum((Pn.index[c+1:]-1)*(Pn[c+1:]))
    
    #plots
    
    
    # plt.figure(figsize=(12,4))
    # sns.lineplot(x=data.index,y=wait_times,color='black').set(xticklabels=[])
    # plt.xlabel('Customer number')
    # plt.ylabel('minutes')
    # plt.title('Wait time of customers with '+str(c)+ ' servers')
    # sns.despine()
    # plt.show()
    
    # if c==1:
    #     plt.figure(figsize=(7,7))
    #     sns.distplot(inter_arrival_times,kde=False,color='r')
    #     plt.title('Time between Arrivals')
    #     plt.xlabel('Minutes')
    #     plt.ylabel('Frequency')
    #     sns.despine()
    #     plt.show()
        
    #     plt.figure(figsize=(8,8))
    #     sns.distplot(service_times,kde=False)
    #     plt.title('Service Times')
    #     plt.xlabel('Minutes')
    #     plt.ylabel('Frequency')
    #     sns.despine()
    #     plt.show()
    
    # plt.figure(figsize=(8,8))
    # sns.barplot(x=Pn.index,y=Pn,color='g')
    # plt.title('Probability of n customers in the system with '+str(c)+ ' servers')
    # plt.xlabel('number of customers')
    # plt.ylabel('Probability')
    # sns.despine()
    # plt.show()
    
    ############################
    '''plt.figure(figsize=(7,7))
    sns.barplot(['Idle','Occupied'],[Pn[0],1-Pn[0]],color='mediumpurple')
    plt.title('Utilization %')
    plt.xlabel('System state')
    plt.ylabel('Probability')
    sns.despine()
    plt.show()'''
    ##########################
    utilization.setdefault(c,(Ls-Lq)/c)
    
    
    print('Output:','\n',
          'Servers : '+str(c),'\n '
          'Time Between Arrivals : ',str(data.inter_arrival_times.mean()),'\n',
          'Service Time: (1/µ)',str(data.service_times.mean()),'\n'
          ' Utilization (c): ',str((Ls-Lq)/c),'\n',
          'Expected wait time in line (Wq):',str(data['wait_times'].mean()),'\n',
          'Expected time spent on the system (Ws):',str(data.total_times.mean()),'\n',
          'Expected number of customers in line (Lq):',str(Lq),'\n',
          'Expected number of occupied servers :',str(Ls-Lq),'\n')
    
    c=c+1
    
utilization=pd.Series(utilization) 
# plt.figure(figsize=(6,6))  
# sns.pointplot(x=utilization.index,y=utilization)
# plt.xlabel('Number of servers')
# plt.ylabel('Utilization')
# plt.title('number of servers vs Utilization')
counter=[]

mx=0
for i in range(0,ncust):
    if finish_times[i]>mx:
        mx=int(finish_times[i])
print(mx)
# counter
for i in range(mx):
    counter.append(0)
for time in range(mx):
    count = 0 
    for i in range(0,ncust):
        if finish_times[i]-service_times[i]>=time and arrival_times[i]<=time:
            # print('The last customer left the system at:',time)
            count+=1
    counter[time] = count

slowdown=[]

for i in range(ncust):
    slowdown.append(total_times[i]/service_times[i])

print("Average Service Time ",slowdown)
slowdown=np.array(slowdown)
print("Average Slow Down Time",slowdown.mean())


# plt.plot(range(len(slowdown)), slowdown)
# plt.xlabel('Time')
# plt.ylabel('Number of Jobs')
# plt.title('Slow Down Time')
# plt.show()





# plt.plot(range(mx), counter)
# plt.xlabel('Time')
# plt.ylabel('Number of Customers')
# plt.title('Number of Customers vs Time')
# plt.show()
# counter = np.array(counter)
# print('The average number of customers in the system is:', counter.mean())




# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:00:13 2020

@author: Miguel Rizzo
"""

##single server 

#Importing Libraries
import pandas as pd ,seaborn as sns, numpy as np ,matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# set seed for reproducibility
np.random.seed(0)


#Single server, single queue simulation
l = 5 # average number of arrivals per minute
µ =10 # average number of people served per minute
ncust =100# number of customers
c=1 # number of servers
utilization={}
service_times = [] # list of service times once they reach the front

 #generating inter arrival times using exponential distribution
while c<=1:
    if c==1:
        inter_arrival_times = list(np.random.exponential(scale=1/l,size=ncust))
    
    arrival_times= []# list of arrival times of a person joining the queue
    finish_times = [] # list of finish times after waiting and being served
        
    arrival_times = [0 for i in range(ncust)]
    finish_times = [0 for i in range(ncust)]
        
    arrival_times[0]=round(inter_arrival_times[0],4)#arrival of first customer
        
        #Generate arrival times
      
    for i in range(1,ncust):
        arrival_times[i]=round((arrival_times[i-1]+inter_arrival_times[i]),4)
    arrival_times2=arrival_times.copy()
            
        # Generate random service times for each customer 
    if c==1:
        service_times = list(np.random.exponential(scale=1/µ,size=ncust))
    
    service_times2=service_times.copy()
    #Generate finish times
    finish_times[0]= round((arrival_times[0]+service_times[0]),4)
    # for i in range(1,ncust):
    #     previous_finish=finish_times[:i]
    #     previous_finish.sort(reverse=True)
    #     previous_finish=previous_finish[:c]
    #     # if i< c:
    #     #     finish_times[i] = round(arrival_times[i] + service_times[i],4)
    #     # else:
    #     finish_times[i]=round((max(arrival_times[i],(previous_finish))+service_times[i]),4)
    currtime=finish_times[0]

    for i in range(1,ncust):

        # to find new process to be schedule
        newprocess=-1
        for j in range(ncust):
            if finish_times[j] == 0:
                if arrival_times[j] > currtime:
                    break
                else:
                    newprocess=j
                pass
        if newprocess==-1:
            for j in range(ncust):
                if finish_times[j] ==0:
                    newprocess=j
                    break   
        finish_times[newprocess]=max(currtime,arrival_times[newprocess])+service_times[newprocess]
        currtime=finish_times[newprocess]
    
           # Total time spent in the system by each customer
    total_times =[abs(round((finish_times[i]-arrival_times[i]),4)) for i in range(ncust)]
    
    
    
         # Time spent@waiting before being served (time spent in the queue)
    wait_times = [abs(round((total_times[i] - service_times[i]),4)) for i in range(ncust)]
    resp_lifo=wait_times
    
        #creating a dataframe with all the data of the model
    data = pd.DataFrame(list(zip(arrival_times,finish_times,service_times,total_times,wait_times,inter_arrival_times)), 
                   columns =['arrival_times','finish_times', 'service_times','total_times','wait_times','inter_arrival_times']) 
    
    #generating the timeline , and their description (arrivals, departures)
    
    tbe=list([0])
    timeline=['simulation starts']
    for i in range(0,ncust):
        tbe.append(data['arrival_times'][i])
        tbe.append(data['finish_times'][i])
        timeline.append('customer ' +str(i+1)+' arrived')
        timeline.append('customer ' +str(i+1)+' left')
        
    
    #generating a dataframe with the timeline and description of events
    
    timeline = pd.DataFrame(list(zip(tbe,timeline)), 
                   columns =['time','Timeline']).sort_values(by='time').reset_index()
    timeline=timeline.drop(columns='index')
    
    #generating the number of customers inside the system at any given time of the simulation
    # and recording idle and working times
    
    timeline['n']=0
    x=0
    for i in range(1,(2*ncust)-1):
        if len(((timeline.Timeline[i]).split()))>2:
            z=str(timeline['Timeline'][i]).split()[2]
        else:
            continue
        if z =='arrived':
            x = x+1
            timeline['n'][i]=x
        else:
            x=x-1
            if x==-1:
                x=0
            timeline['n'][i]=x
        
    
    
    #computing time between events
    t= list()
    for i in timeline.index:
       if i == (2*ncust) -2 :
           continue
       if i < 2*ncust:
           x=timeline.time[i+1]
       else:
           x=timeline.time[i]
       y=timeline.time[i]
       t.append(round((x-y),4))
    
    t.append(0) 
    timeline['tbe']=t
    
    #computing the probability of 'n' customers being in the system
    
    Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)
    Tn=timeline.groupby('n').tbe.agg('count')
    
      
    #checking central tendency measures and dispersion of the data
    timeline.n.describe()
    
    
    #computing expected number of customers in the system
    Ls=(sum(Pn*Pn.index))
    
    
    #computing expected customers waiting in line
    Lq=sum((Pn.index[c+1:]-1)*(Pn[c+1:]))
    
    #plots
    
    
    # plt.figure(figsize=(12,4))
    # sns.lineplot(x=data.index,y=wait_times,color='black').set(xticklabels=[])
    # plt.xlabel('Customer number')
    # plt.ylabel('minutes')
    # plt.title('Wait time of customers with '+str(c)+ ' servers')
    # sns.despine()
    # plt.show()
    
    # if c==1:
        # plt.figure(figsize=(7,7))
        # sns.distplot(inter_arrival_times,kde=False,color='r')
        # plt.title('Time between Arrivals')
        # plt.xlabel('Minutes')
        # plt.ylabel('Frequency')
        # sns.despine()
        # plt.show()
        
        # plt.figure(figsize=(8,8))
        # sns.distplot(service_times,kde=False)
        # plt.title('Service Times')
        # plt.xlabel('Minutes')
        # plt.ylabel('Frequency')
        # sns.despine()
        # plt.show()
    
    # plt.figure(figsize=(8,8))
    # sns.barplot(x=Pn.index,y=Pn,color='g')
    # plt.title('Probability of n customers in the system with '+str(c)+ ' servers')
    # plt.xlabel('number of customers')
    # plt.ylabel('Probability')
    # sns.despine()
    # plt.show()
    
    ############################
    ''' plt.figure(figsize=(7,7))
    sns.barplot(['Idle','Occupied'],[Pn[0],1-Pn[0]],color='mediumpurple')
    plt.title('Utilization %')
    plt.xlabel('System state')
    plt.ylabel('Probability')
    sns.despine()
    plt.show() '''
    ##########################
    utilization.setdefault(c,(Ls-Lq)/c)
    
    
    print('Output:','\n',
          'Servers : '+str(c),'\n '
          'Time Between Arrivals : ',str(data.inter_arrival_times.mean()),'\n',
          'Service Time: (1/µ)',str(data.service_times.mean()),'\n'
          ' Utilization (c): ',str((Ls-Lq)/c),'\n',
          'Expected wait time in line (Wq):',str(data['wait_times'].mean()),'\n',
          'Expected time spent on the system (Ws):',str(data.total_times.mean()),'\n',
          'Expected number of customers in line (Lq):',str(Lq),'\n',
          'Expected number of occupied servers :',str(Ls-Lq),'\n')
    
    c=c+1
    
utilization=pd.Series(utilization) 
# plt.figure(figsize=(6,6))  
# sns.pointplot(x=utilization.index,y=utilization)
# plt.xlabel('Number of servers')
# plt.ylabel('Utilization')
# plt.title('number of servers vs Utilization')


counter = []

slowdown=[]

for i in range(ncust):
    slowdown.append(total_times[i]/service_times2[i])

print("Average Service Time ",slowdown)
slowdown=np.array(slowdown)
print("Average Slow Down Time",slowdown.mean())


# plt.plot(range(len(slowdown)), slowdown)
# plt.xlabel('Time')
# plt.ylabel('Number of Jobs')
# plt.title('Slow Down Time')
# plt.show()

# mx = 0
# for i in range(0, ncust):
#     if finish_times[i] > mx:
#         mx = int(finish_times[i])
# print(mx)
# # counter
# for i in range(mx):
#     counter.append(0)
# for time in range(mx):
#     count = 0
#     for i in range(0, ncust):
#         if finish_times[i]-service_times2[i] >= time and arrival_times2[i] <= time:
#             # print('The last customer left the system at:',time)
#             count += 1
#     counter[time] = count

# print(counter)
# # exit(0)
# plt.plot(range(mx), counter)
# plt.xlabel('Time')
# plt.ylabel('Number of Customers')
# plt.title('Number of Customers vs Time')
# plt.show()
# counter = np.array(counter)
# print('The average number of customers in the system is:', counter.mean())


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns




time_quantum = 0.1
ncust = 100
max_queue_size = 10
service_times = []
µ = 10
l = 5
c=1
response=[]
for i in range(ncust):
    response.append(-1)

inter_arrival_times = list(np.random.exponential(scale=1/l, size=ncust))

arrival_times = [0 for i in range(ncust)]
finish_times = [0 for i in range(ncust)]

# arrival of first customer
arrival_times[0] = round(inter_arrival_times[0], 4)

# Generate arrival times

for i in range(1, ncust):
    arrival_times[i] = round((arrival_times[i-1]+inter_arrival_times[i]), 4)
arrival_times2 = arrival_times.copy()

# Generate random service times for each customer
service_times = list(np.random.exponential(scale=1/µ, size=ncust))
service_times2 = service_times.copy()



# now we have inter arrival times and service times for each customer

print(arrival_times)
print(service_times)
queue = []
currtime = 0
utilization={}

while 1:
    for i in range(ncust):
        if arrival_times[i] <= currtime:
            queue.append(i)
            arrival_times[i] = 1e18

    if len(queue) == 0:
        f = 0
        for i in range(ncust):
            if arrival_times[i] != 1e18:
                queue.append(i)
                f = 1
                currtime = arrival_times[i]
                arrival_times[i] = 1e18
                break
        if f == 0:
            break

    if currtime >= 1e18:
        break

    index = queue[0]
    queue = queue[1:]
    if response[index] == -1:
        response[index] = currtime-arrival_times2[index]

    if service_times[index] <= time_quantum:
        resp_rr[index]=currtime-arrival_times2[index]
        currtime += service_times[index]
        service_times[index] = 0
        finish_times[index] = currtime

    else:
        currtime += time_quantum
        service_times[index] -= time_quantum
        queue.append(index)
    # print(currtime)
    # print(queue)
    # print(service_times)

# print(finish_times)
# print(arrival_times2)

total_times =[abs(round((finish_times[i]-arrival_times2[i]),4)) for i in range(ncust)]

print(total_times)

    # Time spent@waiting before being served (time spent in the queue)
wait_times = [abs(round((total_times[i] - service_times2[i]),4)) for i in range(ncust)]

print(wait_times)

    #creating a dataframe with all the data of the model
data = pd.DataFrame(list(zip(arrival_times2,finish_times,service_times2,total_times,wait_times,inter_arrival_times)), 
                columns =['arrival_times','finish_times', 'service_times','total_times','wait_times','inter_arrival_times']) 



#generating the timeline , and their description (arrivals, departures)

tbe=list([0])
timeline=['simulation starts']
for i in range(0,ncust):
    tbe.append(data['arrival_times'][i])
    tbe.append(data['finish_times'][i])
    timeline.append('customer ' +str(i+1)+' arrived')
    timeline.append('customer ' +str(i+1)+' left')
    

#generating a dataframe with the timeline and description of events

timeline = pd.DataFrame(list(zip(tbe,timeline)), 
                columns =['time','Timeline']).sort_values(by='time').reset_index()
timeline=timeline.drop(columns='index')

#generating the number of customers inside the system at any given time of the simulation
# and recording idle and working times

timeline['n']=0
x=0
for i in range(1,(2*ncust)-1):
    if len(((timeline.Timeline[i]).split()))>2:
        z=str(timeline['Timeline'][i]).split()[2]
    else:
        continue
    if z =='arrived':
        x = x+1
        timeline['n'][i]=x
    else:
        x=x-1
        if x==-1:
            x=0
        timeline['n'][i]=x
    


#computing time between events
t= list()
for i in timeline.index:
    if i == (2*ncust) -2 :
        continue
    if i < 2*ncust:
        x=timeline.time[i+1]
    else:
        x=timeline.time[i]
    y=timeline.time[i]
    t.append(round((x-y),4))

t.append(0) 
timeline['tbe']=t

#computing the probability of 'n' customers being in the system

Pn=timeline.groupby('n').tbe.agg(sum)/sum(t)
Tn=timeline.groupby('n').tbe.agg('count')

    
#checking central tendency measures and dispersion of the data
timeline.n.describe()


#computing expected number of customers in the system
Ls=(sum(Pn*Pn.index))


#computing expected customers waiting in line
Lq=sum((Pn.index[c+1:]-1)*(Pn[c+1:]))

#plots


# plt.figure(figsize=(12,4))
# sns.lineplot(x=data.index,y=wait_times,color='black').set(xticklabels=[])
# plt.xlabel('Customer number')
# plt.ylabel('minutes')
# plt.title('Wait time of customers with '+str(c)+ ' servers')
# sns.despine()
# plt.show()

# if c==1:
#     plt.figure(figsize=(7,7))
#     sns.distplot(inter_arrival_times,kde=False,color='r')
#     plt.title('Time between Arrivals')
#     plt.xlabel('Minutes')
#     plt.ylabel('Frequency')
#     sns.despine()
#     plt.show()
    
#     plt.figure(figsize=(8,8))
#     sns.distplot(service_times2,kde=False)
#     plt.title('Service Times')
#     plt.xlabel('Minutes')
#     plt.ylabel('Frequency')
#     sns.despine()
#     plt.show()

# plt.figure(figsize=(8,8))
# sns.barplot(x=Pn.index,y=Pn,color='g')
# plt.title('Probability of n customers in the system with '+str(c)+ ' servers')
# plt.xlabel('number of customers')
# plt.ylabel('Probability')
# sns.despine()
# plt.show()

############################
'''plt.figure(figsize=(7,7))
sns.barplot(['Idle','Occupied'],[Pn[0],1-Pn[0]],color='mediumpurple')
plt.title('Utilization %')
plt.xlabel('System state')
plt.ylabel('Probability')
sns.despine()
plt.show()'''
##########################
utilization.setdefault(c,(Ls-Lq)/c)


print('Output:','\n',
        'Servers : '+str(c),'\n '
        'Time Between Arrivals : ',str(data.inter_arrival_times.mean()),'\n',
        'Service Time: (1/µ)',str(data.service_times.mean()),'\n'
        ' Utilization (c): ',str((Ls-Lq)/c),'\n',
        'Expected wait time in line (Wq):',str(data['wait_times'].mean()),'\n',
        'Expected time spent on the system (Ws):',str(data.total_times.mean()),'\n',
        'Expected number of customers in line (Lq):',str(Lq),'\n',
        'Expected number of occupied servers :',str(Ls-Lq),'\n')

c=c+1

utilization=pd.Series(utilization) 
# plt.figure(figsize=(6,6))  
# sns.pointplot(x=utilization.index,y=utilization)
# plt.xlabel('Number of servers')
# plt.ylabel('Utilization')
# plt.title('number of servers vs Utilization')
counter=[]

slowdown=[]

for i in range(ncust):
    slowdown.append(total_times[i]/service_times2[i])

print("Average Service Time ",slowdown)
slowdown=np.array(slowdown)
print("Average Slow Down Time",slowdown.mean())



# plt.plot(range(len(slowdown)), slowdown)
# plt.xlabel('Time')
# plt.ylabel('Number of Jobs')
# plt.title('Slow Down Time')
# plt.show()



zeros=[0 for i in range(ncust)]
pro_index=[i for i in range(1,ncust+1)]
plt.plot(pro_index, resp_fifo, label='FIFO')
plt.plot(pro_index, resp_lifo, label='LIFO')
plt.plot(pro_index, zeros, label='LIFO_PR')
plt.plot(pro_index,response, label='RR')

plt.xlabel('List 3')
plt.ylabel('Values')
plt.title('Plot of List 1 and List 2 vs List 3')

# Adding legend
plt.legend()

# Displaying the plot
plt.show()


