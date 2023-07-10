#InstallKeybdHook
#UseHook
#SingleInstance Force

$numpad0::
send {enter} 0645 TOPF 0644 JGF 0630 MIDF 0617 ADF 0616 SUPF{enter}
return

$numpad9::
ExitApp
return