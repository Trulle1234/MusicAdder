from templates import templates, templates_single_file
from file_name_templates import file_name_templates
import os
import re

# Optional: install mutagen via pip (pip install mutagen)
from mutagen.oggvorbis import OggVorbis

def get_ogg_length(path):
    """
    Return the duration in seconds (float) of an OGG file.
    """
    audio = OggVorbis(path)
    return audio.info.length

def replace_placeholders(template, values):
    """
    Replace only the keys in 'values' dict wrapped in {key} within the template string.
    """
    keys = [re.escape(k) for k in values.keys()]
    # Match exactly {key}
    pattern = re.compile(r"\{(" + "|".join(keys) + r")\}")
    return pattern.sub(lambda m: str(values[m.group(1)]), template)

def names_from_midis(path):
    """
    Extract base filenames (without extension) from all files in a folder.
    """
    files = os.listdir(path)
    return [os.path.splitext(f)[0] for f in files if os.path.isfile(os.path.join(path, f))]

def template_name_adder_list_file(file_name, name_list, template):
    """
    Write a single text file by concatenating formatted templates for each name.
    """
    content = "".join(
        replace_placeholders(template, {
            'name': n.lower(),
            'name_first_capital': n.capitalize(),
            'name_capital': n.upper()
        }) for n in name_list
    )
    with open(f"{file_name}.txt", 'w', encoding='utf-8') as f:
        f.write(content)

def generate_json_files(name_list, json_template, fname_tpl, output_folder, ogg_folder=None):
    """
    For each name, compute ogg length (if ogg_folder given), set comparator_output_int,
    format the JSON template, and write a .json file using the given filename template.
    """
    os.makedirs(output_folder, exist_ok=True)

    for name in name_list:
        placeholders = {
            'name': name.lower(),
            'name_first_capital': name.capitalize(),
            'name_capital': name.upper()
        }
        # If OGG folder provided, compute lengths
        if ogg_folder:
            ogg_path = os.path.join(ogg_folder, f"{name}.ogg")
            length_sec = get_ogg_length(ogg_path)
            placeholders['length_in_seconds_float'] = length_sec
            placeholders['comparator_output_int'] = int(length_sec)

        # Generate JSON content
        json_content = replace_placeholders(json_template, placeholders)

        # Determine output filename and write
        fname = replace_placeholders(fname_tpl, placeholders)
        path = os.path.join(output_folder, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json_content)

if __name__ == "__main__":
    # Paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    midi_dir = r"C:\Anthem_Discs\anthem-discs-fabric-1.21.2\anthems\europe_anthems"
    ogg_folder = os.path.join(project_dir, 'output_oggs')
    output_folder = os.path.join(project_dir, 'generated_jsons')

    # Prepare names
    names = names_from_midis(midi_dir)

    # Write a concatenated text file for each template
    text_file_names = ["ModItems", "ModSounds", "en_us", "sounds", "ModItemGroups"]
    for file_name, tpl in zip(text_file_names, templates):
        template_name_adder_list_file(file_name, names, tpl)

    # Generate JSONs: pair each JSON template with its filename template
    for idx, json_tpl in enumerate(templates_single_file):
        # pick matching filename template if exists, else use first
        if idx < len(file_name_templates):
            fname_tpl = file_name_templates[idx]
        else:
            fname_tpl = file_name_templates[0]
        # For the first template (idx 0), no OGG length
        if idx == 0:
            generate_json_files(names, json_tpl, fname_tpl, output_folder)
        else:
            generate_json_files(names, json_tpl, fname_tpl, output_folder, ogg_folder)

    print(f"JSON files written to: {output_folder}")
