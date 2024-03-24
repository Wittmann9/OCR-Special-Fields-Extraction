# Test-task description

This code presents the solution for automatic extraction of contents in the fiels of interest. The algorithm utilizes given example of inspection certificate. 
It does preprocess inspection certificate and it's example, so the images are aligned. Then it extracts the coordinates of blue boxes with relevant fields from *example*, and crops *inspection certificate* using those coordinates. Each cropped image is then preprocesses and EasyOCR is used to extract the content.


To run this code on Linux machine, use the following comands:

python3 -m venv venv  
pip3 install -r requirements.txt  
apt-get install -y poppler-utils -qq  
python3 main.py --pdf_name Inspection_Certificate --gpu_availability false  


Note_1: use your current python and pip versions  
Note_2: pass the name of inspection certificate without *.pdf*  
