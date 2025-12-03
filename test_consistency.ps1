# Test script for verifying first-run consistency fixes
# This script helps test that the application returns consistent results across server restarts

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "CONTRACT ANALYSIS CONSISTENCY TEST" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

# Check if keyword cache exists
$cacheFile = "user_memory\keyword_cache\keywords.json"
if (Test-Path $cacheFile) {
    $cacheContent = Get-Content $cacheFile | ConvertFrom-Json
    $cacheSize = ($cacheContent | Get-Member -MemberType NoteProperty).Count
    Write-Host "✓ Keyword cache found: $cacheSize entries" -ForegroundColor Green
    
    Write-Host "`nCache sample (first 3 entries):" -ForegroundColor Yellow
    $cacheContent | Get-Member -MemberType NoteProperty | Select-Object -First 3 | ForEach-Object {
        $key = $_.Name
        $keywords = $cacheContent.$key
        Write-Host "  Hash: $($key.Substring(0, 16))..." -ForegroundColor Gray
        Write-Host "  Keywords: $($keywords -join ', ')" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ No keyword cache found - will be created on first run" -ForegroundColor Yellow
}

Write-Host ""

# Check for old vector stores
$vectorStores = Get-ChildItem "user_memory" -Directory -ErrorAction SilentlyContinue | Where-Object {$_.Name -like "faiss_*"}
if ($vectorStores) {
    Write-Host "⚠ Found $($vectorStores.Count) old vector store(s):" -ForegroundColor Yellow
    $vectorStores | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor Gray
    }
    Write-Host "`nThese should be cleaned up on server startup." -ForegroundColor Yellow
} else {
    Write-Host "✓ No old vector stores found - disk is clean" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "TESTING INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Make sure the server is running:" -ForegroundColor White
Write-Host "   uvicorn backend.main:app --reload" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Run your first analysis through the web interface" -ForegroundColor White
Write-Host "   - Upload your obligations file" -ForegroundColor Gray
Write-Host "   - Upload your contract file" -ForegroundColor Gray
Write-Host "   - Note the results (which obligations are Yes/No)" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Stop the server (Ctrl+C in the terminal)" -ForegroundColor White
Write-Host ""

Write-Host "4. Start the server again:" -ForegroundColor White
Write-Host "   uvicorn backend.main:app --reload" -ForegroundColor Gray
Write-Host ""

Write-Host "5. Run the EXACT SAME analysis again" -ForegroundColor White
Write-Host "   - Use the same obligations file" -ForegroundColor Gray
Write-Host "   - Use the same contract file" -ForegroundColor Gray
Write-Host ""

Write-Host "6. Compare results - they should be IDENTICAL" -ForegroundColor White
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "EXPECTED BEHAVIOR" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "✓ First run and second run should have IDENTICAL results" -ForegroundColor Green
Write-Host "✓ Server logs should show 'Using cached keywords' on second run" -ForegroundColor Green
Write-Host "✓ Old vector stores should be cleaned up on server startup" -ForegroundColor Green
Write-Host "✓ Keyword cache should persist across server restarts" -ForegroundColor Green
Write-Host ""

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "TROUBLESHOOTING" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

Write-Host "If results are still inconsistent:" -ForegroundColor Yellow
Write-Host "1. Check server logs for errors" -ForegroundColor Gray
Write-Host "2. Verify you're using the exact same files" -ForegroundColor Gray
Write-Host "3. Clear the cache and try again:" -ForegroundColor Gray
Write-Host "   Remove-Item -Recurse -Force user_memory\keyword_cache" -ForegroundColor DarkGray
Write-Host "4. Enable DEBUG logging in .env file:" -ForegroundColor Gray
Write-Host "   LOG_LEVEL=DEBUG" -ForegroundColor DarkGray
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
