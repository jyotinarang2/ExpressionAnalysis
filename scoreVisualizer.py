from audioOperations import *

'''fff ---- louder than ff.
ff ----- fortissimo ------ louder than f.
f ------ forte -------------- loudly.
mf --- mezzo-forte ------ moderately loud.
mp -- mezzo-piano ----- moderately soft.
p ----- piano -------------- softly.
pp --- pianissimo ------ softer than p.
ppp - softer than pp.'''
def convert_label_to_integer(label):
    if label=='ppp':
        return 1
    elif label=='pp':
        return 2
    elif label=='p':
        return 3
    elif label=='mp':
        return 4
    elif label=='mf':
        return 5
    elif label=='f':
        return 6
    elif label=='ff':
        return 7
    else:
        return 8

def convert_score_data_to_csv(score_path, output_file_path, offset_start):
    import IPython.display as ipd
    xml_data = converter.parse(score_path)
    xml_list = xml_to_list(xml_data, offset_start)
    
    df = pd.DataFrame(xml_list, columns=['measure_number', 'beat_number', 'Start', 'End', 'Pitch', 'Velocity', 'start_time', 'duration_time', 'pitch_frequency'])
    df['Start'] = df['Start'].astype(float)
    df.to_csv(output_file_path, index=False)
    return df, xml_list

def csv_to_list(csv):
    """Convert a csv score file to a list of note events

    Notebook: C1/C1S2_CSV.ipynb

    Args:
        csv: Either a path to a csv file or a data frame

    Returns:
        score: A list of note events where each note is specified as 
        [start, duration, pitch, velocity, label]
    """

    if isinstance(csv, str):
        df = read_csv(csv)
    elif isinstance(csv, pd.DataFrame):
        df = csv
    else:
        raise RuntimeError('csv must be a path to a csv file or pd.DataFrame')

    score = []
    for i, (measure_number, beatNumber, start, end, pitch, velocity, start_time, duration_time, pitch_frequency) in df.iterrows():
        score.append([measure_number, beatNumber, start, end, pitch, velocity, start_time, duration_time, pitch_frequency])
    return score

# Read data from the score
def xml_to_list(xml_data, offset_start= 0):
    
    xml_list = []
    scoreParts = xml_data.parts.stream()
    vocal_part = scoreParts[0]
    mm = vocal_part.getElementsByClass('Measure').stream()
#     measures = vocal_part.getElementsByClass('Measure').stream()
    bpm = mm[0].getElementsByClass(tempo.MetronomeMark).stream()[0].number
    for note in vocal_part.flat.notes:
        measureNumber = note.measureNumber
        beatNumber = note.beat
        start = note.offset
        start_time = start*60.0/bpm
        duration = note.quarterLength
        duration_time = duration*60/bpm
        if note.isChord:
            pitch = note.pitches[0].ps
        else:
            pitch = note.pitch.ps
        pitch_frequency = 440*np.power(2, (pitch-69)/12)
        volume = note.volume.realized
        xml_list.append([measureNumber, beatNumber, start, duration, pitch, volume, start_time, duration_time, pitch_frequency])
                
    #xml_list = sorted(xml_list, key=lambda x: (x[0], x[2]))
    return xml_list

def change_intermediate_dynamics_values(dynamics_contour):
    for position in range(len(dynamics_contour)):
        if dynamics_contour[position] > 0:
            pos = position
            new_pos = pos+1
            while new_pos<len(dynamics_contour) and dynamics_contour[new_pos] == 0:
                dynamics_contour[new_pos] = dynamics_contour[pos]
                new_pos += 1
                position += 1
    return dynamics_contour

