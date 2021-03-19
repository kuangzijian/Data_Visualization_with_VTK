import vtk

reader = vtk.vtkXMLUnstructuredGridReader()
reader.SetFileName("Disc_BiQuadraticQuads_0_0.vtu")
reader.Update()


# Create line through center
center = reader.GetOutput().GetCenter()
bounds = reader.GetOutput().GetBounds()

startRay = [bounds[0] - center[0], center[1], center[2]]
endRay = [bounds[1] + center[0], center[1], center[2]]

# Initialize cell data colors
cellData = vtk.vtkUnsignedCharArray()
cellData.SetNumberOfComponents(3)
cellData.SetNumberOfTuples(reader.GetOutput().GetNumberOfCells())
reader.GetOutput().GetCellData().SetScalars(cellData)

for i in range(cellData.GetNumberOfTuples()):
    cellData.InsertTuple(i, [227.0, 207.0, 87.0])

# Find line cell intersections
cellIds = vtk.vtkIdList()
locator = vtk.vtkCellLocator()
locator.SetDataSet(reader.GetOutput())
locator.BuildLocator()
locator.FindCellsAlongLine(startRay, endRay, 0.001, cellIds)

for i in range(cellIds.GetNumberOfIds()):
    cellData.InsertTuple(cellIds.GetId(i), [255, 99, 71])

# Shrink cells
shrink = vtk.vtkShrinkFilter()
shrink.SetInputConnection(reader.GetOutputPort())
shrink.SetShrinkFactor(0.95)

# Convert cells to polydata
surface = vtk.vtkDataSetSurfaceFilter()
surface.SetInputConnection(shrink.GetOutputPort())
surface.SetNonlinearSubdivisionLevel(2)
surface.Update()

# Show line
lineSource = vtk.vtkLineSource()
lineSource.SetPoint1(startRay)
lineSource.SetPoint2(endRay)
lineMapper = vtk.vtkPolyDataMapper()
lineMapper.SetInputConnection(lineSource.GetOutputPort())
lineActor = vtk.vtkActor()
lineActor.SetMapper(lineMapper)

# Render results
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUseCellData()

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(lineActor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Camera settings
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()

iren.SetRenderWindow(renWin)
renWin.AddRenderer(renderer)
renWin.SetSize(800, 600)
renWin.Render()

iren.Start()
