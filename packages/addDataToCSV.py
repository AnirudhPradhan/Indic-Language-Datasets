import csv
from packages.difSpeechLength import compute_actual_speech

csv.field_size_limit(10**7)

def add_transcript_to_metadata(
    video_id, 
    transcript, 
    diarization,
    csv_file
):
    try:
        # Read existing CSV and ensure all required fields
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_fieldnames = reader.fieldnames or []
            # Required fields
            required_fields = [
                'Video ID', 'Title', 'Channel ID', 'Video Duration', 'Actual Speech Duration',
                'Published Date', 'Language', 'AI Training Status', 'Number of Speakers',
                'Speaker Distribution', 'Transcript'
            ]
            # Ensure all required fields are present
            fieldnames = existing_fieldnames.copy()
            for field in required_fields:
                if field not in fieldnames:
                    fieldnames.append(field)
            rows = list(reader)

        updated = False
        for row in rows:
            if row.get('Video ID', '').strip() == video_id.strip():
                # Update existing row
                row['Number of Speakers'] = len(set(diarization.labels()))
                row['Speaker Distribution'] = str(diarization.chart())
                row['Transcript'] = str(transcript)
                row['Actual Speech Duration'] = round(
                    float(compute_actual_speech(str(diarization.chart()))), 2
                )
                updated = True
                break

        if not updated:
            # Create a new row with all required fields
            new_row = {field: '' for field in fieldnames}
            new_row['Video ID'] = video_id
            new_row['Speaker Distribution'] = str(diarization.chart())
            new_row['Number of Speakers'] = len(set(diarization.labels()))
            new_row['Transcript'] = str(transcript)
            new_row['Actual Speech Duration'] = round(
                float(compute_actual_speech(str(diarization.chart()))), 2
            )
            rows.append(new_row)

        # Write updated data back to CSV
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"✅ Updated {csv_file}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
