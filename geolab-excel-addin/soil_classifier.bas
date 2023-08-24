Option Explicit

Const m_GRAVEL As String = "G"
Const m_SAND As String = "S"
Const CLAY As String = "C"
Const SILT As String = "M"
Const WELL_GRADED As String = "W"
Const POORLY_GRADED As String = "P"
Const ORGANIC As String = "O"
Const LOW_PLASTICITY As String = "L"
Const HIGH_PLASTICITY As String = "H"

Private Function IsClose( _
    a As Double, _
    b As Double, _
    Optional relTol As Double = 1E-9, _
    Optional absTol As Double = 0 _
) As Boolean
    If a = b Then
        IsClose = True
    ElseIf Abs(a - b) <= WorksheetFunction.Max(relTol * WorksheetFunction.Max(Abs(a), Abs(b)), absTol) Then
        IsClose = True
    Else
        IsClose = False
    End If
End Function

Private Function GroupIndex(fines As Double, liquidLmt As Double, plasticityIdx As Double) As Double
    Dim groupIdx As Double
    
    groupIdx = (fines - 35) * (0.2 + 0.005*(liquidLmt - 40)) + 0.01 * (fines - 15) * (plasticityIdx - 10)

    GroupIndex = IIf(groupIdx <=0, 0, Round(groupIdx, 0))

End Function

Private Function ALine(liquidLmt As Double)
    ALine = 0.73 * (liquidLmt - 20)
End Function

Private  Function CurvatureCoefficient(d10 As Double, d30 As Double, d60 As Double) As Double
    CurvatureCoefficient = d30 ^ 2 / (d10 * d60)
End Function

Private  Function UniformityCoefficient(d10 As Double, d60 As Double) As Double
    UniformityCoefficient = d60 / d10
End Function

Private  Function SoilGrade( _
    curvatureCoefficient As Double, _
    uniformityCoefficient As Double, _
    coarseSoil As String _
) As String
    Dim condition As Boolean

    ' Gravel
    If (coarseSoil = m_GRAVEL) Then 
        condition = curvatureCoefficient > 1 and curvatureCoefficient < 3 and uniformityCoefficient >= 4
        SoilGrade = IIf(condition, WELL_GRADED, POORLY_GRADED)
    
    ' Sand
    Else
        condition = curvatureCoefficient > 1 and curvatureCoefficient < 3 and uniformityCoefficient >= 6
        SoilGrade = IIf(condition, WELL_GRADED, POORLY_GRADED)
    End If

End Function

Private  Function DualSoilClassifier( _
    liquidLmt As Double, _
    plasticityIdx As Double, _ 
    curvatureCoefficient As Double, _
    uniformityCoefficient As Double, _
    coarseSoil As String _
) As String
    Dim soilGrd As String, A_LINE As Double, fineSoil As String

    soilGrd = SoilGrade(curvatureCoefficient, uniformityCoefficient, coarseSoil)
    A_LINE = ALine(liquidLmt)

    fineSoil = IIf(plasticityIdx > A_LINE, CLAY, SILT)

    DualSoilClassifier = coarseSoil & soilGrd & "-" & coarseSoil & fineSoil

End Function

Private Function ClassifyCoarseSoil( _
    liquidLmt As Double, _
    plasticLmt As Double, _
    plasticityIdx As Double, _ 
    fines As Double, _
    sand As Double, _
    gravel As Double, _
    coarseSoil As String, _
    d10 As Double, _
    d30 As Double, _
    d60 As Double  _
) As String
    ' More than 12% pass No. 200 sieve
    If (fines > 12) Then
        Dim A_LINE As Double 

        A_LINE = ALine(liquidLmt)

        ' Limits plot in hatched zone on plasticity chart
        if (IsClose(plasticityIdx, A_LINE, relTol:=0.01)) Then  
            ClassifyCoarseSoil = coarseSoil & SILT & "-" & coarseSoil & CLAY   

        ' Above Aline 
        ElseIf (plasticityIdx > A_LINE) Then
            ClassifyCoarseSoil = coarseSoil & CLAY
        ' Below Aline
        Else
            ClassifyCoarseSoil = coarseSoil & SILT
        End If
    
    ' Between 5% and 12% pass No. 200 sieve
    ElseIf (fines >= 5 and fines <= 12) Then
        Dim cc As Double, cu As Double, soilGrd As String

        'Requires dual symbol based on gradation and plasticity characteristics
        If (d10=0 and d30=0 and d60=0) Then 
            ClassifyCoarseSoil = coarseSoil & WELL_GRADED & "-" & coarseSoil & SILT  & ", " & _
                             coarseSoil & POORLY_GRADED & "-" & coarseSoil & SILT & ", " & _ 
                             coarseSoil & WELL_GRADED & "-" & coarseSoil & CLAY & ", " & _
                             coarseSoil & POORLY_GRADED & "-" & coarseSoil & CLAY 
        Else
            cc = CurvatureCoefficient(d10, d30, d60)
            cu = UniformityCoefficient(d10, d60)
            
            ClassifyCoarseSoil = DualSoilClassifier(liquidLmt, plasticityIdx, cc, cu, coarseSoil)
        End If
    ' Less than 5% pass No. 200 sieve
    Else
        If (d10=0 and d30=0 and d60=0) Then 
            ClassifyCoarseSoil = coarseSoil & WELL_GRADED & "or" & coarseSoil & POORLY_GRADED
        Else
            cc = CurvatureCoefficient(d10, d30, d60)
            cu = UniformityCoefficient(d10, d60)
            soilGrd = SoilGrade(cc, cu, coarseSoil)

            ClassifyCoarseSoil = coarseSoil & soilGrd
        End If
    End If

