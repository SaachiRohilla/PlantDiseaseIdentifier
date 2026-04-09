import kaggle
import random
import shutil
kaggle.api.authenticate()
{
  "username": "vivichung01",
  "key": "KGAT_2120327891f44125b4b2799987b9bf85"
}

folder_path = './randomdata'
shutil.rmtree(folder_path, ignore_errors=True)

dataset = 'sujallimje/plant-pathogens'
subsetcount = 3
bacterianums = random.sample(range(1, 35423), subsetcount)
fungusnums = random.sample(range(1, 36076), subsetcount)
healthynums = random.sample(range(1, 35134), subsetcount)
pestsnums = random.sample(range(1, 34790), subsetcount)
virusnums = random.sample(range(1, 35291), subsetcount)
i = 0
# while i < subsetcount: 
#     # print('pathogens/bacteria/bac ('+str(num)+').JPG')  <---------- was to test the numbers
#     try:
#         kaggle.api.dataset_download_file(dataset,'pathogen/bacteria/bac ('+str(bacterianums[i])+').JPG', path='./randomdata')    
#         kaggle.api.dataset_download_file(dataset,'pathogen/fungus/fung ('+str(fungusnums[i])+').JPG', path='./randomdata')
#         kaggle.api.dataset_download_file(dataset,'pathogen/healthy/hea ('+str(healthynums[i])+').JPG', path='./randomdata')
#         kaggle.api.dataset_download_file(dataset,'pathogen/pests/pes ('+str(pestsnums[i])+').JPG', path='./randomdata')
#         kaggle.api.dataset_download_file(dataset,'pathogen/virus/vir ('+str(virusnums[i])+').JPG', path='./randomdata')
#         i+=1
#     except Exception as e:
#         print("bad number!")
#         bacterianums[i] = random.randint(1, 35423)
#         fungusnums[i] = random.randint(1, 36076)
#         healthynums[i] = random.randint(1, 35134)
#         pestsnums[i] = random.randint(1, 34790)
#         virusnums[i] = random.randint(1, 35291)


while i < subsetcount:
    try:
        print('pathogen/bacteria/bac ('+str(bacterianums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/bacteria/bac ('+str(bacterianums[i])+').JPG', path='./randomdata')
        i+=1
    except Exception as e:
        print("bad bac number!")
        bacterianums[i] = random.randint(1, 35423)
i = 0
while i < subsetcount:
    try:
        print('pathogens/fungus/fung ('+str(fungusnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/fungus/fung ('+str(fungusnums[i])+').JPG', path='./randomdata')
        i+=1
    except Exception as e:
        print("bad fun number!")
        fungusnums[i] = random.randint(1, 36076)
i = 0
while i < subsetcount:
    try:
        print('pathogens/healthy/hea ('+str(healthynums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/healthy/hea ('+str(healthynums[i])+').JPG', path='./randomdata')
        i+=1
    except Exception as e:
        print("bad hea number!")
        healthynums[i] = random.randint(1, 35134)
i = 0
while i < subsetcount:
    try:
        print('pathogen/pests/pes ('+str(pestsnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset, 'pathogen/pests/pes ('+str(pestsnums[i])+').JPG', path='./randomdata')
        i+=1
    except Exception as e:
        print("bad pes number!")
        pestsnums[i] = random.randint(1, 34790)
i = 0
while i < subsetcount:
    try:
        print('pathogen/virus/vir ('+str(virusnums[i])+').JPG')
        kaggle.api.dataset_download_file(dataset,'pathogen/virus/vir ('+str(virusnums[i])+').JPG', path='./randomdata')
        i+=1
    except Exception as e:
        print("bad vir number!")
        virusnums[i] = random.randint(1, 35291)