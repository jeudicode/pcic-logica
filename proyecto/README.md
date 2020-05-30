# Paquete de BDDs

## Proyecto final para la materia de Lógica Computacional del PCIC del IIMAS @ UNAM (2020-II)

El proyecto consiste en hacer una implementación de diagramas binarios de decisión (BDDs), así como los algoritmos REDUCE y APPLY. Todas las funciones están implementadas de manera recursiva excepto REDUCE, que se implementó de manera iterativa.

### Uso

La aplicación se ejecuta mediante línea de comandos con la siguiente estructura:

`python main.py <formula1> <formula2> <op> <order>`

donde `<formula1>` y `<formula2>` son las expresiones lógicas a evaluar, `<op>` es el operador a aplicar entre dichas expresiones y `<order>` es el orden de las variables a utilizar. Las expresiones deben estar escritas de forma infija y por el momento se pide utilizar un orden consecutivo en las variables. Por ejemplo:

`python main.py p+q pxr + pqr`

En este caso, la primera fórmula corresponde a $p \lor q$ y la segunda fórmula corresponde a $p \land r$; el operador a aplicar entre ellas es $\lor$ y el orden es $\{p,q,r\}$.

Los operadores implementados son:

1.  AND (x)
2.  OR (+)
3.  NOT(-)
4.  XOR(#)

Algunos ejemplos de expresiones:

    pxqxr
    p#q
    q#r
    -p+q#r

El programa muestra una salida en consola con los resultados de la construcción y reducción de los BDDs. A su vez, crea imágenes con los dibujos de los BDD1, BDD2 y BDD1 op BDD2.
