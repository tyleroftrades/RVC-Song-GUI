# RVC-Song-GUI
A simple gui to make inferring songs with RVC faster.

I ain't good at coding this pasted together with elmers glue, but it gets the job done for me. Its a gui to be able to use a youtube url to download the sound split it and then infer it and remerge. To output an infered song with the model you choose. It stores the downloaded & split audio tracks, this is because that part seems to be the longest point of the code. 


# To Setup
A fair amount of the dependincies in here are not well maintained by others. First you must get 3.11.6. I would suggest getting this exact one(I think there is play room, however there are applications in here that rely on it being both old, and new. I think 3.11 is your biggest playroom with versions). 

Download the repo as a zip and extract into the C: drive. I am not motivated nor educated enough to be able to get this thing to work with whatever directory it's placed in as I'm far to lazy right now as well. So there's a lot of hardcoded paths.
use the requirements.txt to install the dependincies(There may be some files that aren't needed, I just don't know how to refine it).

This is the biggest point of error. it's pytorch not installing the correct file, and just can causes issues. It tends to not install the gpu version which conflicts with the UVR splitter as thats set to use the gpu, you can change this if you can't get it to work. It should be in the AutoInfer.py file in the spliting part?

Next Download RVC from the rvc github https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/releases I highly suggest installing it via the releases as it tends to just work more often. 

Take all those files from inside the rvc zip and put it into the rvc folder in AI Stuff

Now take your models and put them in the Models folder. each model should be in its own folder, and the .pth file should be renamed to be the name of the model as thats whats used to generate the file & folder names(no, I don't know why I didn't use the folder of the model for that)

Note: The program WILL look like it's not responding. And you WILL be asked to close it by windows. But this is because the program is downloading the song via the youtube url provided, this is the longest point in time and can take a good few secs. Once it downloads the sound, it will then start to infer it to which a cmd prompt should prompt up of RVC.
