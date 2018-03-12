
## How to configure it

In config.py you can configure:
* Name of output latex file
* Path to folders with prolog programs and least models
* Pattern to consider (example: 1212)
* Syllogims to include in the file
* Information to include in the file about each syllogism. 
Currently the following information can be selected
to be included in the latex file:

```
include_Program = True     --> prolog encoding
include_GProgram = True    --> grounded program
include_LeastModel = True  --> least model
include_EntailedConclusions = True  --> conclusions entailed by our least model
include_Experiments = True          --> human answers
```
Do not delete any constant from config.py file. 


## How to run it

```
python createLatexFile.py 
```

