import vtk


def main():
    fileName = "FullHead.mhd" # path to the MHD file

    # Initialize essential rendering objects
    ren = vtk.vtkRenderer()

    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Read MHD file
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(fileName)
    reader.Update()

    # Apply Marching Cubes algorithm
    iso = vtk.vtkMarchingCubes()
    iso.SetInputConnection(reader.GetOutputPort())
    iso.ComputeGradientsOn()
    iso.ComputeScalarsOff()
    iso.SetValue(0, 1150)

    # Polydata mapper for the iso-surface
    isoMapper = vtk.vtkPolyDataMapper()
    isoMapper.SetInputConnection(iso.GetOutputPort())
    isoMapper.ScalarVisibilityOff()

    # Actor for the iso surface
    isoActor = vtk.vtkActor()
    isoActor.SetMapper(isoMapper)
    isoActor.GetProperty().SetColor(1.,1.,1.)

    # Add iso-surface object to the renderer
    ren.AddActor(isoActor)
    ren.ResetCamera()
    ren.ResetCameraClippingRange()

    renWin.SetSize(640, 480)

    renWin.Render()
    iren.Start()





if __name__ == '__main__':
    main()