End Function

Private Function ClassifyFineSoil( _
    liquidLmt As Double, _
    plasticLmt As Double, _
    plasticityIdx As Double, _
    color As Boolean, _
    odor As Boolean _
) As String
    ' High LL
    If (liquidLmt >= 50) Then 
        ' Above A line on plasticity chart
        If (plasticityIdx > ALine(liquidLmt)) Then 
            ClassifyFineSoil = CLAY & HIGH_PLASTICITY
        ' Below A line on plasticity chart 
        Else
            ' Color or odor
            If (color = True Or odor = True) Then 
                ClassifyFineSoil = ORGANIC & HIGH_PLASTICITY
            Else
                ClassifyFineSoil = SILT & HIGH_PLASTICITY
            End If
        
        End If
    ' Low LL
    Else
        ' Below A line or PI < 4
        If (plasticityIdx < ALine(liquidLmt) or plasticityIdx < 4) Then
            ' Color or odor
            If (color = True Or odor = True) Then 
                ClassifyFineSoil = ORGANIC & LOW_PLASTICITY
            Else
                ClassifyFineSoil = SILT & LOW_PLASTICITY
            End If
        
        ' Above A line and PI > 7
        ElseIf (plasticityIdx > ALine(liquidLmt) and plasticityIdx > 7) Then
            ClassifyFineSoil = CLAY & LOW_PLASTICITY
        
        ' Limits plot in hatched area on plasticity chart
        Else
            ClassifyFineSoil = SILT & LOW_PLASTICITY & "-" & CLAY & LOW_PLASTICITY
        End If
    
    End If
End Function

Public Function USCS( _
    liquidLmt As Double, _
    plasticLmt As Double, _
    plasticityIdx As Double, _ 
    fines As Double, _
    sand As Double, _
    gravel As Double, _
    Optional d10 As Double, _
    Optional d30 As Double, _
    Optional d60 As Double, _
    Optional color As Boolean = False, _
    Optional odor As Boolean = False _
) As String
    ' More than 50% passes the No. 200 sieve
    If (fines > 50) Then 
        USCS = ClassifyFineSoil(liquidLmt, plasticLmt, plasticityIdx, color, odor)
    
    ' 50% or more retained on No. 200 sieve
    Else
        If (sand > gravel) Then  
            USCS = ClassifyCoarseSoil( _
                liquidLmt, _
                plasticLmt, _ 
                plasticityIdx, _
                fines, _
                sand, _
                gravel, _ 
                coarseSoil:=m_SAND, _
                d10:=d10, _
                d30:=d30, _
                d60:=d60 _
                )
        Else
            USCS = ClassifyCoarseSoil( _
                liquidLmt, _
                plasticLmt, _ 
                plasticityIdx, _
                fines, _
                sand, _
                gravel, _ 
                coarseSoil:=m_GRAVEL, _
                d10:=d10, _
                d30:=d30, _
                d60:=d60 _
                )
        End If
    End If

End Function


Public Function AASHTO( _
    liquidLmt As Double, _
    plasticityIdx As Double, _ 
    fines As Double _
) As String
    Dim grpIdx As Double
    Dim subgradeInfo As String

    grpIdx = GroupIndex(fines, liquidLmt, plasticityIdx)
    subgradeInfo = " (" & grpIdx & ")"

    ' A1 - A3
    If (fines <= 35) Then  
        If (liquidLmt <= 40) Then  
            If (plasticityIdx <= 10) Then
                AASHTO = "A-2-4" & subgradeInfo
            Else
                AASHTO = "A-2-6" & subgradeInfo
            End If
        Else
            If (plasticityIdx <= 10) Then  
                AASHTO = "A-2-5" & subgradeInfo
            Else
                AASHTO = "A-2-7" & subgradeInfo
            End If
        End If

    ' A4 - A7
    Else
        If (liquidLmt <= 40) Then  
            If (plasticityIdx <= 10) Then
                AASHTO = "A4" & subgradeInfo
            Else
                AASHTO = "A6" & subgradeInfo
            End If
        Else
            If (plasticityIdx <= 10) Then  
                AASHTO = "A5" & subgradeInfo
            Else
                If (plasticityIdx <= liquidLmt - 30) Then
                    AASHTO = "A-7-5" & subgradeInfo
                Else 
                    AASHTO = "A-7-6" & subgradeInfo
                End If
            End If
        End If
    End If

End Function