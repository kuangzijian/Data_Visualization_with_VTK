import vtk
from vtk.util.colors import red, turquoise

reader = vtk.vtkPolyDataReader()
reader.SetFileName("hello.vtk")

lineMapper = vtk.vtkPolyDataMapper()
lineMapper.SetInputConnection(reader.GetOutputPort())

lineActor = vtk.vtkActor()
lineActor.SetMapper(lineMapper)
lineActor.GetProperty().SetColor(red)

imp = vtk.vtkImplicitModeller()
imp.SetInputConnection(reader.GetOutputPort())
imp.SetSampleDimensions(110, 40, 20)
imp.SetMaximumDistance(0.25)
imp.SetModelBounds(-1, 10, -1, 3, -1, 1)

contour = vtk.vtkContourFilter()
contour.SetInputConnection(imp.GetOutputPort())
contour.SetValue(0, 0.25)

impMapper = vtk.vtkPolyDataMapper()
impMapper.SetInputConnection(contour.GetOutputPort())
impMapper.ScalarVisibilityOff()

impActor = vtk.vtkActor()
impActor.SetMapper(impMapper)
impActor.GetProperty().SetColor(turquoise)
impActor.GetProperty().SetOpacity(0.5)


ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(lineActor)
ren.AddActor(impActor)

renWin.SetSize(800, 300)
ren.ResetCamera()
ren.GetActiveCamera().Zoom(2.5)


iren.Initialize()
renWin.Render()
iren.Start()
