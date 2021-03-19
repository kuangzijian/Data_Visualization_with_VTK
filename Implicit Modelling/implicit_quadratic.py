import vtk
 
quadric = vtk.vtkQuadric()
quadric.SetCoefficients(.5, 1, .2, 0, .1, 0, 0, .2, 0, 0)
 
sample = vtk.vtkSampleFunction()
sample.SetImplicitFunction(quadric)
sample.SetModelBounds(-.5, .5, -.5, .5, -.5, .5)
sample.SetSampleDimensions(40, 40, 40)
sample.ComputeNormalsOff()
 
# contour
surface = vtk.vtkContourFilter()
surface.SetInputConnection(sample.GetOutputPort())
surface.SetValue(0, 0.0)
 
# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(.2, .2, .5)
 
renderer = vtk.vtkRenderer()
 
# add the actor
renderer.AddActor(actor)
 
# render window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
 
# An interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)
 
# Start
interactor.Initialize()
interactor.Start()
