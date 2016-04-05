try: pvsimple
except:
  import pvsimple
  from pvsimple import *
pvsimple._DisableFirstRenderCameraReset()

dir='/home/fred/asteretude/kenyatta/resultat/resultatcubepoutre/vmis/'
i=1
filein=dir+'CHRCUM%D.med'%i
fileout=dir+'CHRCUM%D.png'%i
CHRCURM1_med = MEDReader( FileName=file)

AnimationScene1 = GetAnimationScene()
CHRCURM1_med.Frequencies = ['[0] -1', '[1] 4.94066e-324']
CHRCURM1_med.Groups = ['GROUP/MAIL/OnCell/base', 'GROUP/MAIL/OnCell/toutface', 'GROUP/MAIL/OnCell/tout', 'GROUP/MAIL/OnCell/forc', 'GROUP/MAIL/OnCell/No_Group']
CHRCURM1_med.PointArrays = ['CHRATIO']

AnimationScene1.EndTime = 4.9406564584124654e-324
AnimationScene1.PlayMode = 'Snap To TimeSteps'
AnimationScene1.StartTime = -1.0

CHRCURM1_med.Entity = ['CELL_TYPE/MED_CELL/MED_HEXA8']

RenderView1 = GetRenderView()
a1_CHRATIO_PVLookupTable = GetLookupTableForArray( "CHRATIO", 1, NanColor=[0.25, 0.0, 0.0], RGBPoints=[1.0, 0.23000000000000001, 0.29899999999999999, 0.754, 1.0, 0.70599999999999996, 0.016, 0.14999999999999999], VectorMode='Magnitude', ColorSpace='Diverging', ScalarRangeInitialized=1.0 )

a1_CHRATIO_PiecewiseFunction = CreatePiecewiseFunction()

DataRepresentation1 = Show()
DataRepresentation1.ConstantRadius = 0.44785425863863337
DataRepresentation1.EdgeColor = [0.0, 0.0, 0.50000762951094835]
DataRepresentation1.PointSpriteDefaultsInitialized = 1
DataRepresentation1.ScalarOpacityFunction = a1_CHRATIO_PiecewiseFunction
DataRepresentation1.ColorArrayName = 'CHRATIO'
DataRepresentation1.ScalarOpacityUnitDistance = 1.5553290377917328
DataRepresentation1.Texture = []
DataRepresentation1.LookupTable = a1_CHRATIO_PVLookupTable
DataRepresentation1.RadiusRange = [0.0, 0.44785425863863337]

RenderView1.CenterOfRotation = [12.0, 6.0, 6.0]

Slice1 = Slice( SliceType="Plane" )

RenderView1.CameraPosition = [12.0, 6.0, 62.784609690826535]
RenderView1.CameraFocalPoint = [12.0, 6.0, 6.0]
RenderView1.CameraClippingRange = [44.276763593918268, 72.666378836188926]
RenderView1.CameraParallelScale = 14.696938456699069

DataRepresentation1.RadiusRange = [0.0, 0.44785399999999997]

Slice1.SliceOffsetValues = [0.0]
Slice1.SliceType.Origin = [12.0, 6.0, 6.0]
Slice1.SliceType = "Plane"

DataRepresentation2 = Show()
DataRepresentation2.ConstantRadius = 0.44785425863863337
DataRepresentation2.EdgeColor = [0.0, 0.0, 0.50000762951094835]
DataRepresentation2.PointSpriteDefaultsInitialized = 1
DataRepresentation2.ColorArrayName = 'CHRATIO'
DataRepresentation2.Texture = []
DataRepresentation2.LookupTable = a1_CHRATIO_PVLookupTable
DataRepresentation2.RadiusRange = [0.0, 0.44785399999999997]

RenderView1.CameraClippingRange = [41.687034101253943, 75.926314839873911]

DataRepresentation1.Representation = 'Volume'
DataRepresentation1.Visibility = 1
DataRepresentation1.Texture = []

WriteImage(fileout)

Delete(DataRepresentation2)
Delete(SliceType)
Delete(Slice1)
Delete(DataRepresentation1)
Delete(CHRCURM1_med)

Render()
