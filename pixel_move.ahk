#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

; make a integer variable to store the mouse offset
global mouseOffset := 0

; when 0 is hit popup with offset and reset offset
0::
    MsgBox, 0, Mouse Offset, %mouseOffset%`n`nResetting offset to 0
    mouseOffset := 0
return

; move the mouse up 5 pixels when 6 is pressed and store the offset in the variable
6::
    mouseOffset := mouseOffset - 5
    MouseMove, 0, -5, 0, R
return

; move the mouse down 5 pixels when 5 is pressed and store the offset in the variable
5::
    mouseOffset := mouseOffset + 5
    MouseMove, 0, 5, 0, R
return

; move the mouse up 10 pixels when 8 is pressed and store the offset in the variable
8::
    mouseOffset := mouseOffset - 10
    MouseMove, 0, -10, 0, R
return

; move the mouse down 10 pixels when 9 is pressed and store the offset in the variable
9::
    mouseOffset := mouseOffset + 10
    MouseMove, 0, 10, 0, R
return

; move mouse to straight up when 7 is pressed
4::
    MouseMove, 0, -1440, 0, R
return

; move mouse to straight up when 7 is pressed
7::
    DllCall("mouse_event", uint, 1, int, 2944, int, -1233)
return
; exit app when 
j::ExitApp