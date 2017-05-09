#!/usr/bin/python
# coding=utf-8

import sys
from simso.core import Model,ProcEvent
from simso.configuration import Configuration

#from core import ProcEvent


def main(argv):
    if len(argv) == 1:
        # Configuration set up.
        configuration = Configuration(argv[0])
    else:
        # Configuration set up :
        configuration = Configuration()

        configuration.duration = 50 * configuration.cycles_per_ms
        
        # Add the number of cores.
        configuration.add_processor(name="Core 1", identifier=1)
        configuration.add_processor(name="Core 2", identifier=2)

        # Add tasks to the configuration.
        # Adding Periodic tasks to the configuration
        configuration.add_task(name="T0", identifier=1,task_type='Periodic', period=6,
                               activation_date=0, wcet=3, deadline=6)
        configuration.add_task(name="T1", identifier=2,task_type='Periodic', period=8,
                               activation_date=0, wcet=3, deadline=8)
        configuration.add_task(name="T2", identifier=3, period=7, task_type='Periodic',
                               activation_date=0, wcet=5, deadline=7)
        configuration.add_task(name="T3", identifier=4,task_type='Periodic', period=10,
                               activation_date=0, wcet=3, deadline=10)
        configuration.add_task(name="T4", identifier=5,task_type='Periodic', period=9,
                               activation_date=0, wcet=3, deadline=9)
        configuration.add_task(name="T5", identifier=6, period=11, task_type='Periodic',
                               activation_date=0, wcet=5, deadline=11)

        # Utilization calculation 2.677
        U = ((3/6)+(3/8)+(5/7)+(3/10)+(3/9)+(5/11))
#        Adding Aperiodic tasks to the configuration      
#        Finding the virtual deadline for aperiodic tasks
        A6_deadline = 1+(2/U)
        configuration.add_task(name="A6",identifier=7,task_type='Sporadic',list_activation_dates=[1],wcet=2, deadline=A6_deadline)
        A7_deadline = max(A6_deadline,4)+(1/U)
        configuration.add_task(name="A7", identifier=8,task_type='Sporadic', list_activation_dates=[4],wcet=1,deadline=A7_deadline)
        A8_deadline = max(A7_deadline,6)+(5/U)       
        configuration.add_task(name="A8", identifier=9,task_type='Sporadic',list_activation_dates=[6],wcet=5,deadline=A8_deadline)
        A9_deadline = max(A8_deadline,8)+(3/U)       
        configuration.add_task(name="A9", identifier=10,task_type='Sporadic',list_activation_dates=[8],wcet=3,deadline=A9_deadline)
        A10_deadline = max(A9_deadline,10)+(2/U)       
        configuration.add_task(name="A10", identifier=11,task_type='Sporadic',list_activation_dates=[10],wcet=2,deadline=A10_deadline)

        configuration.scheduler_info.set_name("schedulers/SchedulingAlgorithm.py")

    # Vérification of the configuration.
    configuration.check_all()

    # Initialisation of the configuration.
    model = Model(configuration)
    # Execute the simulation.
    model.run_model()

#     Printing the results.
    for log in model.logs:
        print(log)

    # 

    print("Job computation times")
    for task in model.task_list:
        print(task.name + ":")
        for job in task.jobs:
            print(job.name +' '+str(job.computation_time)+' '+str(job.activation_date))
           # print("%s %.3f ms" % (job.name, job.computation_time))

    # Nombre de préemptions par task
#    print("Preemption counts:")
#    for task in model.task_list:
#        print("%s %d" % (task.name, sum([job.preemption_count for job in task.jobs])))
#
    cxt = 0
    for processor in model.processors:
        prev = None
        for evt in processor.monitor:
            if evt[1].event == ProcEvent.RUN:
                if prev is not None and prev != evt[1].args.name:
                    cxt += 1
                prev = evt[1].args.name
    print("Number of context switches (without counting the OS): " + str(cxt))

if __name__ == "__main__":
    main(sys.argv[1:])
