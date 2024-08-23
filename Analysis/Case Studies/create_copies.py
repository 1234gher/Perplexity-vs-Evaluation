import os
import shutil

copy_names = 'Malayalam, Kannada, Nepali, Gujarati, Hindi, Arabic, Ukrainian,  Basque, French, Vietnamese, English, Russian, Serbian, Slovak'
copy_names = copy_names.split(', ')
copy_names = [x.strip() for x in copy_names]

base = 'English.ipynb'

for name in copy_names:
    if name == 'English':
        continue
    new_name = name + '.ipynb'
    shutil.copy(base, new_name)
    print(f'Copied {base} to {new_name}')