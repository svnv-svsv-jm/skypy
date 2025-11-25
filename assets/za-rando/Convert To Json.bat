@echo off
title Flatbuffers BIN Converter v2.1
echo " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
echo " ______ _       _   _            __  __                "
echo " |  ___| |     | | | |          / _|/ _|               "
echo " | |_  | | __ _| |_| |__  _   _| |_| |_ ___ _ __ ___   "
echo " |  _| | |/ _\`| __| '_ \| | | |  _|  _/ _ \ '__/ __|  "
echo " | |   | | (_| | |_| |_) | |_| | | | ||  __/ |  \__ \  "
echo " \_|   |_|\__,_|\__|_.__/ \__,_|_| |_| \___|_|  |___/  "
echo " ______ _____ _   _                                    "
echo " | ___ \_   _| \ | |                                   "
echo " | |_/ / | | |  \| |                                   "
echo " | ___ \ | | | . \ |                                   "
echo " | |_/ /_| |_| |\  |                                   "
echo " \____/ \___/\_| \_/                                   "
echo "  _____                           _                    "
echo " /  __ \                         | |                   "
echo " | /  \/ ___  _ ____   _____ _ __| |_ ___ _ __         "
echo " | |    / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|        "
echo " | \__/\ (_) | | | \ V /  __/ |  | ||  __/ |           "
echo "  \____/\___/|_| |_|\_/ \___|_|   \__\___|_|           "
echo "                                                       "
echo " By duckdoom5 & Inidar                                 "
echo "                                                       "
echo "                                                       "
echo " For support, find us on Discord:                      "
echo " https://discord.gg/bCkhsSdwSY                         "
echo "                                                       "
echo " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
echo:
echo:


setlocal enabledelayedexpansion
set "SchemaExt=.bfbs .fbs"
set "InputExt=.bin"
set "OutputExt=.json"
set "InputPath=Input/"
set "OutputPath=Output/"
set "OutputType=-t"

set "Red=[91m"
set "Yellow=[93m"
set "White=[0m"

:: Set this to true to always overwrite the file
set "overwriteAll="

:f_main
:: Create the output folder if it doesn't exist
if not exist "%OutputPath%" ( mkdir "%OutputPath%" )

call :f_checkFlatcExists

:: Run code for all BIN files in 'Input/'
echo Looking for %InputExt% files in '%InputPath%'...

set "filesFound="
for %%l in (%InputPath%*%InputExt%) do (
    set "filesFound=true"

    :: Check if a .bfbs is present in the input folder with the same name
    if exist %InputPath%%%~nl.bfbs (
        :: Check if the file should be converted
        call :f_shouldConvert %%l

        if errorlevel 1 (
            call :f_convertFile %%l
        ) else (
            echo Skipping convertion for '%%l%'...
        )
    ) else (
        echo %Red%Couldn't find '%InputPath%%%~nl.bfbs'. This file is required to convert '%InputPath%%%l'.%White%
    )
)

if not defined filesFound (
    echo %Red%Couldn't find any %InputExt% files in '%InputPath%'...%White%
)

goto atExit

:: Checks if output file already exists and prompts the user if it does
:f_shouldConvert
if defined overwriteAll ( exit /B 1 )

if exist %OutputPath%%~n1%OutputExt% (
    echo.
    echo %Yellow%The file '%OutputPath%%~n1%OutputExt%' already exists^^!%White%
    choice /C YNA /M "Would you like to overwrite the file? (Yes)/(No)/(Yes to All)"
    echo.

    if errorlevel 3 (
        set "overwriteAll=true"
        exit /B 1
    )
    if errorlevel 2 ( exit /B 0 )
)
exit /B 1

:f_convertFile
echo Converting '%1'...
:: Run flatc converter
flatc.exe -o %OutputPath% %OutputType% --raw-binary --defaults-json --strict-json "%InputPath%%~n1.bfbs" -- "%InputPath%%1"
GOTO :eof

:: Check if flatc.exe is next to the batch script
:f_checkFlatcExists
if not exist flatc.exe (
    echo %Red%'flatc.exe' should be in the same folder as this script file%White%
    goto atExit
)
GOTO :eof

:atExit
echo.
echo Finished converting files^^!
:: 'pause' will keep the cmd window open until the user presses any key
pause
