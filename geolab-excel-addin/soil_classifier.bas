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

    If (groupIdx <= 0) Then 
        GroupIndex = 0
    Else
        GroupIndex = Round(groupIdx, 0)
    End If

End Function

Private Function ALine(liquidLmt As Double)

    ALine = 0.73 * (liquidLmt - 20)

End Function

Private Function ClassifyCoarseSoil( _
    liquidLmt As Double, _
    plasticLmt As Double, _
    plasticityIdx As Double, _ 
    fines As Double, _
    sand As Double, _
    gravel As Double, _
    coarseSoil As String _
) As String
    ' More than 12% pass No. 200 sieve
    If (fines > 12) Then
        ' Limits plot in hatched zone on plasticity chart
        Dim A_LINE As Double 
        A_LINE = ALine(liquidLmt)

        if (IsClose(plasticityIdx, A_LINE, relTol=0.01)) Then  
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
        'Requires dual symbol based on gradation and plasticity characteristics
        ClassifyCoarseSoil = coarseSoil & WELL_GRADED & "-" & coarseSoil & SILT  & ", " & _
                             coarseSoil & POORLY_GRADED & "-" & coarseSoil & SILT & ", " & _ 
                             coarseSoil & WELL_GRADED & "-" & coarseSoil & CLAY & ", " & _
                             coarseSoil & POORLY_GRADED & "-" & coarseSoil & CLAY 

    ' Less than 5% pass No. 200 sieve
    Else
        ClassifyCoarseSoil = coarseSoil & WELL_GRADED & "or" & coarseSoil & POORLY_GRADED
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

Function USCS( _
    liquidLmt As Double, _
    plasticLmt As Double, _
    plasticityIdx As Double, _ 
    fines As Double, _
    sand As Double, _
    gravel As Double, _
    Optional color As Boolean = False, _
    Optional odor As Boolean = False _
) As String

    ' More than 50% passes the No. 200 sieve
    If (fines > 50) Then 
        USCS = ClassifyFineSoil(liquidLmt, plasticLmt, plasticityIdx, color, odor)
    
    ' 50% or more retained on No. 200 sieve
    Else
    
        Dim coarseSoil As String
        
        If (sand > gravel) Then  
            coarseSoil = m_SAND
            USCS = ClassifyCoarseSoil(liquidLmt, plasticLmt, plasticityIdx, fines, sand, gravel, coarseSoil)
        Else
            coarseSoil = m_GRAVEL
            USCS = ClassifyCoarseSoil(liquidLmt, plasticLmt, plasticityIdx, fines, sand, gravel, coarseSoil)
        End If
    End If

End Function


Function AASHTO( _
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