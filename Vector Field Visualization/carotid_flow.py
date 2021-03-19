import vtk

def main():
    fileName = r"carotid.vtk"

    colors = vtk.vtkNamedColors()

    ren1 = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create the pipeline.
    reader = vtk.vtkStructuredPointsReader()
    reader.SetFileName(fileName)

    psource = vtk.vtkPointSource()
    psource.SetNumberOfPoints(25)
    psource.SetCenter(133.1, 116.3, 5.0)
    psource.SetRadius(2.0)

    threshold = vtk.vtkThresholdPoints()
    threshold.SetInputConnection(reader.GetOutputPort())
    threshold.ThresholdByUpper(275)

    streamers = vtk.vtkStreamTracer()
    streamers.SetInputConnection(reader.GetOutputPort())
    streamers.SetSourceConnection(psource.GetOutputPort())
    streamers.SetMaximumPropagation(100.0)
    streamers.SetInitialIntegrationStep(0.2)
    streamers.SetTerminalSpeed(.01)
    streamers.Update()
    scalarRange = [0] * 2
    scalarRange[0] = streamers.GetOutput().GetPointData().GetScalars().GetRange()[0]
    scalarRange[1] = streamers.GetOutput().GetPointData().GetScalars().GetRange()[1]

    tubes = vtk.vtkTubeFilter()
    tubes.SetInputConnection(streamers.GetOutputPort())
    tubes.SetRadius(0.3)
    tubes.SetNumberOfSides(6)
    tubes.SetVaryRadius(0)

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(.667, 0.0)
    lut.Build()

    streamerMapper = vtk.vtkPolyDataMapper()
    streamerMapper.SetInputConnection(tubes.GetOutputPort())
    streamerMapper.SetScalarRange(scalarRange[0], scalarRange[1])
    streamerMapper.SetLookupTable(lut)

    streamerActor = vtk.vtkActor()
    streamerActor.SetMapper(streamerMapper)

    # Speed contours.
    iso = vtk.vtkContourFilter()
    iso.SetInputConnection(reader.GetOutputPort())
    iso.SetValue(0, 175)

    isoMapper = vtk.vtkPolyDataMapper()
    isoMapper.SetInputConnection(iso.GetOutputPort())
    isoMapper.ScalarVisibilityOff()

    isoActor = vtk.vtkActor()
    isoActor.SetMapper(isoMapper)
    isoActor.GetProperty().SetRepresentationToWireframe()
    isoActor.GetProperty().SetOpacity(0.25)

    # Outline
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)
    outlineActor.GetProperty().SetColor(0., 0., 0.)

    # Add the actors to the renderer, set the background and size.
    ren1.AddActor(outlineActor)
    ren1.AddActor(streamerActor)
    ren1.AddActor(isoActor)
    ren1.SetBackground(1., 1., 1.)
    renWin.SetSize(640, 480)


    ren1.ResetCamera()
    ren1.ResetCameraClippingRange()

    # Render the image.
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()