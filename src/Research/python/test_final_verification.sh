#!/bin/bash

echo "=========================================="
echo "YouTube Channel Scraper - Final Verification"
echo "=========================================="
echo ""

echo "1. Checking script syntax..."
python -m py_compile youtube_channel_scraper.py
if [ $? -eq 0 ]; then
    echo "   ✅ No syntax errors"
else
    echo "   ❌ Syntax errors found"
    exit 1
fi

echo ""
echo "2. Checking help command..."
python youtube_channel_scraper.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Help command works"
else
    echo "   ❌ Help command failed"
    exit 1
fi

echo ""
echo "3. Verifying new arguments..."
if python youtube_channel_scraper.py --help | grep -q "download-high-views"; then
    echo "   ✅ --download-high-views argument present"
else
    echo "   ❌ --download-high-views argument missing"
    exit 1
fi

if python youtube_channel_scraper.py --help | grep -q "view-threshold"; then
    echo "   ✅ --view-threshold argument present"
else
    echo "   ❌ --view-threshold argument missing"
    exit 1
fi

echo ""
echo "4. Running download feature tests..."
python test_download_feature.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Download feature tests pass (4/4)"
else
    echo "   ❌ Download feature tests failed"
    exit 1
fi

echo ""
echo "5. Running integration tests..."
python test_integration.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Integration tests pass (6/6)"
else
    echo "   ❌ Integration tests failed"
    exit 1
fi

echo ""
echo "6. Checking documentation..."
docs=("DOWNLOAD_FEATURE.md" "UPDATE_SUMMARY.md" "YOUTUBE_SCRAPER_IMPROVEMENTS.md")
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc exists"
    else
        echo "   ❌ $doc missing"
        exit 1
    fi
done

echo ""
echo "=========================================="
echo "✅ All Verifications Passed!"
echo "=========================================="
echo ""
echo "The YouTube Channel Scraper is ready to use:"
echo ""
echo "  Basic usage:"
echo "    python youtube_channel_scraper.py @channel --top 10"
echo ""
echo "  With downloads (10M+ views):"
echo "    python youtube_channel_scraper.py @channel --top 20 --download-high-views"
echo ""
echo "  Custom threshold (5M views):"
echo "    python youtube_channel_scraper.py @channel --download-high-views --view-threshold 5000000"
echo ""
exit 0
