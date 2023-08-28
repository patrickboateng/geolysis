Attribute VB_Name = "soil_classifier"

Option Explicit

Public Const mGRAVEL As String = "G"
Public Const mSAND As String = "S"
Public Const mCLAY As String = "C"
Public Const mSILT As String = "M"
Public Const mWELL_GRADED As String = "W"
Public Const mPOORLY_GRADED As String = "P"
Public Const mORGANIC As String = "O"
Public Const mLOW_PLASTICITY As String = "L"
Public Const mHIGH_PLASTICITY As String = "H"

Private Function GroupIndex(fines As Double, liquidLmt As Double, plasticityIdx As Double) As Double
    Dim expr1#, expr2#, expr3#, expr4#, groupIdx As Double

    x1 = IIf(fines - 35 < 0, 0, WorksheetFunction.Min(fines - 35, 40))
    x2 = IIf(liquidLmt - 40 < 0, 0, WorksheetFunction.Min(liquidLmt - 40, 20))
    x3 = IIf(fines - 15 < 0, 0, WorksheetFunction.Min(fines - 15, 40))
    x4 = IIf(plasticityIdx - 10 < 0, 0, WorksheetFunction.Min(plasticityIdx - 10, 20))

    groupIdx = (x1) * (0.2 + 0.005 * (x2)) + 0.01 * (x3) * (x4)

    GroupIndex = IIf(groupIdx <= 0, 0, Round(groupIdx, 0))

End Function

Private Function DualSoilClassifier(AL As clsAtterbergLmts, PSD As clsPSD, coarseSoil As String) As String
    Dim soilGrd As String, fineSoil As String

    soilGrd = PSD.grade(coarseSoil)
    fineSoil = IIf(AL.aboveALINE, mCLAY, mSILT)

    DualSoilClassifier = coarseSoil & soilGrd & "-" & coarseSoil & fineSoil
End Function

Private Function ClassifyCoarseSoil( _
    Byref AL As clsAtterbergLmts, _
    Byref PSD As clsPSD, _
    coarseSoil As String _
    ) As String
    ' More than 12% pass No. 200 sieve
    If (PSD.fines > 12) Then
        ' Limits plot in hatched zone on plasticity chart
        If (AL.limitPlotInHatchedZone) Then
            ClassifyCoarseSoil = coarseSoil & mSILT & "-" & coarseSoil & mCLAY

            ' Above Aline
        Elseif (AL.aboveALINE) Then
            ClassifyCoarseSoil = coarseSoil & mCLAY
            ' Below Aline
        Else
            ClassifyCoarseSoil = coarseSoil & mSILT
        End If

        ' Between 5% And 12% pass No. 200 sieve
    Elseif (PSD.fines >= 5 And PSD.fines <= 12) Then
        'Requires dual symbol based on gradation And plasticity characteristics
        If (PSD.hasParticleSizes) Then
            ClassifyCoarseSoil = DualSoilClassifier(AL, PSD, coarseSoil)
        Else
            ClassifyCoarseSoil = coarseSoil & mWELL_GRADED & "-" & coarseSoil & mSILT & ", " & _
            coarseSoil & mPOORLY_GRADED & "-" & coarseSoil & mSILT & ", " & _
            coarseSoil & mWELL_GRADED & "-" & coarseSoil & mCLAY & ", " & _
            coarseSoil & mPOORLY_GRADED & "-" & coarseSoil & mCLAY
        End If
        ' Less than 5% pass No. 200 sieve
    Else
        If (PSD.hasParticleSizes) Then
            Dim soilGrd As String

            soilGrd = PSD.grade(coarseSoil)

            ClassifyCoarseSoil = coarseSoil & soilGrd
        Else
            ClassifyCoarseSoil = coarseSoil & mWELL_GRADED & "Or" & coarseSoil & mPOORLY_GRADED
        End If
    End If

End Function

Private Function ClassifyFineSoil( _
    Byref AL As clsAtterbergLmts, _
    color As Boolean, _
    odor As Boolean _
    ) As String
    ' High LL
    If (AL.liquidLmt >= 50) Then
        ' Above A line on plasticity chart
        If (AL.aboveALINE) Then
            ClassifyFineSoil = mCLAY & mHIGH_PLASTICITY
            ' Below A line on plasticity chart
        Else
            ' Color Or odor
            If (color = True Or odor = True) Then
                ClassifyFineSoil = mORGANIC & mHIGH_PLASTICITY
            Else
                ClassifyFineSoil = mSILT & mHIGH_PLASTICITY
            End If

        End If
        ' Low LL
    Else
        ' Below A line Or PI < 4
        If (Not AL.aboveALINE Or AL.plasticityIdx < 4) Then
            ' Color Or odor
            If (color = True Or odor = True) Then
                ClassifyFineSoil = mORGANIC & mLOW_PLASTICITY
            Else
                ClassifyFineSoil = mSILT & mLOW_PLASTICITY
            End If

            ' Above A line And PI > 7
        Elseif (AL.aboveALINE And AL.plasticityIdx > 7) Then
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

    Dim AL As clsAtterbergLmts
    Dim PSD As clsPSD

    Set AL = New clsAtterbergLmts
    With AL
        .liquidLmt = liquidLmt
        .plasticLmt = plasticLmt
        .plasticityIdx = plasticityIdx
    End With

    If (fines > 50) Then
        USCS = ClassifyFineSoil(AL, color, odor)

        ' 50% Or more retained on No. 200 sieve
    Else
        Set PSD = New clsPSD
        With PSD
            .fines = fines
            .sand = sand
            .gravel = gravel
            .d10 = d10
            .d30 = d30
            .d60 = d60
        End With

        If (PSD.sand > PSD.gravel) Then
            USCS = ClassifyCoarseSoil(AL, PSD, coarseSoil:=mSAND)
        Else
            USCS = ClassifyCoarseSoil(AL, PSD, coarseSoil:=mGRAVEL)
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
    ' One-time execution just To describe arguments For user-defined functions.
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
    ArgumentDescriptions:=argDesc, _
    Category:="Engineering"

End Sub

Sub RegisterUSCSFunction()

End Sub
