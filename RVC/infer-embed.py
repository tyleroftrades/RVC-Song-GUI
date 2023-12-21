import os
import sys
now_dir = os.getcwd()
sys.path.append(now_dir)
from dotenv import load_dotenv



from infer.modules.vc.modules import VC

from infer.modules.uvr5.modules import uvr

from infer.lib.train.process_ckpt import (
    change_info,
    extract_small_model,
    merge,
    show_info,
)

from i18n.i18n import I18nAuto
from configs.config import Config
import torch
import numpy as np
import gradio as gr
import fairseq
from time import sleep
import warnings
import shutil
import logging
from scipy.io import wavfile




logging.getLogger("numba").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

tmp = os.path.join(now_dir, "TEMP")
shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/infer_pack" % (now_dir), ignore_errors=True)
shutil.rmtree("%s/runtime/Lib/site-packages/uvr5_pack" % (now_dir), ignore_errors=True)
os.makedirs(tmp, exist_ok=True)
os.makedirs(os.path.join(now_dir, "logs"), exist_ok=True)
os.makedirs(os.path.join(now_dir, "assets/weights"), exist_ok=True)
os.environ["TEMP"] = tmp
warnings.filterwarnings("ignore")
torch.manual_seed(114514)

load_dotenv()
config = Config()
vc = VC(config)



if config.dml == True:

    def forward_dml(ctx, x, scale):
        ctx.scale = scale
        res = x.clone().detach()
        return res

    fairseq.modules.grad_multiply.GradMultiply.forward = forward_dml
i18n = I18nAuto()
logger.info(i18n)
# 判断是否有能用来训练和加速推理的N卡
ngpu = torch.cuda.device_count()
gpu_infos = []
mem = []
if_gpu_ok = False

if torch.cuda.is_available() or ngpu != 0:
    for i in range(ngpu):
        gpu_name = torch.cuda.get_device_name(i)
        if any(
            value in gpu_name.upper()
            for value in [
                "10",
                "16",
                "20",
                "30",
                "40",
                "A2",
                "A3",
                "A4",
                "P4",
                "A50",
                "500",
                "A60",
                "70",
                "80",
                "90",
                "M4",
                "T4",
                "TITAN",
            ]
        ):
            # A10#A100#V100#A40#P40#M40#K80#A4500
            if_gpu_ok = True  # 至少有一张能用的N卡
            gpu_infos.append("%s\t%s" % (i, gpu_name))
            mem.append(
                int(
                    torch.cuda.get_device_properties(i).total_memory
                    / 1024
                    / 1024
                    / 1024
                    + 0.4
                )
            )
if if_gpu_ok and len(gpu_infos) > 0:
    gpu_info = "\n".join(gpu_infos)
    default_batch_size = min(mem) // 2
else:
    gpu_info = i18n("很遗憾您这没有能用的显卡来支持您训练")
    default_batch_size = 1
gpus = "-".join([i[0] for i in gpu_infos])





model_path = sys.argv[6]



vc.get_vc(model_path)

sid0 = 0#Model Dropdown(Path to module?)
#clean_button.click(
#    fn=clean, inputs=[], outputs=[sid0], api_name="infer_clean"

spk_item = 0#Unkown Not visible
#minimum=0,
#maximum=2333,
#step=1,
#label=i18n("请选择说话人id"),
#value=0,
#visible=False,

vc_transform0 = sys.argv[10]#Octave Change
#value=0

input_audio0 = sys.argv[4]#Path to Audio file to be infered upon
#placeholder="C:\\Users\\Desktop\\audio_example.wav"

file_index1 = sys.argv[8]#Path to index file of model
#placeholder="C:\\Users\\Desktop\\model_example.index",

file_index2 = None#Index Dropdown
#choices=sorted(index_paths),

f0method0 = "rmvpe"#Algrorith choice. PM, Harvest, Crepe, Rmvpe
#choices=["pm", "harvest", "crepe", "rmvpe"]
#if config.dml == False
#else ["pm", "harvest", "rmvpe"],
#value="rmvpe",

resample_sr0 = 0# Resample the output audio in post-processing to the final sample rate. Set to 0 for no resampling:
#minimum=0,
#maximum=48000,
#value=0,
#step=1,

