import vtk

# Read sphere data
reader = vtk.vtkSLCReader()
reader.SetFileName("sphere.slc")

# Set an opacity transfer function for volume rendering
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddSegment(1, 0, 255, 1)

# Set a color transfer function
tfun = vtk.vtkColorTransferFunction()
tfun.AddRGBPoint(0, 0, 0.5, 1)
tfun.AddRGBPoint(255, 0, 0.5, 1)

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(tfun)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()
volumeProperty.SetDiffuse(0.8) # 0.8
volumeProperty.SetAmbient(0.3) # 0.3
volumeProperty.SetSpecular(1.0) # 1.0
volumeProperty.SetSpecularPower(40.0)

volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty (volumeProperty)

# Add sphere to renderer
ren1 = vtk.vtkRenderer()
ren1.AddVolume(volume)

# Create light object
light = vtk.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, 100, 25)
light.SetFocalPoint(0,0,0)
light.SetIntensity(0.8)

# Add the lights to the renderer
ren1.AddLight(light)
ren1.SetBackground(.3,.3,0.3)
 
# Create render window and add renderer
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)

# Set up interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Render the scene
renWin.Render()

# Zoom in to get a bit bigger object
ren1.GetActiveCamera().Zoom(1.5)

iren.Start()

  