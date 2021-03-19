import vtk

'''This example code shows the volume rendering of a DICOM data set with and without shading'''

ddir = r"Head_Neck" # path to the directory that contains the DICOM image sequence

# Loading the DICOM file
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(ddir)
reader.Update()

# Create an opacity function
opacityfunction = vtk.vtkPiecewiseFunction()
opacityfunction.AddPoint(-1024, 0)
opacityfunction.AddPoint(0, 0)
opacityfunction.AddPoint(3071, 1)

# Create a color transfer function
colorfunction = vtk.vtkColorTransferFunction()
colorfunction.AddRGBPoint(-1024, 0, 0, 0)
colorfunction.AddRGBPoint(3071, 1, 1, 1)

# volume mapper for rendering DICOM with no shading
mapper1 = vtk.vtkSmartVolumeMapper()
mapper1.SetInputConnection(reader.GetOutputPort())

# volume mapper for rendering DICOM with shading
mapper2 = vtk.vtkSmartVolumeMapper()
mapper2.SetInputConnection(reader.GetOutputPort())

# define volume property and add color & opacity transfer functions. Turn shading off.
volumeprop1 = vtk.vtkVolumeProperty()
volumeprop1.SetScalarOpacity(opacityfunction)
volumeprop1.SetColor(colorfunction)
volumeprop1.ShadeOff()

# define volume property and add color & opacity transfer functions. Turn shading on.
volumeprop2 = vtk.vtkVolumeProperty()
volumeprop2.SetScalarOpacity(opacityfunction)
volumeprop2.SetColor(colorfunction)
volumeprop2.ShadeOn()

# Create volume actor and set mapper and volume property
volume1 = vtk.vtkVolume()
volume1.SetMapper(mapper1)
volume1.SetProperty(volumeprop1)

# Create volume actor and set mapper and volume property
volume2 = vtk.vtkVolume()
volume2.SetMapper(mapper2)
volume2.SetProperty(volumeprop2)

# create renderers
ren1 = vtk.vtkRenderer()
ren2 = vtk.vtkRenderer()

# Add volumes to the respective renderers
ren1.AddVolume(volume1)
ren2.AddVolume(volume2)

# Create a scene light and add it to the second renderer
light = vtk.vtkLight()
light.SetLightTypeToSceneLight()
light.SetPosition(0.0, 1.0, 0.0)
ren2.AddLight(light)

# Set side-by-side viewports for renderers
ren1.SetViewport(0, 0, 0.5, 1)
ren2.SetViewport(0.5, 0, 1, 1)

# Create the render window and add renderers
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)

# Set display to full screen
renWin.SetFullScreen(1)

# Render scene
renWin.Render()

# Create a render window interactor and set the render window. 
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

# Initialize and run
iren.Initialize()
iren.Start()
