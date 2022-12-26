# About:

This is a verb conjugator for Czech verbs that currently conjugates for 2 tenses: present and past, as well as for 3 moods: indicative, imperative, and conditional. This conjugator is also capable of conjugating *future* tense for so far only 1 verb, that verb being *být* and its negated form *nebýt*.

## Caveats:
1. For some verbs, there are multiple valid/grammatically correct forms. I chose the forms that most closely adhere to the conjugation patterns.
2. Some verbs are homonyms, and therefore have different conjugations depending on its intended meaning. I only chose the more common meaning of the verb to conjugate. 
    Some homonyms include the following:
    - *žít*: to live, *žít (žnout)* to reap
    - *snít*: to dream,  *snít (sejmout)* to take away
    
    These homonyms have alternate forms more commonly used in the parentheses (and also more regular!). These homonyms conjugate like *tít* or *vzít* regardless.
3. This conjugator is naive. It cannot recognize whether the word given is actually an existing Czech verb. That being said, it **will** attempt conjugate non-Czech words such as *racket*, *gadget*, *habit*, *snout* and so forth since they **look** like verbs. This also includes Czech nouns that look like verbs.
4. This conjugator may not conjugate ***all*** verbs correctly, though I tried my best in covering the vast majoity of edge cases (irregular, slightly irregular, etc.). This is because the verbs I used to test the conjugator came from here: https://en.wiktionary.org/wiki/Category:Czech_verbs, where it has (as of December 25th, 2022) 4,573 verbs. I did not test all of them. The majority of the verbs in that list are regular.

## Requirements:
1. Python3.8 intepreter or higher
2. Knowledge of the command line (if using a CLI)
3. Czech (or Slovak) keyboard installed

## Files:
1. conjugator.py:
    - runs the actual program
2. verbs.py:
    - code file to for the implementation of the Verb base class and its various subclasses
4. irregular.txt:
    - .txt file containing almost 100 irregular verbs. Each line holds the infinitive, its conjugation class, present tense stem, past participle (masculine singular), and singular form of the verb in the imperative
6. prefix.txt:
    - .txt file containing the list of verbal prefixes, and its variant forms, as indicated with regex. This file is intended for generating a regex string.
 
## Running the Program:

(if CLI) Type in the following command to begin running the program:
```python3.8 conjugator.py```

Once run it should soon prompt you to enter a verb, as shown here:
```please enter a verb infinitive:```

And enter a verb *infinitive*. If one is not given, "none of the above" is displayed and nothing is conjugated:

```
please enter a verb infinitive:
none of the above
```

```
please enter a verb infinitive: hello
none of the above
```

Once entered, the verb infinitive is conjugated and produces the following tables:
(using example verb *studovat* (to study))

