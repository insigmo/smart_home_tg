portaudio_path='portaudio.tgz'


sudo apt-get install libasound-dev

# from http://files.portaudio.com/download.html
curl 'http://files.portaudio.com/archives/pa_stable_v190700_20210406.tgz' --output $portaudio_path
tar -zxvf $portaudio_path
cd portaudio && ./configure --enable-optimization && make -j 20 && sudo make install && cd ..
rm $portaudio_path
rm -r portaudio/

pip install -r requirements.txt
