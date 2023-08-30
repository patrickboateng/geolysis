Attribute VB_Name = "soil_classifier"
Option Explicit

Public Const gGRAVEL As String = "G"
Public Const gSAND As String = "S"
Public Const gCLAY As String = "C"
Public Const gSILT As String = "M"
Public Const gWELL_GRADED As String = "W"
Public Const gPOORLY_GRADED As String = "P"
Public Const gORGANIC As String = "O"
Public Const gLOW_PLASTICITY As String = "L"
Public Const gHIGH_PLASTICITY As String = "H"

Private Function GroupIndex(fines As Double, liquidLmt As Double, plasticityIdx As Double) As Double
    Dim x1#, x2#, x3#, x4#, groupIdx As Double

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
    fineSoil = IIf(AL.aboveALINE, gCLAY, gSILT)

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
            ClassifyCoarseSoil = coarseSoil & gSILT & "-" & coarseSoil & gCLAY

            ' Above Aline
        Elseif (AL.aboveALINE) Then
            ClassifyCoarseSoil = coarseSoil & gCLAY
            ' Below Aline
        Else
            ClassifyCoarseSoil = coarseSoil & gSILT
        End If

        ' Between 5% And 12% pass No. 200 sieve
    Elseif (PSD.fines >= 5 And PSD.fines <= 12) Then
        'Requires dual symbol based on gradation And plasticity characteristics
        If (PSD.hasParticleSizes) Then
            ClassifyCoarseSoil = DualSoilClassifier(AL, PSD, coarseSoil)
        Else
            ClassifyCoarseSoil = coarseSoil & gWELL_GRADED & "-" & coarseSoil & gSILT & ", " & _
            coarseSoil & gPOORLY_GRADED & "-" & coarseSoil & gSILT & ", " & _
            coarseSoil & gWELL_GRADED & "-" & coarseSoil & gCLAY & ", " & _
            coarseSoil & gPOORLY_GRADED & "-" & coarseSoil & gCLAY
        End If
        ' Less than 5% pass No. 200 sieve
    Else
        If (PSD.hasParticleSizes) Then
            Dim soilGrd As String

            soilGrd = PSD.grade(coarseSoil)

            ClassifyCoarseSoil = coarseSoil & soilGrd
        Else
            ClassifyCoarseSoil = coarseSoil & gWELL_GRADED & "Or" & coarseSoil & gPOORLY_GRADED
        End If
    End If

End Function

Private Function ClassifyFineSoil(Byref AL As clsAtterbergLmts, organic As Boolean) As String
    ' High LL
    If (AL.liquidLmt >= 50) Then
        ' Above A line on plasticity chart
        If (AL.aboveALINE) Then
            ClassifyFineSoil = gCLAY & gHIGH_PLASTICITY
            ' Below A line on plasticity chart
        Else
            ' Color Or odor
            If (organic = True) Then
                ClassifyFineSoil = gORGANIC & gHIGH_PLASTICITY
            Else
                ClassifyFineSoil = gSILT & gHIGH_PLASTICITY
            End If

        End If
        ' Low LL
    Else
        ' Below A line Or PI < 4
        If (Not AL.aboveALINE Or AL.plasticityIdx < 4) Then
            ' Color Or odor
            If (organic = True) Then
                ClassifyFineSoil = gORGANIC & gLOW_PLASTICITY
            Else
                ClassifyFineSoil = gSILT & gLOW_PLASTICITY
            End If

            ' Above A line And PI > 7
        Elseif (AL.aboveALINE And AL.plasticityIdx > 7) Then
            ClassifyFineSoil = gCLAY & gLOW_PLASTICITY

            ' Limits plot in hatched area on plasticity chart
        Else
            ClassifyFineSoil = gSILT & gLOW_PLASTICITY & "-" & gCLAY & gLOW_PLASTICITY
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
    Optional organic As Boolean _
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
        USCS = ClassifyFineSoil(AL, organic)

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
            USCS = ClassifyCoarseSoil(AL, PSD, coarseSoil:=gSAND)
        Else
            USCS = ClassifyCoarseSoil(AL, PSD, coarseSoil:=gGRAVEL)
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
                AASHTO = "A-4" & subgradeInfo
            Else
                AASHTO = "A-6" & subgradeInfo
            End If
        Else
            If (plasticityIdx <= 10) Then
                AASHTO = "A-5" & subgradeInfo
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


