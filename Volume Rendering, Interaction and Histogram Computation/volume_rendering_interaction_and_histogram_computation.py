import vtk

# Specify the directory which contains the CT image data
dir_ = r"CT"

# Read CT dataset using vtkDICOMImageReader class
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

# Retrieve CT dataset details
print('Dimension: ' + str(reader.GetOutput().GetDimensions()))
print('Voxel Resolution: ' + str(reader.GetOutput().GetSpacing()))
print('Minimum & Maximum Pixel Intensities: ' + str(reader.GetOutput().GetScalarRange()))
print('File Size (kb): ' + str(reader.GetOutput().GetActualMemorySize()))

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

# Set render window
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1800, 1200)

# Set renderer for 3 viewports
ren = [vtk.vtkRenderer() for i in range(3)]
ren[0].SetViewport(0, 0, 2/3, 1)
renWin.AddRenderer(ren[0])
ren[1].SetViewport(2/3, 1/2, 1, 1)
renWin.AddRenderer(ren[1])
ren[2].SetViewport(2/3, 0, 1, 1/2)
renWin.AddRenderer(ren[2])

# For viewport 1, create an interactable plane widget using vtkImagePlaneWidget class
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
volume = vtk.vtkVolume()
planeWidget = vtk.vtkImagePlaneWidget()
planeWidget.SetInteractor(iren)
planeWidget.SetCurrentRenderer(ren[0])
planeWidget.SetInputData(reader.GetOutput())
planeWidget.SetPlaneOrientationToZAxes()
planeWidget.On()

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
ren[0].AddVolume(volume)

# In viewport 2, display the content of the sampled CT dataset using GetResliceOutput() function
sampledCTMapper = vtk.vtkImageMapper()
sampledCTMapper.SetInputData(planeWidget.GetResliceOutput())
sampledCTActor = vtk.vtkActor2D()
sampledCTActor.SetMapper(sampledCTMapper)
ren[1].AddActor(sampledCTActor)

def UpdateSampleHistogram(obj, ev):
    # For viewport 3, construct the histogram of the sampled data using vtkImageAccumulate class
    histogram = vtk.vtkImageAccumulate()

    # retrieve the scalar range of the plane widget using GetScalarRange()
    range = obj.GetResliceOutput().GetScalarRange()
    r = int(range[1] - range[0])

    # using GetResliceOutput() function to get sampled data from vtkImagePlaneWidget object
    histogram.SetInputData(obj.GetResliceOutput())
    histogram.SetComponentExtent(0, r - 1, 0, 0, 0, 0)
    histogram.SetComponentOrigin(range[0], 0.0, 0.0)
    histogram.SetComponentSpacing(100, 0, 0)
    histogram.Update()

    # In viewport 3, using vtkXYPlotActor class for plotting the histogram
    plot = vtk.vtkXYPlotActor()
    plot.AddDataSetInputConnection(histogram.GetOutputPort())
    plot.SetXRange(range[0], range[1])
    plot.SetLabelFormat("%g")
    plot.SetXTitle("Scalar Value")
    plot.SetYTitle("Frequency")
    plot.SetXValuesToValue()
    ren[2].AddActor(plot)

# Ensure that the sample image and histogram are updated when user moves the image sampling plane in viewport 1
planeWidget.AddObserver('EndInteractionEvent', UpdateSampleHistogram)

# Render the scene
renWin.Render()

# Calculate Histogram after rendering
UpdateSampleHistogram(planeWidget, '')
iren.Start()