```
please enter a verb infinitive: studovat
+------------------------------------------------------------------------+
|                      PRESENT TENSE (PŘÍTOMNÝ ČAS)                      |
+------------------------------------------------------------------------+
| +----------------+---------------------------+-----------------------+ |
| | PERSON (OSOBA) | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ) | |
| +----------------+---------------------------+-----------------------+ |
| |       1.       |      studuji/studuju      |       studujeme       | |
| |       2.       |          studuješ         |       studujete       | |
| |       3.       |          studuje          |        studují        | |
| +----------------+---------------------------+-----------------------+ |
+------------------------------------------------------------------------+
+------------------------------------------------------------------------+
|                  IMPERATIVE MOOD (ROZKAZOVÁCÍ ZPŮSOB)                  |
+------------------------------------------------------------------------+
| +----------------+---------------------------+-----------------------+ |
| | PERSON (OSOBA) | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ) | |
| +----------------+---------------------------+-----------------------+ |
| |       1.       |             -             |        studujme       | |
| |       2.       |           studuj          |        studujte       | |
| |       3.       |             -             |           -           | |
| +----------------+---------------------------+-----------------------+ |
+------------------------------------------------------------------------+
+----------------------------------------------------------------------------------------------------+
|                                      PAST TENSE (MINULÝ ČAS)                                       |
+----------------------------------------------------------------------------------------------------+
|               +----------------+---------------------------+-----------------------+               |
|               | PERSON (OSOBA) | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ) |               |
|               +----------------+---------------------------+-----------------------+               |
|               |       1.       |       studoval jsem       |     studovali jsme    |               |
|               |       2.       |     studoval jsi/jseš     |     studovali jste    |               |
|               |       3.       |          studoval         |       studovali       |               |
|               +----------------+---------------------------+-----------------------+               |
|          NOTE: past participles must agree with both gender and number of the subject(s):          |
| +--------------------------------------------+---------------------------+-----------------------+ |
| |                GENDER (ROD)                | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ) | |
| +--------------------------------------------+---------------------------+-----------------------+ |
| |   MASCULINE ANIMATE (ROD MUŽSKÝ ŽIVOTNÝ)   |          studoval         |       studovali       | |
| | MASCULINE INANIMATE (ROD MUŽSKÝ NEŽIVOTNÝ) |          studoval         |       studovaly       | |
| |           FEMININE (ROD ŽENSKÝ)            |         studovala         |       studovaly       | |
| |            NEUTER (ROD STŘEDNÍ)            |         studovalo         |       studovala       | |
| +--------------------------------------------+---------------------------+-----------------------+ |
+----------------------------------------------------------------------------------------------------+
+----------------------------------------------------------------------------------------------------+
|                               CONDITIONAL MOOD (PODMIŇOVÁCÍ ZPŮSOB)                                |
+----------------------------------------------------------------------------------------------------+
|                        NOTE: conjugations of by also apply to aby and kdyby                        |
|              +----------------+---------------------------+------------------------+               |
|              | PERSON (OSOBA) | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ)  |               |
|              +----------------+---------------------------+------------------------+               |
|              |       1.       |       studoval bych       | studovali bychom/bysme |               |
|              |       2.       |        studoval bys       |     studoval byste     |               |
|              |       3.       |        studoval by        |      studoval by       |               |
|              +----------------+---------------------------+------------------------+               |
|          NOTE: past participles must agree with both gender and number of the subject(s):          |
| +--------------------------------------------+---------------------------+-----------------------+ |
| |                GENDER (ROD)                | SINGULAR (ČÍSLO JEDNOTNÉ) | PLURAL (ČÍSLO MNOŽNÉ) | |
| +--------------------------------------------+---------------------------+-----------------------+ |
| |   MASCULINE ANIMATE (ROD MUŽSKÝ ŽIVOTNÝ)   |          studoval         |       studovali       | |
| | MASCULINE INANIMATE (ROD MUŽSKÝ NEŽIVOTNÝ) |          studoval         |       studovaly       | |
| |           FEMININE (ROD ŽENSKÝ)            |         studovala         |       studovaly       | |
| |            NEUTER (ROD STŘEDNÍ)            |         studovalo         |       studovala       | |
| +--------------------------------------------+---------------------------+-----------------------+ |
+----------------------------------------------------------------------------------------------------+
```

# Further information:
All information, that was not initally from my own knowledge of the Czech language were from these following sources. These websites are in Czech, barring the 1st (though sometimes the conjugation may only be available on the Czech version of the page):
1. https://en.wiktionary.org/wiki/Category:Czech_verbs (and the following pages of each verb listed)
2. https://www.nechybujte.cz/
3. https://www.pravidla.cz/
4. http://www.dobryslovnik.cz/cestina
5. https://ssjc.ujc.cas.cz/ (requires the archaic form of the infinitive to search properly (the -i after the t))
*************************************************************
# Future improvements/plans:
1. adding passive participle conjugation
2. adding transgressive conjugation (present and past)
3. adding verbal noun/adjectival form
4. adding future tense form if imperfective
5. determining the verb's aspect
6. seperation of conditional mood into present and past conditional mood