Sub RegisterUDF()
    ' One-time execution just To describe arguments For user-defined functions.
    Dim rowIdx As Long, functionDesc As String, ArgDesc() As String
    Dim workSheetName As String, functionName As String, category As String
    Dim ws As Worksheet

    workSheetName = "_IntelliSense_"
    functionName = "AASHTO"
    category = "Engineering"

    ReDim ArgDesc(2)

    functionDesc = "Returns the soil classification based on the AASHTO Classification system."
    ' liquid limit
    ArgDesc(0) = "Water content beyond which soils flows under their own weight (%)"
    ' plasticity index
    ArgDesc(1) = "Range of water content over which soil remains in plastic condition (%)"
    ' fines
    ArgDesc(2) = "Percentage of fines in soil sample (%)"

    Application.MacroOptions _
    Macro:=functionName, _
    Description:=functionDesc, _
    ArgumentDescriptions:=ArgDesc, _
    Category:=category

    Dim i As Long

    For i = 1 To Worksheets.count
        If Worksheets(i).Name = workSheetName Then
         Exit Sub
        End If

     Exit For
    Next i


    Worksheets.Add.Name = workSheetName
    Set ws = Worksheets(workSheetName)

    ws.Range("A1") = "FunctionInfo"
    ws.Range("B1") = 1

    ' AASHTO INTELLISENSE
    rowIdx = 2

    ws.Cells(rowIdx, 1) = functionName
    ws.Cells(rowIdx, 2) = functionDesc
    ws.Cells(rowIdx, 3) = "" ' Function help website
    ws.Cells(rowIdx, 4) = "liquidLmt"
    ws.Cells(rowIdx, 5) = ArgDesc(0)
    ws.Cells(rowIdx, 6) = "plasticityIdx"
    ws.Cells(rowIdx, 7) = ArgDesc(1)
    ws.Cells(rowIdx, 8) = "fines"
    ws.Cells(rowIdx, 9) = ArgDesc(2)

    ReDim ArgDesc(9)

    functionName = "USCS"
    functionDesc = "Returns the soil classification based on the USC system."
    ' liquid limit
    ArgDesc(0) = "Water content beyond which soils flows under their own weight (%)"
    ' plastic limit
    ArgDesc(1) = "Water content at which plastic deformation can be initiated (%)"
    ' plasticity index 
    ArgDesc(2) = "Range of water content over which soil remains in plastic condition (%)"
    ' fines
    ArgDesc(3) = "Percentage of fines in soil sample (%)"
    ' sand
    ArgDesc(4) = "Percentage of sand in soil sample (%)"
    ' gravel
    ArgDesc(5) = "Percentage of gravel in soil sample (%)"
    ' d10
    ArgDesc(6) = "Diameter at which 10% of the soil by weight is finer"
    ' d30
    ArgDesc(7) = "Diameter at which 30% of the soil by weight is finer"
    ' d60
    ArgDesc(8) = "Diameter at which 60% of the soil by weight is finer"
    ' organic
    ArgDesc(9) = "Determines If soil sample is organic Or inorganic"

    Application.MacroOptions _ 
    Macro:=functionName, _ 
    Description:=functionDesc, _ 
    ArgumentDescriptions:=ArgDesc, _
    Category:=category

    ' USCS INTELLISENSE
    rowIdx = 3

    ws.Cells(rowIdx, 1) = functionName
    ws.Cells(rowIdx, 2) = functionDesc
    ws.Cells(rowIdx, 3) = ""
    ws.Cells(rowIdx, 4) = "liquidLmt"
    ws.Cells(rowIdx, 5) = ArgDesc(0)
    ws.Cells(rowIdx, 6) = "plasticLmt"
    ws.Cells(rowIdx, 7) = ArgDesc(1)
    ws.Cells(rowIdx, 8) = "plasticityIdx"
    ws.Cells(rowIdx, 9) = ArgDesc(2)
    ws.Cells(rowIdx, 10) = "fines"
    ws.Cells(rowIdx, 11) = ArgDesc(3)
    ws.Cells(rowIdx, 12) = "sand"
    ws.Cells(rowIdx, 13) = ArgDesc(4)
    ws.Cells(rowIdx, 14) = "gravel"
    ws.Cells(rowIdx, 15) = ArgDesc(5)
    ws.Cells(rowIdx, 16) = "d10"
    ws.Cells(rowIdx, 17) = ArgDesc(6)
    ws.Cells(rowIdx, 18) = "d30"
    ws.Cells(rowIdx, 19) = ArgDesc(7)
    ws.Cells(rowIdx, 20) = "d60"
    ws.Cells(rowIdx, 21) = ArgDesc(8)
    ws.Cells(rowIdx, 22) = "organic"
    ws.Cells(rowIdx, 23) = ArgDesc(9)

    ws.Visible = xlSheetVeryHidden

    Debug.Print "Function registration was succesful"
End Sub
