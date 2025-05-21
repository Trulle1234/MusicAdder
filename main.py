from templates import templates, templates_single_file

import os

def template_name_adder(name, template):
    name_dict = {
        'name': name.lower(),
        'name_first_capital': name.capitalize(),
        'name_capital':       name.upper(),
    }
    return template.format(**name_dict)

def template_name_adder_list(name_list, template):
    file_file = ""
    for name in name_list:
        file_file += template_name_adder(name, template)
    return file_file

def names_from_midis(path):
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(os.path.join(path, f))]
    no_extension = []
    for file in files:
        name_only, ext = os.path.splitext(file)
        no_extension.append(name_only)
    return no_extension

def template_name_adder_list_file(file_name, name_list, template):
    file_content = template_name_adder_list(name_list, template)
    with open(file_name + ".txt", 'w', encoding='utf-8') as f:
        f.write(file_content)



name_list = names_from_midis("C:\\Anthem_Discs\\anthem-discs-fabric-1.21.2\\anthems\\europe_anthems")
template_name_adder_list_file("ModItemsEurope", name_list, templates[0])