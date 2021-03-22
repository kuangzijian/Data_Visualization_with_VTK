import vtk
from vtk.util.colors import brown_ochre, tomato, banana, mint

# Read the STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("trex.stl")
reader.Update()

# Compute normals
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# Create a plane using vtkPlane class
plane = vtk.vtkPlane()
# And set the center of the plane to be the center of the 3D model
polyData = reader.GetOutput()
modelCenter = polyData.GetCenter()
plane.SetOrigin(modelCenter)

# Set the normal vector to [1, 15, 1]
plane.SetNormal(1, 15, 1)

# Clip the data using vtkClipPolyData class
clipper = vtk.vtkClipPolyData()
# And set the clipping value of the implicit function to zero
clipper.SetValue(0)
clipper.SetInputConnection(normals.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()

# Set the clipped out part of the 3D model
clippedMapper = vtk.vtkPolyDataMapper()
clippedMapper.SetInputData(clipper.GetClippedOutput())
clippedMapper.ScalarVisibilityOff()
backProp = vtk.vtkProperty()
backProp.SetDiffuseColor(tomato)
clippedActor = vtk.vtkActor()
clippedActor.SetMapper(clippedMapper)
clippedActor.GetProperty().SetColor(mint)
clippedActor.SetBackfaceProperty(backProp)
# And use surface representation to display the clipped out parts
clippedActor.GetProperty().SetRepresentationToSurface()

# Set the remaining part of the 3D model
remainingMapper = vtk.vtkPolyDataMapper()
remainingMapper.SetInputConnection(clipper.GetOutputPort())
remainingMapper.ScalarVisibilityOff()
remainingActor = vtk.vtkActor()
remainingActor.SetMapper(remainingMapper)
# And use the wireframe representation to display the remaining parts
remainingActor.GetProperty().SetRepresentationToWireframe()

# Set the intersection area between the plane and polygonal data
cutEdges = vtk.vtkCutter()
cutEdges.SetInputConnection(normals.GetOutputPort())
cutEdges.SetCutFunction(plane)
cutEdges.GenerateCutScalarsOn()
cutEdges.SetValue(0, 0)
cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutEdges.GetOutputPort())
cutStrips.Update()
cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

# Use vtkTriangleFilter class for triangulation
cutTriangles = vtk.vtkTriangleFilter()
cutTriangles.SetInputData(cutPoly)
cutTriangles.Update()
cutMapper = vtk.vtkPolyDataMapper()
cutMapper.SetInputData(cutPoly)
cutMapper.SetInputConnection(cutTriangles.GetOutputPort())
cutActor = vtk.vtkActor()
cutActor.SetMapper(cutMapper)
cutActor.GetProperty().SetColor(banana)

# Display the plane. Use vtkSampleFunction and vtkContourFilter classes to
# create a polygonal data from the implicit plane function
planeSample = vtk.vtkSampleFunction()
# Set the bounds of the plane polygonal data to be the same as 3D model
bounds = polyData.GetBounds()
planeSample.SetImplicitFunction(plane)
planeSample.SetModelBounds(bounds)
planeSample.SetSampleDimensions(60, 60, 60)
planeSample.ComputeNormalsOff()
planeSurface = vtk.vtkContourFilter()
planeSurface.SetInputConnection(planeSample.GetOutputPort())
planeSurface.SetValue(0, 0.0)
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(planeSurface.GetOutputPort())
planeMapper.ScalarVisibilityOff()
planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.GetProperty().SetColor(tomato)

# Set render window, renderer and interactor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Set actor for the clipped out parts, the remaining parts,
# the intersection area, and the implicit plane
ren.AddActor(clippedActor)
ren.AddActor(remainingActor)
ren.AddActor(cutActor)
ren.AddActor(planeActor)

iren.Initialize()

# Provide the number of vertices for the original model, clipped out part, remaining part,
# and intersection part of the model
clippedPart = vtk.vtkCleanPolyData()
clippedPart.SetInputConnection(clipper.GetOutputPort())
clippedPart.Update()
remainingPart = vtk.vtkCleanPolyData()
remainingPart.SetInputData(clipper.GetClippedOutput())
remainingPart.Update()
print("Vertices for the original:" + str(polyData.GetNumberOfPoints()))
print("Vertices for the clipped out part:" + str(remainingPart.GetOutput().GetNumberOfPoints()))
print("Vertices for the remaining part:" + str(clippedPart.GetOutput().GetNumberOfPoints()))
print("Vertices for the intersection part:" + str(cutTriangles.GetOutput().GetNumberOfPoints()))

renWin.Render()
iren.Start()
