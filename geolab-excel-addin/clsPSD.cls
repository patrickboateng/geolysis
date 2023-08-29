Option Explicit

Private fines_ As Double
Private sand_ As Double
Private gravel_ As Double
Public d10 As Double
Public d30 As Double
Public d60 As Double

Private Function curvatureCoefficient() As Double
    curvatureCoefficient = (Me.d30 ^ 2) / (Me.d10 * Me.d60)
End Function

Private Function uniformityCoefficient() As Double
    uniformityCoefficient = Me.d60 / Me.d10
End Function

Public Property Get fines() As Double
fines = fines_
End Property

Public Property Let fines(val As Double)
fines_ = val
End Property

Public Property Get sand() As Double
sand = sand_
End Property

Public Property Let sand(val As Double)
sand_ = val
End Property

Public Property Get gravel() As Double
gravel = gravel_
End Property

Public Property Let gravel(val As Double)
gravel_ = val
End Property

Public Function hasParticleSizes() As Boolean
    If (d10 = 0 And d30 = 0 And d60 = 0) Then
        hasParticleSizes = False
    Else
        hasParticleSizes = True
    End If
End Function

Public Function grade(coarseSoil As String) As String
    ' Gravel
    If (coarseSoil = gGRAVEL) Then
        If (curvatureCoefficient > 1 And curvatureCoefficient < 3 _
            And uniformityCoefficient >= 4 _
            ) Then
            grade = gWELL_GRADED
        Else
            grade = gPOORLY_GRADED
        End If
    Else
        If (curvatureCoefficient > 1 And curvatureCoefficient < 3 _
            And uniformityCoefficient >= 6 _
            ) Then
            grade = gWELL_GRADED
        Else
            grade = gPOORLY_GRADED
        End If
    End If
End Function

