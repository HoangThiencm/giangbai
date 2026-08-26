$ErrorActionPreference = "Stop"
$xmlPath = "C:\Users\TUENHA~1\AppData\Local\Temp\yeucau-extract\unzip\word\document.xml"
[xml]$doc = Get-Content -Raw -Encoding UTF8 $xmlPath
$nsmgr = New-Object System.Xml.XmlNamespaceManager($doc.NameTable)
$nsmgr.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
$body = $doc.SelectSingleNode("//w:body", $nsmgr)

function Get-NodeLines($node) {
  $lines = New-Object System.Collections.Generic.List[string]
  foreach ($p in $node.SelectNodes(".//w:p", $nsmgr)) {
    $sb = New-Object System.Text.StringBuilder
    foreach ($t in $p.SelectNodes(".//w:t", $nsmgr)) { [void]$sb.Append($t.InnerText) }
    $line = ($sb.ToString() -replace "\s+", " ").Trim()
    if ($line) { $lines.Add($line) }
  }
  return $lines
}

function Test-AllCapsLine([string]$text) {
  $first = (@($text -split "`n")[0]).Trim()
  $letters = @($first.ToCharArray() | Where-Object { [char]::IsLetter($_) })
  if ($letters.Count -lt 6) { return $false }
  return -not ($letters | Where-Object { [char]::IsLower($_) })
}

function New-YccdEntry($themeVal, $topicVal, $items) {
  $cleanItems = New-Object System.Collections.Generic.List[string]
  foreach ($it in @($items)) {
    $t = ([string]$it).Trim()
    while ($t.Length -gt 0 -and ($t[0] -in @("-", "*", [char]0x2013, [char]0x2014, [char]0x2022))) {
      $t = $t.Substring(1).Trim()
    }
    if ($t) { $cleanItems.Add($t) }
  }
  return [pscustomobject]@{ theme = [string]$themeVal; topic = (([string]$topicVal) -replace '\.(\p{Lu})', '. $1'); items = $cleanItems }
}

$grades = @{
  "6" = New-Object System.Collections.Generic.List[object]
  "7" = New-Object System.Collections.Generic.List[object]
  "8" = New-Object System.Collections.Generic.List[object]
  "9" = New-Object System.Collections.Generic.List[object]
}
$state = @{ grade = "6"; theme = ""; group = ""; pending = $null; awaitingPractice = $false }

function Flush-Pending {
  if ($null -eq $state.pending) { return }
  $g = [string]$state.grade
  if (-not $grades.ContainsKey($g)) { $g = "6" }
  if ($state.pending.topic -and ($state.pending.items.Count -gt 0 -or $state.pending.topic.Length -gt 20)) {
    $grades[$g].Add($state.pending)
  }
  $state.pending = $null
}

