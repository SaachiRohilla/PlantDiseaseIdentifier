import kaggle
import random
import shutil
import os
kaggle.api.authenticate()
{
  "username": "vivichung01",
  "key": "KGAT_2120327891f44125b4b2799987b9bf85"
}

# folder_path = os.path.join(os.path.dirname(__file__), '..', 'randomdata')
# shutil.rmtree(folder_path, ignore_errors=True)

dataset = 'sujallimje/plant-pathogens'
subsetcount = 3000 # <----------------- CHANGE THIS IF YOU WANT MORE DATA; DO NOT TOUCH ANYTHING ELSE
bacterianums = random.sample(range(1, 35423), subsetcount)
fungusnums = random.sample(range(1, 36076), subsetcount)
healthynums = random.sample(range(1, 35134), subsetcount)
pestsnums = random.sample(range(1, 34790), subsetcount)
virusnums = random.sample(range(1, 35291), subsetcount)
i = 0
while i < subsetcount:
    try:
        # print('pathogen/bacteria/bac ('+str(bacterianums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/bacteria/bac ('+str(bacterianums[i])+').JPG', path='./randomdata/bac')
        i+=1
    except Exception as e:
        # print("bad bac number!")
        bacterianums[i] = random.randint(1, 35423)
i = 0
while i < subsetcount:
    try:
        # print('pathogens/fungus/fung ('+str(fungusnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/fungus/fung ('+str(fungusnums[i])+').JPG', path='./randomdata/fung')
        i+=1
    except Exception as e:
        # print("bad fun number!")
        fungusnums[i] = random.randint(1, 36076)
i = 0
while i < subsetcount:
    try:
        # print('pathogens/healthy/hea ('+str(healthynums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/healthy/hea ('+str(healthynums[i])+').JPG', path='./randomdata/hea')
        i+=1
    except Exception as e:
        # print("bad hea number!")
        healthynums[i] = random.randint(1, 35134)
i = 0
while i < subsetcount:
    try:
        # print('pathogen/pests/pes ('+str(pestsnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset, 'pathogen/pests/pes ('+str(pestsnums[i])+').JPG', path='./randomdata/pes')
        i+=1
    except Exception as e:
        # print("bad pes number!")
        pestsnums[i] = random.randint(1, 34790)
i = 0
while i < subsetcount:
    try:
        #print('pathogen/virus/vir ('+str(virusnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/virus/vir ('+str(virusnums[i])+').JPG', path='./randomdata/vir')
        i+=1
    except Exception as e:
        #print("bad vir number!")
        virusnums[i] = random.randint(1, 35291)