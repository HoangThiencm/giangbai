param($docxPath)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$inDocx = (Resolve-Path $docxPath).Path
$outPdf = [System.IO.Path]::ChangeExtension($inDocx, ".pdf")
$doc = $word.Documents.Open($inDocx)
$doc.SaveAs([ref]$outPdf, [ref]17)
$doc.Close()
$word.Quit()
Write-Host "PDF generated: $outPdf"
