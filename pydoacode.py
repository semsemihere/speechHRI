# pydoa.py
# pydoa (for visualization) practice 

from DoaProcessor import DoaProcessor

d = DoaProcessor('pydoa/samples/sample.csv', 4)
d.getGroups()
d.getPeakDegree(sigma=3,group='group-1')

# d.plotDegreeDistribution(group='group-1')

