import vtk

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("teapot.stl")
reader.Update()

# Compute normals
teanormals = vtk.vtkPolyDataNormals()
teanormals.SetInputConnection(reader.GetOutputPort())

# Set actor and mapper
mapper = [vtk.vtkPolyDataMapper() for i in range(3)]
actor = [vtk.vtkActor() for i in range(3)]
for i in range(3):
    mapper[i].SetInputConnection(teanormals.GetOutputPort())
    actor[i].SetMapper(mapper[i])

    # Set actor properties
    prop = actor[i].GetProperty()
    prop.SetColor(1,0,0)
    prop.SetAmbient(0.2)
    prop.SetDiffuse(0.3)
    prop.SetSpecular(0.8)
    prop.SetSpecularPower(40.0)
    if i == 0:
        prop.SetInterpolationToFlat()
    elif i == 1:
        prop.SetInterpolationToGouraud()
    else:
        prop.SetInterpolationToPhong()
        
    # actor.GetProperty().SetRepresentationToWireframe()
    prop.ShadingOn()

# Set render window
renWin = vtk.vtkRenderWindow()
renWin.SetSize(900, 300)

# Set renderer
ren = [vtk.vtkRenderer() for i in range(3)]
for i in range(3):
    ren[i].AddActor(actor[i])

    # Add light
    lightkit = vtk.vtkLightKit()
    lightkit.AddLightsToRenderer(ren[i])

    ren[i].SetViewport(i/3, 0, (i+1)/3, 1)
    renWin.AddRenderer(ren[i])

# Set interactor, render loop
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.Render()
iren.Start()