# Python-SentiStrength
Python 3 Wrapper for SentiStrength, reads a single or multiple input with options for binary class or scale output.

Ensure that you have SentiStrength.jar file and SentiStrengthData Language folders, otherwise you can download them from http://sentistrength.wlv.ac.uk/.

## Installation

Pip:

```sh
pip install sentistrength
```


## Examples

Example use (single string):

```python
>>> from sentistrength import PySentiStr
>>> senti = PySentiStr()
>>> result = senti.getSentiment('What a lovely day')
>>> print(result)

... [0.25]
```


Example use (list of strings or pandas Series):

```python
>>> from sentistrength import PySentiStr
>>> senti = PySentiStr()
>>> str_arr = ['What a lovely day', 'What a bad day']
>>> result = senti.getSentiment(str_arr)
>>> print(result)

... [0.25,-0.25]
# OR, if want binary scoring (a score each for positive rating and negativing rating) instead of scale
>>> result = senti.getSentiment(str_arr, score='binary')
>>> print(result)

... [(2, -1), (1, -2)]
```

## Path Setup

Ensure that you have SentiStrength.jar file and SentiStrengthData folder in the same folder, otherwise you can specify the path:

```python
>>> senti = PySentiStr()
>>> senti.setSentiStrengthPath = ... # e.g. 'C:\Documents\SentiStrength.jar'
>>> senti.setSentiStrengthLanguageFolderPath = ... # e.g. 'C:\Documents\SentiStrengthData\'
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Big thanks to Dr. Mike Thelwall for access to SentiStrength.
