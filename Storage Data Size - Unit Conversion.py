# Umwandlung von Maßeinheiten für Speicherdaten, mit verschiedenen Präfixen'
# Technical Details: https://www.ibm.com/docs/en/storage-insights?topic=overview-units-measurement-storage-data
# 2023 (c) Martin Ramsner, released under MIT License

# Code Spell Checker Settings
# cSpell:locale de-DE, en-GB

# Import library
import locale 
import os 
import sys

# Zahlenformate auf Deutsch
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

# Initialisierung von Variablen
originPrefix = str()
originBinaryValue = float()
NeueBerechnung = str()

# Mögliche binäre Units und deren Umrechnungswert in aufsteigender rEIHENFOLGE
unitFactors = {'PB': 5, 'TB': 4, 'GB': 3, 'MB': 2, 'KB': 1, 'B': 0}

# Function to return a user friendly name of the operating system
# @param tests Explanation
def get_platform():
# Source: https://www.webucator.com/article/how-to-check-the-operating-system-with-python/
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    
    return platforms[sys.platform]

# Umwandlung der Eingabe auf die Größenordnung Byte
def toBytes(binaryValue: float, BinaryUnit: unitFactors) -> int:
    return binaryValue * 1024**(unitFactors[BinaryUnit])

# Umwandlung eines Wertes in eine beliebige Binäre Einheit
def toBinaryWithPrefix(binaryValue: float, originBinaryUnit: unitFactors, targetBinaryUnit: unitFactors) -> float:
    return toBytes(binaryValue, originBinaryUnit) / 1024**(unitFactors[targetBinaryUnit])

# Umwandlung eines Wertes in lesbare Ganzzahlige Binäre Werte
def toReadablePrefixedInteger(binaryValue: float, originBinaryUnit: unitFactors) -> dict:
    resultBinaryIntegers = unitFactors.copy()

    binaryByteValue = toBytes(binaryValue, originBinaryUnit)
    for key, value in unitFactors.items():
        resultBinaryIntegers[key] = binaryByteValue // 1024**value
        binaryByteValue = binaryByteValue % 1024**value

    return resultBinaryIntegers

# Aufforderung und Durchführung der Berechnung bis der Benutzer das Program beendet
while NeueBerechnung.upper() != 'N':
    
    # ! Operating System Specific OS command
    match get_platform():
        case "OS X":            os.system('clear')
        case "Windows":         os.system('cls')
        case "Linux":           os.system('clear')
        #case other:            # DO nothing
    
    # Abfrage der binären Basisgröße und des Präfixes auf das es umgewandelt werden soll.
    origInputBinaryValue = input(
        'Bitte geben Sie eine umzuwandelnde Speichermenge mit einem Einheiten-Präfix ein: ')
    InputBinaryValue = str(origInputBinaryValue.upper()).replace(' ', '')
    InputBinaryValue = str(InputBinaryValue.upper()).replace(',', '.')

    originPrefix = ''
    for binaryUnit in unitFactors:
        if binaryUnit in InputBinaryValue.upper():
            originPrefix = binaryUnit
            originBinaryValue = (InputBinaryValue.split(binaryUnit))[0]
            if not (originBinaryValue.replace('.', '')).isnumeric():
                originPrefix = ''
                next

            break

    errorText = ''
    if not originPrefix or not (str(originBinaryValue).replace('.', '')).isnumeric():
        if not originPrefix:
            errorText = 'KEINE UNTERSTÜTZTE EINHEIT nach der Zahl GEFUNDEN - Folgende Einheiten werden unterstützt: '

            for keys, value in unitFactors.items():
                errorText += keys + ', '

            errorText = errorText.rstrip(', ')

        indent = ''
        if not str(str(originBinaryValue).replace('.', '')).isnumeric() or originBinaryValue == 0:
            if errorText:
                errorText += '\n'
                errorText += '       '
                indent = '                               '

            errorText += f'KEINE ZAHL ERKANNT{indent} - Unterstütze Zeichen sind: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 und ","'

        print('')
        print(f'ERROR: {errorText}\n')
        print(f'       Ihre Eingabe "{origInputBinaryValue}", konnte nicht interpretiert werden.')
        print('       Leerzeichen zwischen den einzelnen Zeichen, sowie Groß- und Kleinschreibung werden ignoriert.\n\n')
        NeueBerechnung = input('Möchten Sie es nochmal versuchen - (N)ein beendet das Programm? ')
        if NeueBerechnung.upper() != 'N':
            continue

    else:
        originBinaryValue = float(originBinaryValue)

        # Umwandlung des Wertes in diverse Prefix Darstellungen
        floatText = ''
        for targetPrefix, value in unitFactors.items():
            if targetPrefix != next(iter(unitFactors.items()))[0]:
                floatText += '                                           '

            floatText += " " + locale.currency(toBinaryWithPrefix(originBinaryValue, originPrefix, targetPrefix), False, grouping=True, ) + ' ' + targetPrefix + '\n'

        resultBinaryIntegers = toReadablePrefixedInteger(
            originBinaryValue, originPrefix)

        readableText = ''
        for key, value in resultBinaryIntegers.items():
            if value > 0:
                if len(readableText) > 0: readableText += ", "
                readableText += str(int(value)) + " " + key

        print('')
        print(f'LESBARE FORM der Speichergröße:             {readableText}\n')
        print(f'GLEITZAHLEN DARSTELLUNG der Speichergrößen:{floatText}')

        # Benutzer Fragen ob er noch eine Berechnung durchführen möchte
        NeueBerechnung = input(
            'Möchten Sie noch eine Berechnung durchführen - (N)ein beendet das Programm? ')

        # Terminal Fenster löschen
        print('Danke das Sie unseren Service in Anspruch genommen haben.\n\n')
