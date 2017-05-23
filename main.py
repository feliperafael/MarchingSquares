import numpy
from vtk import vtkStructuredPointsReader
from vtk.util import numpy_support as VN

filename = "input/ugridex.vtk"

reader = vtkStructuredPointsReader()
reader.SetFileName(filename)
print reader
