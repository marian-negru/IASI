apt install ffmpeg
apt-get install llvm-7 llvm-7-dev
export LLVM_CONFIG=/usr/bin/llvm-config-7
cd /usr/bin
ln -s llvm-config-7 llvm-config
apt-get install libportaudio2
pip3 install -r requirements.txt

