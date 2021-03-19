import vtk

# define coordinates of vertices
points = vtk.vtkPoints()
for z in (-0.5,0.5):
        for x, y in zip((-0.5,-0.5,0.5,0.5),(-0.5,0.5,0.5,-0.5)):
            points.InsertNextPoint(x, y, z)

scalars = vtk.vtkFloatArray()
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(8)
for i in range(8):
    scalars.SetTuple1(i, 1.0*i/8)

# define cell array
lines = vtk.vtkCellArray()            
for i in range(4):
    lines.InsertCellPoint(4)
    lines.InsertNextCell(i)
    lines.InsertNextCell((i+1)%4)
    lines.InsertNextCell(4+(i+1)%4)
    lines.InsertNextCell(i+4)

# Add vertices and edges to polydata object
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetVerts(lines)
polydata.SetLines(lines)

# Set scalar values for each point
polydata.GetPointData().SetScalars(scalars)

# create mapper and actor for the data
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0,0,0)
actor.GetProperty().SetPointSize(10)

# Set VTK pipeline and render the scene
ren = vtk.vtkRenderer()
ren.AddActor(actor)
ren.SetBackground(1,1,1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

renWin.Render()
iren.Start()