rms_mix_rate0 = 0.25# Adjust the volume envelope scaling. Closer to 0, the more it mimicks the volume of the original vocals. Can help mask noise and make volume sound more natural when set relatively low. Closer to 1 will be more of a consistently loud volume:
#minimum=0,
#maximum=1,
#value=0.25,

protect0 = 0.33#Protect voiceless consonants and breath sounds to prevent artifacts such as tearing in electronic music. Set to 0.5 to disable. Decrease the value to increase protection, but it may reduce indexing accuracy:
#minimum=0,
#maximum=0.5,
#value=0.33,
#step=0.01,

filter_radius0 = 3#If >=3: apply median filtering to the harvested pitch results. The value represents the filter radius and can reduce breathiness.
#minimum=0,
#maximum=7,
#value=3,
#step=1,
index_rate1 = 0.75#Search feature ratio (controls accent strength, too high has artifacting):
#minimum=0,
#maximum=1,
#value=0.75,

f0_file = None#Unkown Not Visible
#visible=False

#vc_output1 = gr.Textbox(label=i18n("输出信息"))
#vc_output2 = gr.Audio(label=i18n("输出音频(右下角三个点,点了可以下载)"))



_, wav_opt = vc.vc_single(
    spk_item,
    input_audio0,
    vc_transform0,
    f0_file,
    f0method0,
    file_index1,
    file_index2,
    # file_big_npy1,
    index_rate1,
    filter_radius0,
    resample_sr0,
    rms_mix_rate0,
    protect0)

opt_path = "C:\AI Stuff\Scripts\InferedVocals.wav"


wavfile.write(opt_path, wav_opt[0], wav_opt[1])







   
"""



                sid0 = #Model Dropdown(Path to module?)
                    choices=sorted(names))  
                    
                clean_button.click(
                    fn=clean, inputs=[], outputs=[sid0], api_name="infer_clean"
                )
                            vc_transform0 = gr.Number( #Octave Change
                                value=0
                                
                            input_audio0 = #Path to Audio file to be infered upon
                                placeholder="C:\\Users\\Desktop\\audio_example.wav"
                                
                            file_index1 = #Path to index file of model
                                placeholder="C:\\Users\\Desktop\\model_example.index",

                            file_index2 #Index Dropdown
                                choices=sorted(index_paths),
                                
                            f0method0 = #Algrorith choice. PM, Harvest, Crepe, Rmvpe
                                choices=["pm", "harvest", "crepe", "rmvpe"]
                                if config.dml == False
                                else ["pm", "harvest", "rmvpe"],
                                value="rmvpe",

                            resample_sr0 = # Resample the output audio in post-processing to the final sample rate. Set to 0 for no resampling:
                                minimum=0,
                                maximum=48000,
                                value=0,
                                step=1,

                            rms_mix_rate0 = # Adjust the volume envelope scaling. Closer to 0, the more it mimicks the volume of the original vocals. Can help mask noise and make volume sound more natural when set relatively low. Closer to 1 will be more of a consistently loud volume:
                                minimum=0,
                                maximum=1,
                                value=0.25,

                            protect0 = #Protect voiceless consonants and breath sounds to prevent artifacts such as tearing in electronic music. Set to 0.5 to disable. Decrease the value to increase protection, but it may reduce indexing accuracy:
                                minimum=0,
                                maximum=0.5,
                                value=0.33,
                                step=0.01,

                            filter_radius0 = #If >=3: apply median filtering to the harvested pitch results. The value represents the filter radius and can reduce breathiness.
                                minimum=0,
                                maximum=7,
                                value=3,
                                step=1,
                            index_rate1 = #Search feature ratio (controls accent strength, too high has artifacting):
                                minimum=0,
                                maximum=1,
                                value=0.75,

                            
                            
                            

                            vc_output1 = gr.Textbox(label=i18n("输出信息"))
                            vc_output2 = gr.Audio(label=i18n("输出音频(右下角三个点,点了可以下载)"))

                        but0.click(
                            vc.vc_single,
                            [
                                spk_item,
                                input_audio0,
                                vc_transform0,
                                f0_file,
                                f0method0,
                                file_index1,
                                file_index2,
                                # file_big_npy1,
                                index_rate1,
                                filter_radius0,
                                resample_sr0,
                                rms_mix_rate0,
                                protect0,
                            ],
                            [vc_output1, vc_output2],
                            api_name="infer_convert",
                        )
                        
"""
