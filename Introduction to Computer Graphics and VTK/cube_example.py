import vtk

reader = vtk.vtkSTLReader()
reader.SetFileName("teapot.stl")

# arrow = vtk.vtkArrowSource()
# arrow.SetTipResolution(60)
# arrow.SetShaftResolution(60)

mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()
ren = vtk.vtkRenderer()

mapper.SetInputConnection(reader.GetOutputPort())
# mapper.SetInputConnection(arrow.GetOutputPort())
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1,1,0)


ren.AddActor(actor)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 800)

renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballActor())

iren.SetRenderWindow(renWin)

renWin.Render()
iren.Initialize()
iren.Start()