#!/usr/bin/env python3
"""
Add city names to top 100 risk locations using reverse geocoding.
Uses OpenStreetMap Nominatim API (free, 1 request/second rate limit).
"""

import pandas as pd
import urllib.request
import json
import time
import os

# Configuration
CSV_PATH = '/Users/jeanyi/Documents/Sewer Pipes Project/sso-prediction-model/outputs/model_results.csv'
CACHE_PATH = '/Users/jeanyi/Documents/Sewer Pipes Project/city_cache.json'
TOP_N = 100  # Only geocode top N risk locations

def load_cache():
    """Load cached geocoding results"""
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """Save cache to disk"""
    with open(CACHE_PATH, 'w') as f:
        json.dump(cache, f, indent=2)

def reverse_geocode(lat, lon):
    """Get city/area name from coordinates using Nominatim API"""
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&zoom=14&addressdetails=1"
    headers = {'User-Agent': 'LACountySewerProject/1.0 (educational research)'}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            address = data.get('address', {})

            # Check for incorporated city first
            city = (address.get('city') or
                    address.get('town') or
                    address.get('village'))

            if city:
                return city

            # For unincorporated areas, check for neighborhood/suburb name
            local_name = (address.get('suburb') or
                         address.get('neighbourhood') or
                         address.get('hamlet') or
                         address.get('locality'))

            if local_name:
                return f"{local_name} (Unincorporated)"

            # Fallback to county-level
            county = address.get('county', '')
            if 'Los Angeles' in county:
                return "Los Angeles County (Unincorporated)"

            return county if county else ''

    except Exception as e:
        print(f"  Error geocoding {lat},{lon}: {e}")
        return ''

def main():
    print("Loading CSV with risk scores...")
    df = pd.read_csv(CSV_PATH)
    print(f"Total rows: {len(df)}")

    # Add city column if it doesn't exist
    if 'city' not in df.columns:
        df['city'] = ''

    # Get top N by risk score
    df_sorted = df.sort_values('risk_score', ascending=False)
    top_n = df_sorted.head(TOP_N)

    print(f"\nGeocoding top {TOP_N} risk locations...")
    print(f"Risk score range: {top_n['risk_score'].min():.1f} - {top_n['risk_score'].max():.1f}")

    # Load cache
    cache = load_cache()
    print(f"Cached locations: {len(cache)}")

    # Get unique coordinates from top N
    coords = top_n[['latitude', 'longitude']].drop_duplicates().dropna()
    print(f"Unique coordinates in top {TOP_N}: {len(coords)}")

    # Filter out already cached
    to_geocode = []
    for _, row in coords.iterrows():
        key = f"{row['latitude']},{row['longitude']}"
        if key not in cache:
            to_geocode.append((row['latitude'], row['longitude']))

    print(f"New coordinates to geocode: {len(to_geocode)}")

    if len(to_geocode) > 0:
        print(f"\nEstimated time: ~{len(to_geocode)} seconds")
        print("Starting geocoding...\n")

        for i, (lat, lon) in enumerate(to_geocode):
            key = f"{lat},{lon}"
            city = reverse_geocode(lat, lon)
            cache[key] = city
            print(f"  [{i+1}/{len(to_geocode)}] {lat:.4f}, {lon:.4f} → {city}")

            # Save cache every 10 requests
            if (i + 1) % 10 == 0:
                save_cache(cache)

            time.sleep(1.1)  # Rate limit

    # Save final cache
    save_cache(cache)

    # Update city column for ALL rows (using cache)
    print("\nUpdating city column in CSV...")
    def get_city(row):
        if pd.isna(row['latitude']) or pd.isna(row['longitude']):
            return ''
        key = f"{row['latitude']},{row['longitude']}"
        return cache.get(key, '')

    df['city'] = df.apply(get_city, axis=1)

    # Save updated CSV
    print(f"Saving to {CSV_PATH}...")
    df.to_csv(CSV_PATH, index=False)

    # Print summary
    top_cities = df.head(TOP_N)['city'].value_counts()
    print(f"\nDone! Cities in top {TOP_N} risks:")
    print(top_cities.to_string())

if __name__ == '__main__':
    main()