foreach ($child in $body.ChildNodes) {
  if ($child.LocalName -eq "p") {
    $psb = New-Object System.Text.StringBuilder
    foreach ($t in $child.SelectNodes(".//w:t", $nsmgr)) { [void]$psb.Append($t.InnerText) }
    $pt = $psb.ToString().Trim()
    if ($pt -match "L.P\s*([6-9])") {
      Flush-Pending
      $state.grade = $Matches[1]
      $state.theme = ""
      $state.group = ""
      $state.awaitingPractice = $false
    }
    continue
  }
  if ($child.LocalName -ne "tbl") { continue }

  foreach ($tr in $child.SelectNodes("./w:tr", $nsmgr)) {
    $cellTexts = New-Object System.Collections.Generic.List[string]
    foreach ($tc in $tr.SelectNodes("./w:tc", $nsmgr)) {
      $cellTexts.Add(((Get-NodeLines $tc) -join "`n"))
    }
    $cells = @($cellTexts)
    $joined = ($cells -join " ").Trim()
    $firstCell = ([string]$cells[0]).Trim()
    if ($firstCell.StartsWith("N") -and $firstCell.Length -le 20 -and $joined.Length -lt 90 -and $joined -match "Y") { continue }

    if ($cells.Count -eq 1) {
      $text = $cells[0]
      $first = (@($text -split "`n")[0]).Trim()
      if (Test-AllCapsLine $text) {
        Flush-Pending
        $state.theme = $first
        $state.group = ""
        $state.awaitingPractice = $first.StartsWith("HO") -or $first.Length -gt 30
        $rest = @($text -split "`n")
        if ($state.awaitingPractice -and $rest.Count -gt 1) {
          $state.pending = New-YccdEntry $state.theme "Hoat dong thuc hanh va trai nghiem" $rest[1..($rest.Count-1)]
          $state.pending.topic = "Hoạt động thực hành và trải nghiệm"
        }
      } elseif ($state.awaitingPractice -and $state.pending) {
        foreach ($line in @($text -split "`n")) { if ($line.Trim()) { $state.pending.items.Add($line.Trim()) } }
      } elseif ($first -match "phong may tinh") {
        Flush-Pending
        $state.group = $first
        $state.awaitingPractice = $true
        $state.pending = New-YccdEntry $state.theme $first @()
      } else {
        Flush-Pending
        $state.group = $first
        $state.awaitingPractice = $false
        $more = @($text -split "`n")
        if ($more.Count -gt 1) {
          $state.pending = New-YccdEntry $state.theme $state.group $more[1..($more.Count-1)]
        }
      }
      continue
    }

    $c0 = $cells[0]
    $c1 = if ($cells.Count -ge 2) { $cells[1] } else { "" }
    $c2 = if ($cells.Count -ge 3) { $cells[2] } else { "" }
    if ($cells.Count -eq 2) { $c2 = $c1; $c1 = $c0; $c0 = "" }

    $state.awaitingPractice = $false
    $c1start = if ($c1) { $c1.Substring(0,1) } else { "" }
    $isCont = $false
    if ($null -ne $state.pending) {
      if ((-not $c0) -and (-not $c1) -and $c2) { $isCont = $true }
      elseif ((-not $c0) -and $c1start -eq "(") { $isCont = $true }
      elseif ((-not $c0) -and $c1start -and [char]::IsLetter($c1start[0]) -and -not [char]::IsUpper($c1start[0])) { $isCont = $true }
    }

    if ($isCont) {
      if ($c1) { $state.pending.topic = ($state.pending.topic.TrimEnd() + " " + $c1.TrimStart()).Trim() }
      if ($c2) {
        $parts = @($c2 -split "`n" | Where-Object { $_.Trim() })
        if ($parts.Count -gt 0) {
          if ($state.pending.items.Count -eq 0) {
            foreach ($p in $parts) { $state.pending.items.Add($p.Trim()) }
          } else {
            $lastIdx = $state.pending.items.Count - 1
            $state.pending.items[$lastIdx] = ($state.pending.items[$lastIdx].TrimEnd() + " " + $parts[0].TrimStart()).Trim()
            if ($parts.Count -gt 1) {
              foreach ($p in $parts[1..($parts.Count-1)]) { $state.pending.items.Add($p.Trim()) }
            }
          }
        }
      }
    } else {
      Flush-Pending
      if ($c0) { $state.group = (@($c0 -split "`n")[0]) }
      $topic = if ($c1) { $c1 } else { $state.group }
      $items = @()
      if ($c2) { $items = @($c2 -split "`n") }
      $state.pending = New-YccdEntry $state.theme $topic $items
    }
  }
}
Flush-Pending

function Merge-Continuations($list) {
  $out = New-Object System.Collections.Generic.List[object]
  foreach ($e in $list) {
    $topic = [string]$e.topic
    if (-not $topic) { continue }
    $start = $topic.Substring(0, 1)
    $isCont = $out.Count -gt 0 -and (
      $start -eq "(" -or
      ([char]::IsLetter($start[0]) -and -not [char]::IsUpper($start[0]))
    )
    if ($isCont) {
      $prev = $out[$out.Count - 1]
      $prev.topic = ($prev.topic.TrimEnd() + " " + $topic.TrimStart()).Trim()
      foreach ($it in $e.items) { if ($it) { $prev.items.Add([string]$it) } }
    } else {
      $out.Add($e)
    }
  }
  return $out
}

