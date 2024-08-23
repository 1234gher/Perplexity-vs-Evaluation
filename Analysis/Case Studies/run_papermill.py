import papermill as pm

copy_names = 'Malayalam, Kannada, Nepali, Gujarati, Hindi, Arabic, Ukrainian,  Basque, French, Vietnamese, English, Russian, Serbian, Slovak'
copy_names = copy_names.split(', ')
copy_names = [x.strip() for x in copy_names]

base = 'English.ipynb'

for name in copy_names:
    pm.execute_notebook(
    base,
    f'{name}.ipynb',
    parameters = dict(LANGUAGE=name)
    )