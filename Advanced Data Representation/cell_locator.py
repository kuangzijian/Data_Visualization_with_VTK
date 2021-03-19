import vtk


def slider_callback(obj, evt):
    global cellLocator, polydata, renderer
    level = vtk.vtkMath.Round(obj.GetRepresentation().GetValue())
    cellLocator.GenerateRepresentation(level, polydata)
    renderer.Render()

# Read data
reader = vtk.vtkBYUReader()
reader.SetGeometryFileName("cow.g")
reader.Update()


pointsMapper = vtk.vtkPolyDataMapper()
pointsMapper.SetInputConnection(reader.GetOutputPort())

pointsActor = vtk.vtkActor()
pointsActor.SetMapper(pointsMapper)
pointsActor.GetProperty().SetInterpolationToFlat()

# Create tree
cellLocator = vtk.vtkCellLocator()
cellLocator.SetDataSet(reader.GetOutput())
cellLocator.BuildLocator()

# Initialize representation
polydata = vtk.vtkPolyData()
cellLocator.GenerateRepresentation(0, polydata)

locatorTreeMapper = vtk.vtkPolyDataMapper()
locatorTreeMapper.SetInputData(polydata)

locatorTreeActor = vtk.vtkActor()
locatorTreeActor.SetMapper(locatorTreeMapper)
locatorTreeActor.GetProperty().SetInterpolationToFlat()
locatorTreeActor.GetProperty().SetRepresentationToWireframe()
locatorTreeActor.GetProperty().SetColor(0.2, 0.4, 0.8)


renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Add actors
renderer.AddActor(pointsActor)
renderer.AddActor(locatorTreeActor)

# Render the scene
renderWindow.Render()

# Add slider
sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.SetMinimumValue(0)
sliderRep.SetMaximumValue(cellLocator.GetLevel())
sliderRep.SetValue(0)
sliderRep.SetTitleText("MaxPointsPerRegion")
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.2, 0.2)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(0.8, 0.2)
sliderRep.SetSliderLength(0.075)
sliderRep.SetSliderWidth(0.05)
sliderRep.SetEndCapLength(0.05)

sliderWidget = vtk.vtkSliderWidget()
sliderWidget.SetInteractor(renderWindowInteractor)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.SetAnimationModeToAnimate()
sliderWidget.EnabledOn()

# Add slider callback
sliderWidget.AddObserver("InteractionEvent", slider_callback)

renderWindowInteractor.Initialize()
renderWindow.Render()

renderWindowInteractor.Start()