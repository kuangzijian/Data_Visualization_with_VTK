# Example from 2017 Jan 12nd class

import vtk

cube = vtk.vtkCubeSource() 

cone = vtk.vtkConeSource()
cone.SetResolution(200)

cubeMapper = vtk.vtkPolyDataMapper()
cubeMapper.SetInputConnection(cube.GetOutputPort())

cubeActor = vtk.vtkActor()
cubeActor.SetMapper(cubeMapper)
cubeActor.GetProperty().SetColor(1,0,0)

coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone.GetOutputPort())

coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)

transform = vtk.vtkTransform()
transform.Translate(1, 1, 1)

coneActor.SetUserTransform(transform)

ren1 = vtk.vtkRenderer()
ren1.SetViewport(0, 0, 0.5, 1)
ren1.AddActor(cubeActor)
ren1.AddActor(coneActor)


ren2 = vtk.vtkRenderer()
ren2.SetViewport(0.5, 0, 1.0, 1.0)
ren2.AddActor(cubeActor)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(600, 300)

renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.Render()


iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()
iren.Start()

print ren1.GetActiveCamera()