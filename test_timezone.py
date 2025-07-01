#!/usr/bin/env python
"""
Test script to verify Manila timezone functionality
"""
import os
import sys
import django
from datetime import datetime
import pytz

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AttendanceScanner.settings')
django.setup()

from django.utils import timezone
from scanner.views import get_manila_now, get_manila_today, get_manila_time, MANILA_TZ

def test_timezone():
    """Test timezone functionality"""
    print("=== Manila Timezone Test ===")
    
    # Test utility functions
    manila_now = get_manila_now()
    manila_today = get_manila_today()
    manila_time = get_manila_time()
    
    print(f"Manila Now: {manila_now}")
    print(f"Manila Today: {manila_today}")
    print(f"Manila Time: {manila_time}")
    print(f"Manila Timezone: {manila_now.tzinfo}")
    
    # Test UTC vs Manila
    utc_now = timezone.now()
    print(f"\nUTC Now: {utc_now}")
    print(f"UTC to Manila: {utc_now.astimezone(MANILA_TZ)}")
    
    # Test timezone offset
    offset = manila_now.utcoffset()
    print(f"\nManila UTC Offset: {offset}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_timezone() 