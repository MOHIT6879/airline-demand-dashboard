import pandas as pd


def process_flight_data(data):
    flights = data.get("data", [])

    df = pd.DataFrame([{
        'flight_date': f.get('flight_date'),
        'flight_status': f.get('flight_status'),
        'airline': f.get('airline', {}).get('name'),
        'flight_number': f.get('flight', {}).get('number'),
        'from': f.get('departure', {}).get('airport'),
        'from_iata': f.get('departure', {}).get('iata'),
        'to': f.get('arrival', {}).get('airport'),
        'to_iata': f.get('arrival', {}).get('iata'),
        'departure_time': f.get('departure', {}).get('scheduled'),
        'arrival_time': f.get('arrival', {}).get('scheduled'),
    } for f in flights])

    # Convert time columns
    df['departure_time'] = pd.to_datetime(df['departure_time'], errors='coerce')
    df['arrival_time'] = pd.to_datetime(df['arrival_time'], errors='coerce')

    # Drop if key info is missing
    df = df.dropna(subset=['departure_time', 'from', 'to', 'airline'])

    # Remove timezone awareness
    df['departure_time'] = df['departure_time'].dt.tz_localize(None)
    df['arrival_time'] = df['arrival_time'].dt.tz_localize(None)

    return df



def apply_filters(df, selected_airlines, selected_routes):
    if selected_airlines:
        df = df[df['airline'].isin(selected_airlines)]

    if selected_routes:
        df = df[df[['from', 'to']].apply(lambda row: f"{row['from']} → {row['to']}" in selected_routes, axis=1)]

    return df
