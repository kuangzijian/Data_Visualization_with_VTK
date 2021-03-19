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

    threshold = vtk.vtkThresholdPoints()
    threshold.SetInputConnection(reader.GetOutputPort())
    threshold.ThresholdByUpper(200)

    mask = vtk.vtkMaskPoints()
    mask.SetInputConnection(threshold.GetOutputPort())
    mask.SetOnRatio(5)

    cone = vtk.vtkConeSource()
    cone.SetResolution(11)
    cone.SetHeight(1)
    cone.SetRadius(0.25)

    cones = vtk.vtkGlyph3D()
    cones.SetInputConnection(mask.GetOutputPort())
    cones.SetSourceConnection(cone.GetOutputPort())
    cones.SetScaleFactor(0.4)
    cones.SetScaleModeToScaleByVector()

    lut = vtk.vtkLookupTable()
    lut.SetHueRange(.667, 0.0)
    lut.Build()

    scalarRange = [0] * 2
    cones.Update()
    scalarRange[0] = cones.GetOutput().GetPointData().GetScalars().GetRange()[0]
    scalarRange[1] = cones.GetOutput().GetPointData().GetScalars().GetRange()[1]

    vectorMapper = vtk.vtkPolyDataMapper()
    vectorMapper.SetInputConnection(cones.GetOutputPort())
    vectorMapper.SetScalarRange(scalarRange[0], scalarRange[1])
    vectorMapper.SetLookupTable(lut)

    vectorActor = vtk.vtkActor()
    vectorActor.SetMapper(vectorMapper)

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
    ren1.AddActor(vectorActor)
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