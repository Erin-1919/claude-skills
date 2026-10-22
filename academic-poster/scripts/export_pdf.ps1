# Export a .pptx to PDF with the installed PowerPoint (exact fonts and layout).
# Usage: powershell -File export_pdf.ps1 <poster.pptx> [out.pdf]
param([Parameter(Mandatory)][string]$Pptx, [string]$Pdf)
$Pptx = (Resolve-Path $Pptx).Path
if (-not $Pdf) { $Pdf = [IO.Path]::ChangeExtension($Pptx, '.pdf') }
$Pdf = [IO.Path]::GetFullPath($Pdf)
$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($Pptx, $true, $false, $false)  # read-only, no window
    $pres.SaveAs($Pdf, 32)  # 32 = ppSaveAsPDF
    $pres.Close()
} finally { $app.Quit() }
Write-Output $Pdf
