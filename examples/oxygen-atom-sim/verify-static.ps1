# LoopSpec v2 Static Verification Script
# Verifies the oxygen atom simulation meets criteria by static analysis of source code
# This is the evidence-gathering step for automated criteria

$ErrorActionPreference = "Stop"

$indexPath = Join-Path $PSScriptRoot "index.html"
$content = Get-Content $indexPath -Raw

$passed = 0
$failed = 0
$total = 0

function Test-Criterion {
    param([string]$Id, [string]$Name, [bool]$Result, [string]$Evidence)
    $script:total++
    if ($Result) {
        $script:passed++
        Write-Host "  [PASS] [$Id] $Name" -ForegroundColor Green
    } else {
        $script:failed++
        Write-Host "  [FAIL] [$Id] $Name" -ForegroundColor Red
    }
    Write-Host "         Evidence: $Evidence" -ForegroundColor Gray
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  LoopSpec v2 Static Verification" -ForegroundColor Cyan
Write-Host "  Oxygen Atom Simulation" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# --- C1: Nucleus with 8 protons + 8 neutrons ---
Write-Host "[C1] Nucleus particles:" -ForegroundColor Yellow

$protonMatches = [regex]::Matches($content, "name = i < 8 \? 'proton' : 'neutron'")
$loopMatch = [regex]::Match($content, "for \(let i = 0; i < (\d+); i\+\+\)")
$nucleusCount = if ($loopMatch.Success) { [int]$loopMatch.Groups[1].Value } else { 0 }
$hasNucleusGroup = $content.Contains("nucleusGroup.name = 'nucleus'")

Test-Criterion "C1" "Nucleus loop creates 16 particles" ($nucleusCount -eq 16) "Loop: for(let i=0; i<$nucleusCount; i++)"
Test-Criterion "C1" "Particles named proton/neutron (first 8 proton)" ($protonMatches.Count -gt 0) "Pattern: i < 8 ? 'proton' : 'neutron'"
Test-Criterion "C1" "Nucleus group named 'nucleus'" $hasNucleusGroup "nucleusGroup.name = 'nucleus'"

# Verify proton color is red
$protonColorMatch = [regex]::Match($content, "protonMaterial.*color:\s*(0x[a-fA-F0-9]+)")
$protonColor = if ($protonColorMatch.Success) { $protonColorMatch.Groups[1].Value } else { "not found" }
Test-Criterion "C1" "Proton material is red" ($protonColor -eq "0xff4444") "protonMaterial color: $protonColor"

# Verify neutron color is blue/gray
$neutronColorMatch = [regex]::Match($content, "neutronMaterial.*color:\s*(0x[a-fA-F0-9]+)")
$neutronColor = if ($neutronColorMatch.Success) { $neutronColorMatch.Groups[1].Value } else { "not found" }
Test-Criterion "C1" "Neutron material is blue/gray" ($neutronColor -eq "0x6688aa") "neutronMaterial color: $neutronColor"

# --- C2: Electron configuration 1s2 + 2s2 + 2p4 = 8 ---
Write-Host ""
Write-Host "[C2] Electron configuration:" -ForegroundColor Yellow

$has1sGroup = $content.Contains("orbital_1s")
$has2sGroup = $content.Contains("orbital_2s")
$has2pGroup = $content.Contains("orbital_2p")

# Count electron names
$electron1s = [regex]::Matches($content, "electron_1s_\d")
$electron2s = [regex]::Matches($content, "electron_2s_\d")
$filledLobes = [regex]::Matches($content, "electron_2p_p[xyz]_lobe\d_filled")

Test-Criterion "C2" "1s orbital group exists with 2 electrons" ($electron1s.Count -eq 2) "electron_1s matches: $($electron1s.Count)"
Test-Criterion "C2" "2s orbital group exists with 2 electrons" ($electron2s.Count -eq 2) "electron_2s matches: $($electron2s.Count)"
Test-Criterion "C2" "2p orbital has 4 filled lobes (4 electrons)" ($filledLobes.Count -eq 4) "filled lobe names: $($filledLobes.Count)"

$totalElectrons = $electron1s.Count + $electron2s.Count + $filledLobes.Count
Test-Criterion "C2" "Total electron count = 8" ($totalElectrons -eq 8) "$($electron1s.Count) + $($electron2s.Count) + $($filledLobes.Count) = $totalElectrons"

# --- C3: s-orbitals as spherical probability clouds ---
Write-Host ""
Write-Host "[C3] s-orbital geometry:" -ForegroundColor Yellow

$hasSphereGeo = $content.Contains("SphereGeometry(ORBITAL_1S_RADIUS")
$hasTransparent = [regex]::Match($content, "s1Material[\s\S]*?transparent:\s*true")
$hasOpacity = [regex]::Match($content, "s1Material[\s\S]*?opacity:\s*([0-9.]+)")
$s1Opacity = if ($hasOpacity.Success) { [double]$hasOpacity.Groups[1].Value } else { 1.0 }

Test-Criterion "C3" "1s uses SphereGeometry" $hasSphereGeo "SphereGeometry(ORBITAL_1S_RADIUS, ...)"
Test-Criterion "C3" "1s material is transparent" $hasTransparent.Success "transparent: true in s1Material"
Test-Criterion "C3" "1s opacity < 1 (probability cloud)" ($s1Opacity -lt 1.0) "opacity: $s1Opacity"

# --- C4: p-orbitals as dumbbells on x/y/z ---
Write-Host ""
Write-Host "[C4] p-orbital geometry:" -ForegroundColor Yellow

$hasLobeScale = $content.Contains("ORBITAL_2P_LOBE_SCALE")
$scaleMatch = [regex]::Match($content, "ORBITAL_2P_LOBE_SCALE = \[([^\]]+)\]")
$scaleValues = if ($scaleMatch.Success) { $scaleMatch.Groups[1].Value } else { "" }

# Check non-uniform scale (dumbbell)
$isNonUniform = $false
if ($scaleMatch.Success) {
    $parts = $scaleValues -split ","
    if ($parts.Count -eq 3) {
        $isNonUniform = [double]$parts[0].Trim() -ne [double]$parts[2].Trim()
    }
}

Test-Criterion "C4" "Lobe scale is non-uniform (ellipsoid/dumbbell)" $isNonUniform "ORBITAL_2P_LOBE_SCALE = [$scaleValues]"

# Check px along X
$pxPos = [regex]::Match($content, "px_pos = new THREE\.Vector3\(([^)]+)\)")
$pyPos = [regex]::Match($content, "py_pos = new THREE\.Vector3\(([^)]+)\)")
$pzPos = [regex]::Match($content, "pz_pos = new THREE\.Vector3\(([^)]+)\)")

Test-Criterion "C4" "px lobe positioned along X axis" ($pxPos.Success -and $pxPos.Groups[1].Value.Split(",")[0].Trim() -ne "0") "px_pos = ($($pxPos.Groups[1].Value))"
Test-Criterion "C4" "py lobe positioned along Y axis" ($pyPos.Success -and $pyPos.Groups[1].Value.Split(",")[1].Trim() -ne " 0") "py_pos = ($($pyPos.Groups[1].Value))"
Test-Criterion "C4" "pz lobe positioned along Z axis" ($pzPos.Success -and $pzPos.Groups[1].Value.Split(",")[2].Trim() -ne " 0") "pz_pos = ($($pzPos.Groups[1].Value))"

# --- C5: Animation loop exists ---
Write-Host ""
Write-Host "[C5] Animation performance:" -ForegroundColor Yellow

$hasRAF = $content.Contains("requestAnimationFrame(animate)")
$hasDelta = $content.Contains("currentTime - lastTime")
$hasFrameTimes = $content.Contains("frameTimes.push(delta)")

Test-Criterion "C5" "requestAnimationFrame loop exists" $hasRAF "requestAnimationFrame(animate) found"
Test-Criterion "C5" "Frame timing tracked for FPS measurement" ($hasDelta -and $hasFrameTimes) "delta calculation + frameTimes array"

# --- C6: OrbitControls ---
Write-Host ""
Write-Host "[C6] Camera controls:" -ForegroundColor Yellow

$hasOrbitControls = $content.Contains("new OrbitControls(camera")
$hasEnableRotate = $content.Contains("controls.enableRotate = true")
$hasEnableZoom = $content.Contains("controls.enableZoom = true")
$hasEnablePan = $content.Contains("controls.enablePan = true")

Test-Criterion "C6" "OrbitControls instantiated" $hasOrbitControls "new THREE.OrbitControls(camera, ...)"
Test-Criterion "C6" "enableRotate = true" $hasEnableRotate "controls.enableRotate = true"
Test-Criterion "C6" "enableZoom = true" $hasEnableZoom "controls.enableZoom = true"
Test-Criterion "C6" "enablePan = true" $hasEnablePan "controls.enablePan = true"

# --- C8: No obvious errors (static check) ---
Write-Host ""
Write-Host "[C8] Error-free initialization:" -ForegroundColor Yellow

$hasConsoleError = $content.Contains("console.error")
$hasUndefinedAccess = [regex]::Match($content, "\bundefined\b")
$hasProperClose = $content.Contains("</html>")

Test-Criterion "C8" "No console.error calls in source" (-not $hasConsoleError) "console.error present: $hasConsoleError"
Test-Criterion "C8" "HTML properly closed" $hasProperClose "</html> found"
Test-Criterion "C8" "Three.js CDN scripts included" ($content.Contains("unpkg.com/three@0.162.0")) "CDN URL found"

# --- C9: Hund's rule ---
Write-Host ""
Write-Host "[C9] Hund's rule (partial filling):" -ForegroundColor Yellow

$emptyLobes = [regex]::Matches($content, "electron_2p_p[xyz]_lobe\d_empty")
Test-Criterion "C9" "4 filled + 2 empty lobes" ($filledLobes.Count -eq 4 -and $emptyLobes.Count -eq 2) "filled: $($filledLobes.Count), empty: $($emptyLobes.Count)"

# Check px has 2 filled (paired), py/pz have 1 filled + 1 empty each
$pxFilled = [regex]::Matches($content, "electron_2p_px_lobe\d_filled")
$pyFilled = [regex]::Matches($content, "electron_2p_py_lobe\d_filled")
$pyEmpty = [regex]::Matches($content, "electron_2p_py_lobe\d_empty")
$pzFilled = [regex]::Matches($content, "electron_2p_pz_lobe\d_filled")
$pzEmpty = [regex]::Matches($content, "electron_2p_pz_lobe\d_empty")

Test-Criterion "C9" "px: 2 filled (paired)" ($pxFilled.Count -eq 2) "px filled lobes: $($pxFilled.Count)"
Test-Criterion "C9" "py: 1 filled + 1 empty (unpaired)" ($pyFilled.Count -eq 1 -and $pyEmpty.Count -eq 1) "py filled: $($pyFilled.Count), empty: $($pyEmpty.Count)"
Test-Criterion "C9" "pz: 1 filled + 1 empty (unpaired)" ($pzFilled.Count -eq 1 -and $pzEmpty.Count -eq 1) "pz filled: $($pzFilled.Count), empty: $($pzEmpty.Count)"

# Check opacity difference between filled and empty
$filledOpacityMatch = [regex]::Match($content, "pFilledMaterial[\s\S]*?opacity:\s*([0-9.]+)")
$emptyOpacityMatch = [regex]::Match($content, "pEmptyMaterial[\s\S]*?opacity:\s*([0-9.]+)")
$fOp = if ($filledOpacityMatch.Success) { [double]$filledOpacityMatch.Groups[1].Value } else { 0 }
$eOp = if ($emptyOpacityMatch.Success) { [double]$emptyOpacityMatch.Groups[1].Value } else { 0 }
Test-Criterion "C9" "Filled opacity > empty opacity (visual distinction)" ($fOp -gt $eOp) "filled: $fOp, empty: $eOp"

# --- C10: Info panel ---
Write-Host ""
Write-Host "[C10] Info panel content:" -ForegroundColor Yellow

$hasOxygen = $content.Contains(">Oxygen<")
$hasAtomicNum8 = $content.Contains(">8<")
$hasConfig = $content.Contains("1s") -and $content.Contains("2s") -and $content.Contains("2p")
$hasIdAtomName = $content.Contains('id="atom-name"')
$hasIdAtomicNumber = $content.Contains('id="atomic-number"')
$hasIdElectronConfig = $content.Contains('id="electron-config"')

Test-Criterion "C10" "DOM contains 'Oxygen'" $hasOxygen "Text 'Oxygen' in element"
Test-Criterion "C10" "DOM contains atomic number '8'" $hasAtomicNum8 "Text '8' in element"
Test-Criterion "C10" "DOM contains electron configuration" $hasConfig "1s, 2s, 2p strings present"
Test-Criterion "C10" "Info panel has proper IDs for testing" ($hasIdAtomName -and $hasIdAtomicNumber -and $hasIdElectronConfig) "atom-name, atomic-number, electron-config IDs"

# --- FILE SIZE CHECK ---
Write-Host ""
Write-Host "[CONSTRAINT] File size:" -ForegroundColor Yellow
$fileSize = (Get-Item $indexPath).Length
$fileSizeKB = [math]::Round($fileSize / 1024, 1)
Test-Criterion "SIZE" "Total file size under 50KB" ($fileSize -lt 51200) "index.html: ${fileSizeKB}KB ($fileSize bytes)"

# --- SUMMARY ---
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
if ($failed -eq 0) {
    Write-Host "  ALL $total TESTS PASSED" -ForegroundColor Green
} else {
    Write-Host "  $passed/$total PASSED, $failed FAILED" -ForegroundColor Red
}
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

exit $failed
