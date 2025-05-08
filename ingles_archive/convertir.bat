@echo off
for %%f in (*.wav) do (
    ffmpeg -i "%%f" -vn -acodec libmp3lame -ab 192k "%%~nf.mp3"
)
echo Conversión finalizada.
pause
