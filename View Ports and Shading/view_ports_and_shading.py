import vtk

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("corner-piece.stl")
reader.Update()
print(reader.GetOutput())
# Compute normals
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# Set actor and mapper
mapper = [vtk.vtkPolyDataMapper() for i in range(4)]
actor = [vtk.vtkActor() for i in range(4)]
for i in range(4):
    mapper[i].SetInputConnection(normals.GetOutputPort())
    actor[i].SetMapper(mapper[i])

    # Set actor properties
    prop = actor[i].GetProperty()
    prop.SetColor(1, 0, 0)
    prop.SetAmbient(0.2)
    prop.SetDiffuse(0.3)
    prop.SetSpecular(0.8)
    prop.SetSpecularPower(40.0)
    if i == 0:
        # view port 1 - Wireframe (No shading or texture)
        prop.SetRepresentationToWireframe()
    elif i == 1:
        # view port 2 - Surface (Gouraud shading)
        prop.SetInterpolationToGouraud()
    elif i == 2:
        # view port 3 - Surface (Flat shading)
        prop.SetInterpolationToFlat()
    else:
        # view port 4 - Surface (Phong shading)
        prop.SetInterpolationToPhong()
    prop.ShadingOn()

# Set render window
renWin = vtk.vtkRenderWindow()
renWin.SetSize(600, 600)

# Set renderer
ren = [vtk.vtkRenderer() for i in range(4)]
for i in range(4):
    ren[i].AddActor(actor[i])

    # Add light
    lightkit = vtk.vtkLightKit()
    lightkit.AddLightsToRenderer(ren[i])

    # Create four view ports
    if i < 2:
        ren[i].SetViewport(i/2, 0.5, (i+1)/2, 1)
    else:
        ren[i].SetViewport((i-2)/2, 0, (i-1)/2, 0.5)
    renWin.AddRenderer(ren[i])

# Set interactor, render loop
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.Render()

# Export the rendered scene to a JPG file
filter = vtk.vtkWindowToImageFilter()
filter.SetInput(renWin)
filter.Update()

writer = vtk.vtkJPEGWriter()
writer.SetInputData(filter.GetOutput())
writer.SetFileName('rendered_scene.jpg')
writer.Write()

iren.Start()



