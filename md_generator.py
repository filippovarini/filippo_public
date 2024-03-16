#%%
import pandas as pd
import humanfriendly

header_text = """
# Datasets with annotated fish in marine/freshwater imagery/video

## TOC

* <a href="#overview">Overview</a>
* <a href="#publicly-available-datasets">Publicly available datasets</a>

## Overview

This is a list of datasets with annotated marine/freshwater imagery, suitable for training fish detectors/classifiers. 

It was ideated by [Dan Morris](https://dmorris.net) to emulate the [list of datasets with annotated wildlife in drone/aerial images](https://github.com/agentmorris/agentmorrispublic/blob/main/drone-datasets.md), with standardized metadata for each dataset, and consistent sample code for match annotations to images and rendering sample images.


This list was curated by the following folks:
* <a href="https://www.linkedin.com/in/filippo-varini/">Filippo Varini</a>
* <a href="https://dmorris.net">Dan Morris</a>



Email <a href="mailto:fppvrn@gmail.com">Filippo</a> if anything seems off, or if you know of datasets we're missing.


## Publicly available datasets
"""


#%%
input_file = './downloads/fish_datasets.csv'
output_file = 'fish-datasets.md'

df = pd.read_csv(input_file)

output_lines = []

starting_header_level = '###'

def optional_line(row, title):
    s = '* {}:'.format(title)
    if isinstance(row[title],str):
        s += ' ' + row[title] + '\n'
    else:
        s += '  N/A\n'
    return s

# i_row = 0; row = df.iloc[i_row]
for i_row,row in df.iterrows():
    
    # Ignore everything below this
    s = ''
    s += starting_header_level + ' ' + row['Name'] + '\n\n'
    
    s += row['Short description'] + '\n'
     
    s += '  \n'
    
    if isinstance(row['Citation'],str):
        s += row['Citation'] + '\n\n'
        
    size_string = 'Data'
    if isinstance(row['Size in GB'],str):
        size_bytes = 1000*1000*1000*float(row['Size in GB'])
        size_string = '{},'.format(humanfriendly.format_size(size_bytes))

    download_mechanism_str = ''
    if isinstance(row['Download mechanism'],str):
        download_mechanism_str = 'via {}'.format(row['Download mechanism'])

    s += '* {} downloadable via {} from {} (<a href="{}">download link</a>)\n'.format(
        size_string, download_mechanism_str, row['Hosting site'], row['URL'])
    
    
    if isinstance(row['License'],str):
        s += '* License: {}\n'.format(row['License'])

    s += optional_line(row,'Metadata raw format')
    s += optional_line(row, 'Categories/species')
    s += optional_line(row, 'Vehicle type')

    image_addendum = ''
    if isinstance(row['Image notes'],str):
        note = row['Image notes']
        note = note[0].lower() + note[1:]
        image_addendum = ' (' + note + ')'
        
    s += '* Image information: {} {} images{}\n'.format(row['Number of images or videos'],row['Channels'],image_addendum)
    
    ann_number_string = ''
    try:
        n = int(row['Number of annotations'])
        ann_number_string = str(n) + ' '
    except Exception as e:
            pass
        
    s += '* Annotation information: {} {}\n'.format(ann_number_string,row['Annotation type'])
    s += optional_line(row, 'Typical animal size in pixels')
    
    image_url = row['Image URL']
    if isinstance(row['Shortname'],str):
        code_url = f'./data_preview/visualise_{row["Shortname"]}'
        code_link_name = code_url.split('/')[-1]
        image_url = f'./data_preview/{row["Shortname"]}_sample_image.png'
        
        s += '* Code to render sample annotated image: <a href="{}">{}</a>\n'.format(
            code_url,code_link_name)
    
    s += '  \n'
    s += '  \n'
    
    s += '<img src="{}" width=700>\n'.format(image_url)
    
    s += '  \n'
    s += '  \n'
    
    output_lines.append(s)

with open(output_file,'w') as f:
    f.write(header_text)
    for s in output_lines:
        f.write(s)
        
# %%
