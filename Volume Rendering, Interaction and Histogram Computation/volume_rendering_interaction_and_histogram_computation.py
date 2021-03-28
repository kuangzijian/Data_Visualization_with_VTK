import vtk

dir_ = r"CT" # Specify the directory which contains the CT image data

# Read CT dataset using vtkDICOMImageReader class
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-78, 0.55, 0.25, 0.15)
colorFunc.AddRGBPoint(96, 0.88, 0.6, 0.29)
colorFunc.AddRGBPoint(180, 1, 0.95, 0.93)
colorFunc.AddRGBPoint(260, 0.64, 0, 0)
colorFunc.AddRGBPoint(3071, 0.84, 0.66, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-78, 0.0)
alphaChannelFunc.AddPoint(96, 0.29)
alphaChannelFunc.AddPoint(180, 0.53)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.89)

# Create an interactable plane widget using vtkImagePlaneWidget class
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(800,800)

# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()  
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)  

# Add the volume to the renderer
ren.AddVolume(volume)

# Render the scene
renWin.Render()
iren.Start()
