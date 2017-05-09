"""
Partitionned EDF using PartitionedScheduler.
Try to load balance the tasks among the processors.
"""
from simso.core.Scheduler import SchedulerInfo
from EDF_mono import EDF_mono
from simso.utils import PartitionedScheduler


class SchedulingAlgorithm(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(self, SchedulerInfo("EDF_mono", EDF_mono))

    def packer(self):
        # First Fit
        cpus = [[cpu, 0] for cpu in self.processors]
        for task in self.task_list:
            m = cpus[0][1]
            j = 0
            # Find the processor with the lowest load for tasks.
            if('T' in task.name):
                for i, c in enumerate(cpus):
                    if c[1] < m:
                        m = c[1]
                        j = i
            else :
#               Selecting the processor with low virtual deadline for Aperiodic tasks 
                virtualDeadline_core1= task.wcet/cpus[0][1]
                virtualDeadline_core2= task.wcet/cpus[1][1]
                if(virtualDeadline_core1<virtualDeadline_core2):
                    j=0
                else:
                    j=1
            # Affect it to the task.
#            if('A4' in task.name or 'A3' in task.name) :
#                self.affect_task_to_processor(task, cpus[1][0])
#            else :
            self.affect_task_to_processor(task, cpus[j][0])

            # Update utilization.
            cpus[j][1] += float(task.wcet) / task.deadline
        return True
