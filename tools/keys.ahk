#SingleInstance force
CoordMode, Mouse, Screen;

; https://www.autohotkey.com/docs/KeyList.htm

:*:;pycode::import code; code.interact(local={{}**locals(), **globals(){}})
:*:;mci::mvn clean install
:*:;mcsi::mvn clean install -DskipTests

:*:;yy::{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}{ENTER}
:*:;zz::reset{ENTER}
:*:;pp::ping google.com -t{ENTER}
:*:;xp::xargs -I{{}{}}
:*:;tlh::tail -f -n {+}0 $(ls -t | head -1)
:*:;etlh::tail -f -n {+}0 $(find /. 2>/dev/null | grep hadoop | grep syslog$ | head -1)
:*:;ltlh::tail -F -n {+}0 'C:\Users\jguzman2\dont_upload\logs.txt'

:*:c;tlh::tail -f -n {+}0 $(ls -t | head -1) | colorizer{ENTER}
:*:c;etlh::tail -f -n {+}0 $(find /. 2>/dev/null | grep hadoop | grep syslog$ | head -1) | colorizer{ENTER}
:*:c;ltlh::tail -F -n {+}0 'C:\Users\jguzman2\dont_upload\logs.txt' | colorizer{ENTER}

:*:;clh::cat $(ls -t | head -1)

:*:;jprint::
{
	Send, System.out.println();
	Send, {Left}
	Send, {Left}
	Return
}

:*:;initc::
FileRead, clipboard, %A_ScriptDir%\colorizer.sh.txt
MsgBox, Pasting:`n%clipboard%
SendInput, +{Insert}{Enter}
return

; ^SPACE:: Winset, Alwaysontop, , A
; ^UP:: WinSet, Style, +0xC00000, A
; ^DOWN:: WinSet, Style, -0xC00000, A
; ^RIGHT:: WinHide, A
; ^LEFT:: WinShow, A
