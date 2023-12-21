
cd "C:\AI Stuff\RVC"

runtime\python.exe infer-embed.py --pycmd runtime\python.exe --input_path %1 --model_name %2 --index_path %3 --octave %4
