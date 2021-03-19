import vtk

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(60)
sphere.SetPhiResolution(60)

mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()

# Compute normals
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(sphere.GetOutputPort())

# VTK pipeline for mapper and actor
mapper.SetInputConnection(normals.GetOutputPort())
actor.SetMapper(mapper)

# Set object properties
prop = actor.GetProperty()
prop.SetInterpolationToFlat() # Set shading to Flat
prop.ShadingOn()
prop.SetColor(1, 1, 0)
prop.SetDiffuse(0.8) # 0.8
prop.SetAmbient(0.3) # 0.3
prop.SetSpecular(1.0) # 1.0
prop.SetSpecularPower(100.0)

# Define light
light = vtk.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, 100, 25)
light.SetFocalPoint(0,0,0)
light.SetIntensity(0.8)

# Add the light to the renderer
ren.AddLight(light)

ren.AddActor(actor)
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
# Define interactor and render the scene
iren.SetRenderWindow(renWin)
renWin.Render()
iren.Initialize()
iren.Start()
