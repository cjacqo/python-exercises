# Exercise 1.2

This exercise explains different ways in how to store/manipulate different data types and how to define and structure different data structures. For this exercise, the goal was to build a simple recipe application that stores a list of recipes in a data structure with each recipe structure including the name, cooking time, and a list of ingredients. It was my decision to store a recipe in a dictionary data structure with the name being a string, the cooking time being an integer and the list of ingredients being a tuple. The first two data types (string and integer) are pretty self explanatory, but I decided on storing the list of ingredients in a tuple because the data should be immutable. If you have a list of ingredients for a recipe, the ingredients should not have to be altered. Furthermore, tuples are faster to read and access.

An example of a recipe data structure is below:

```
{
    "name": str,
    "cooking_time": int,
    "ingredients": (tuple)
}

```

An example of the recipes dictionary structure is below:

```
{
    "recipe_name": {
        "name": str,
        "cooking_time": int,
        "ingredients": (tuple)
    },
    "recipe_name": {
        "name": str,
        "cooking_time": int,
        "ingredients": (tuple)
    },
    ...
}
```