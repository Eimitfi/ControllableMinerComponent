# ControllableMinerComponent

Basically this component is a process that can work in order to find mining solutions + through local pipes it can accept arbitrary functions and call them as methods.
This allows to have change the code of the component at runtime.

Well read the report first, then you can directly dive in the hardWorker.py code, it's pretty slim.
Second, I initialized it to be ready to work with garlicoin, that's why cLib is present(if u wanna try, don't forget to gcc -shared -fPIC -o isValid.so isValid.c lyra2/*.c sha3/*.c); of course you can get rid of those C dependencies by telling the hardworker to use a python hash function of any cryptocurrency.

