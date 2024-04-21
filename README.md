# About:

This is a verb conjugator for Czech verbs that currently conjugates for 3 tenses: present and past and future, as well as for 3 moods: indicative, imperative, and conditional. 

## Requirements:
1. Python3.8 intepreter or higher
2. pytest 7.4.1 or higher
3. Czech (or Slovak) keyboard installed (or know the keyboard shortcuts/unicode values for the diacritics used)

## Running

1. Clone this repository:
    `git clone https://github.com/svhawkins/czech-verb-conjugator.git <directory name>`

2. Set up the environment and aliases
    ```
    cd <directory name> (by default czech-verb-conjugator)
    source setup
    ```

    This sets up the aliases `tests` and `conjugator`. `tests` runs the `test.sh` script, and `conjugator` runs `conjugator.py`

3. Run tests
    `tests`

4. Run the conjugator:
    `conjugator`

    Once run, then prompted to enter in an infinitive. 
    The verb is then conjugated and full its full conjugation table is displayed.

    `<show output for regular verb>`

    If the provided verb does not adhere to any infinitive patterns, nothing is conjugated, and reprompts.
    
    ```
    enter a verb infinitive (or 'q' to quit): studovan
    No verb class pattern corresponding with given verb.
    ```

## Directories and Files

```
2 directories, 17 files
.
├── README.md
├── conjugator.py
├── conjugator_utils.py
├── data
│   ├── concrete.txt
│   ├── get_verbs.sh
│   ├── irregular.txt
│   ├── prefix.txt
│   └── verbs.txt
├── setup
├── test
│   ├── __init__.py
│   ├── test.sh
│   ├── test_conjugator.py
│   ├── test_conjutils.py
│   ├── test_verbs.py
│   └── test_vutils.py
├── verb_utils.py
└── verbs.py
```


## Caveats:
1. For some verbs, there are multiple valid/grammatically correct forms. I chose the forms that most closely adhere to the conjugation patterns (as the ones that don't are more likely to be archaic, see 2.)

2. Some verbs are homonyms, and therefore have different conjugations depending on its intended meaning. I only chose the more common meaning of the verb to conjugate. 
    Some homonyms include the following:
    - *žít*: to live, *žít (žnout)* to reap
    - *snít*: to dream,  *snít (sejmout)* to take away
    
    These homonyms have alternate forms more commonly used in the parentheses (and also more regular!). These homonyms conjugate like *tít* or *vzít* regardless.

3. This conjugator is naive. It cannot recognize whether the word given is actually an existing Czech verb. That being said, it **will** attempt conjugate non-Czech words such as *racket*, *gadget*, *habit*, *snout* and so forth since they **look** like verbs. This also includes Czech nouns that look like verbs.

4. This conjugator does not conjugate all verbs correctly. However, it is able to conjugate properly for the majority of cases and for common irregular verbs.

5. All verbs are considered by default imperfective. This may lead to incorrect present + future conjugations.

6. Some verbs ending in *-stit* have multiple imperative stems. They by default use the shortened ending: *sť*.
There are few exceptions: *prstit*, *šustit*, and *hustit* take *-sti*.
 

# Further information:
All information, that was not initally from my own knowledge of the Czech language were from these following sources. These websites are in Czech, barring the 1st (though sometimes the conjugation may only be available on the Czech version of the page):
1. https://en.wiktionary.org/wiki/Category:Czech_verbs (and the following pages of each verb listed)
2. https://www.nechybujte.cz/
3. https://www.pravidla.cz/
4. http://www.dobryslovnik.cz/cestina
5. https://ssjc.ujc.cas.cz/ (requires the archaic form of the infinitive to search properly (the -i after the t in most cases))

*************************************************************
# Further work:
1. adding passive participle conjugation
2. adding transgressive conjugation (present and past)
3. adding verbal noun/adjectival form
4. determining the verb's aspect
5. seperation of conditional mood into present and past conditional mood