foreach ($g in @("6", "7", "8", "9")) {
  $grades[$g] = Merge-Continuations $grades[$g]
}

function ConvertTo-JsString([string]$s) {
  $s = [string]$s
  $s = $s.Replace("\", "\\").Replace('"', '\"').Replace("`r", "").Replace("`n", "\n")
  return $s
}

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine("/**")
[void]$sb.AppendLine(" * js/khbd-yccd.js")
[void]$sb.AppendLine(" * Yeu cau can dat Toan 6-9 trich tu GIAO AN/yeucau.docx")
[void]$sb.AppendLine(" * Nguon: CT GDPT 2018 / TT 32/2018/TT-BGDDT. Khong bia YCCD ngoai van ban nay.")
[void]$sb.AppendLine(" */")
[void]$sb.AppendLine("const KHBD_YCCD = {")
[void]$sb.AppendLine("  source: `"Thong tu 32/2018/TT-BGDDT - Chuong trinh GDPT 2018 mon Toan`",")
[void]$sb.AppendLine("  toan: {")
foreach ($g in @("6", "7", "8", "9")) {
  [void]$sb.AppendLine("    `"$g`": [")
  $entries = New-Object System.Collections.Generic.List[object]
  foreach ($item in $grades[$g]) { $entries.Add($item) }
  for ($i = 0; $i -lt $entries.Count; $i++) {
    $e = $entries[$i]
    [void]$sb.AppendLine("      {")
    [void]$sb.AppendLine(('        theme: "' + (ConvertTo-JsString $e.theme) + '",'))
    [void]$sb.AppendLine(('        topic: "' + (ConvertTo-JsString $e.topic) + '",'))
    [void]$sb.AppendLine("        items: [")
    $items = @($e.items)
    for ($j = 0; $j -lt $items.Count; $j++) {
      $comma = if ($j -lt $items.Count - 1) { "," } else { "" }
      [void]$sb.AppendLine(('          "' + (ConvertTo-JsString $items[$j]) + '"' + $comma))
    }
    [void]$sb.AppendLine("        ]")
    $ecomma = if ($i -lt $entries.Count - 1) { "," } else { "" }
    [void]$sb.AppendLine("      }$ecomma")
  }
  $gcomma = if ($g -ne "9") { "," } else { "" }
  [void]$sb.AppendLine("    ]$gcomma")
}
[void]$sb.AppendLine("  }")
[void]$sb.AppendLine("};")
[void]$sb.AppendLine("")

$outJs = Join-Path $env:TEMP "khbd-yccd-data.js"
[System.IO.File]::WriteAllText($outJs, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))
$jsonPath = Join-Path $env:TEMP "yccd-toan.json"
$jsonObj = [ordered]@{}
foreach ($g in @("6","7","8","9")) {
  $arr = @()
  foreach ($e in $grades[$g]) { $arr += [ordered]@{ theme = $e.theme; topic = $e.topic; items = @($e.items) } }
  $jsonObj[$g] = $arr
}
[System.IO.File]::WriteAllText($jsonPath, ($jsonObj | ConvertTo-Json -Depth 8), [System.Text.UTF8Encoding]::new($false))
Write-Output "JS=$outJs"
Write-Output "JSON=$jsonPath"
foreach ($g in @("6","7","8","9")) { Write-Output ("GRADE {0}: {1}" -f $g, $grades[$g].Count) }
foreach ($g in @("6","7","8","9")) {
  Write-Output ("---- $g ----")
  foreach ($e in $grades[$g]) { Write-Output ("* " + $e.topic.Substring(0, [Math]::Min(90, $e.topic.Length)) + " [" + $e.items.Count + "]") }
}
