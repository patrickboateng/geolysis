Option Explicit

Const mGRAVEL As String = "G"
Const mSAND As String = "S"
Const mCLAY As String = "C"
Const mSILT As String = "M"
Const mWELL_GRADED As String = "W"
Const mPOORLY_GRADED As String = "P"
Const mORGANIC As String = "O"
Const mLOW_PLASTICITY As String = "L"
Const mHIGH_PLASTICITY As String = "H"

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
    Dim expr1#, expr2#, expr3#, expr4#, groupIdx As Double

    expr1 = IIf(fines - 35 < 0, 0, WorksheetFunction.Min(fines - 35, 40))
    expr2 = IIf(liquidLmt - 40 < 0, 0, WorksheetFunction.Min(liquidLmt - 40, 20))
    expr3 = IIf(fines - 15 < 0, 0, WorksheetFunction.Min(fines - 15, 40))
    expr4 = IIf(plasticityIdx - 10 < 0, 0, WorksheetFunction.Min(plasticityIdx - 10, 20))

    groupIdx = (expr1) * (0.2 + 0.005*(expr2)) + 0.01 * (expr3) * (expr4)

    GroupIndex = IIf(groupIdx <= 0, 0, Round(groupIdx, 0))

End Function

Private Function ALine(liquidLmt As Double)
    ALine = 0.73 * (liquidLmt - 20)
End Function

Private Function CurvatureCoefficient(d10 As Double, d30 As Double, d60 As Double) As Double
    CurvatureCoefficient = d30 ^ 2 / (d10 * d60)
End Function

Private Function UniformityCoefficient(d10 As Double, d60 As Double) As Double
    UniformityCoefficient = d60 / d10
End Function

Private Function SoilGrade( _
    curvatureCoefficient As Double, _
    uniformityCoefficient As Double, _
    coarseSoil As String _
) As String
    Dim condition As Boolean

    ' Gravel
    If (coarseSoil = mGRAVEL) Then 
        condition = curvatureCoefficient > 1 and curvatureCoefficient < 3 and uniformityCoefficient >= 4
        SoilGrade = IIf(condition, mWELL_GRADED, mPOORLY_GRADED)
    
    ' Sand
    Else
        condition = curvatureCoefficient > 1 and curvatureCoefficient < 3 and uniformityCoefficient >= 6
        SoilGrade = IIf(condition, mWELL_GRADED, mPOORLY_GRADED)
    End If

End Function

Private Function DualSoilClassifier( _
    liquidLmt As Double, _
    plasticityIdx As Double, _ 
    curvatureCoefficient As Double, _
    uniformityCoefficient As Double, _
    coarseSoil As String _
) As String
    Dim soilGrd As String, A_LINE As Double, fineSoil As String

    soilGrd = SoilGrade(curvatureCoefficient, uniformityCoefficient, coarseSoil)
    A_LINE = ALine(liquidLmt)

    fineSoil = IIf(plasticityIdx > A_LINE, mCLAY, mSILT)

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
            ClassifyCoarseSoil = coarseSoil & mSILT & "-" & coarseSoil & mCLAY   

        ' Above Aline 
        ElseIf (plasticityIdx > A_LINE) Then
            ClassifyCoarseSoil = coarseSoil & mCLAY
        ' Below Aline
        Else
            ClassifyCoarseSoil = coarseSoil & mSILT
        End If
    
    ' Between 5% and 12% pass No. 200 sieve
    ElseIf (fines >= 5 and fines <= 12) Then
        Dim cc As Double, cu As Double, soilGrd As String

        'Requires dual symbol based on gradation and plasticity characteristics
        If (d10=0 and d30=0 and d60=0) Then 
            ClassifyCoarseSoil = coarseSoil & mWELL_GRADED & "-" & coarseSoil & mSILT  & ", " & _
                             coarseSoil & mPOORLY_GRADED & "-" & coarseSoil & mSILT & ", " & _ 
                             coarseSoil & mWELL_GRADED & "-" & coarseSoil & mCLAY & ", " & _
                             coarseSoil & mPOORLY_GRADED & "-" & coarseSoil & mCLAY 
        Else
            cc = CurvatureCoefficient(d10, d30, d60)
            cu = UniformityCoefficient(d10, d60)
            
            ClassifyCoarseSoil = DualSoilClassifier(liquidLmt, plasticityIdx, cc, cu, coarseSoil)
        End If
    ' Less than 5% pass No. 200 sieve
    Else
        If (d10=0 and d30=0 and d60=0) Then 
            ClassifyCoarseSoil = coarseSoil & mWELL_GRADED & "or" & coarseSoil & mPOORLY_GRADED
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
            ClassifyFineSoil = mCLAY & mHIGH_PLASTICITY
        ' Below A line on plasticity chart 
        Else
            ' Color or odor
            If (color = True Or odor = True) Then 
                ClassifyFineSoil = mORGANIC & mHIGH_PLASTICITY
            Else
                ClassifyFineSoil = mSILT & mHIGH_PLASTICITY
            End If
        
        End If
    ' Low LL
    Else
        ' Below A line or PI < 4
        If (plasticityIdx < ALine(liquidLmt) or plasticityIdx < 4) Then
            ' Color or odor
            If (color = True Or odor = True) Then 
                ClassifyFineSoil = mORGANIC & mLOW_PLASTICITY
            Else
                ClassifyFineSoil = mSILT & mLOW_PLASTICITY
            End If
        
        ' Above A line and PI > 7
        ElseIf (plasticityIdx > ALine(liquidLmt) and plasticityIdx > 7) Then
            ClassifyFineSoil = mCLAY & mLOW_PLASTICITY
        
        ' Limits plot in hatched area on plasticity chart
        Else
            ClassifyFineSoil = mSILT & mLOW_PLASTICITY & "-" & mCLAY & mLOW_PLASTICITY
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
    Optional color As Boolean, _
    Optional odor As Boolean _
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
                coarseSoil:=mSAND, _
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
                coarseSoil:=mGRAVEL, _
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


Sub RegisterAASHTOFunction()
' One-time execution just to describe arguments for user-defined functions.
    Dim desc As String, argDesc(1 To 3) As String

    desc = "Returns the soil classification based on the AASHTO Classification system." 
    ' liquid limit
    argDesc(1) = "Water content beyond which soils flows under their own weight (%)"
    ' plasticity index
    argDesc(2) = "Range of water content over which soil remains in plastic condition (%)"
    ' fines
    argDesc(3) = "Percentage of fines in soil sample (%)"

    Application.MacroOptions _
        Macro:="AASHTO", _
        Description:=desc, _
        ArgumentDescriptions:=ArgDesc, _
        Category:="Engineering"

End Sub

Sub RegisterUSCSFunction()

End Sub