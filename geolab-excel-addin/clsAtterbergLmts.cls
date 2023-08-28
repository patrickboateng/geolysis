VERSION 1.0 CLASS
BEGIN
MultiUse = -1  'True
END
Attribute VB_Name = "clsAtterbergLmts"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

Option Explicit

Private liquidLmt_ As Double
Private plasticLmt_ As Double
Private plasticityIdx_ As Double

Private Sub Class_Initialize(LL As Double, PL As Double, PI As Double)
    liquidLmt_ = LL
    plasticLmt_ = PL
    plasticityIdx_ = PI
End Sub

Private Function IsClose( _
    a As Double, _
    b As Double, _
    Optional relTol As Double = 0.01, _
    Optional absTol As Double = 0 _
    ) As Boolean
    If a = b Then
        IsClose = True
    Elseif Abs(a - b) <= WorksheetFunction.Max(relTol * WorksheetFunction.Max(Abs(a), Abs(b)), absTol) Then
        IsClose = True
    Else
        IsClose = False
    End If
End Function

Private Function ALine()
    ALine = 0.73 * (Me.liquidLmt - 20)
End Function

Public Property Get liquidLmt() As Double
liquidLmt = liquidLmt_
End Property

Public Property Let liquidLmt(val As Double)
liquidLmt_ = val
End Property

Public Property Get plasticLmt() As Double
plasticLmt = plasticLmt_
End Property

Public Property Let plasticLmt(val As Double)
plasticLmt_ = val
End Property

Public Property Get plasticityIdx() As Double
plasticityIdx = plasticityIdx_
End Property

Public Property Let plasticityIdx(val As Double)
plasticityIdx_ = val
End Property

Public Function aboveALINE() As Boolean
    aboveALINE = IIf(Me.plasticityIdx > ALine, True, False)
End Function

Public Function limitPlotInHatchedZone() As Boolean
    limitPlotInHatchedZone = IIf(IsClose(Me.plasticityIdx, ALine), True, False)
End Function

Public Function fineSoil() As String
    fineSoil = IIf(Me.aboveALINE, mCLAY, mSILT)
End Function

