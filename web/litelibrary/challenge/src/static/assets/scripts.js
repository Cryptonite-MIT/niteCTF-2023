const isAdmin = false;

const MAX_TEXT_INPUT_LENGTH = 100;
const MAX_PAGE_COUNT = 10000;
const BOOKS_FETCH_URL = "/api/getBooks";
const BOOKS_SEARCH_URL = "/api/search?q=";
const STATS_URL = "/stats";
const IMAGE_ROOT =
    "https://raw.githubusercontent.com/benoitvallon/100-best-books/master/static/";

const searchForm = document.querySelector(".form-search");
const newBookForm = document.querySelector(".form-new-book");
const formSearch = document.querySelector("#book-search");
const formTitle = document.querySelector("#book-title");
const formAuthor = document.querySelector("#book-author");
const formPages = document.querySelector("#book-pageCount");
const formUnread = document.querySelector('img[alt="unread"]');
const formRead = document.querySelector('img[alt="read"]');
const formSubmit = document.querySelector("#submit");
const libraryRoot = document.querySelector(".content-inner");
const templateCard = document.querySelector("#template-card");
const resetBtn = document.querySelector(".resetBtn");

function addClass(element, className) {
    element.classList.add(className);
}

function removeClass(element, className) {
    element.classList.remove(className);
}

function addRemoveClass(className, toRemove, toAdd) {
    toRemove.classList.remove(className);
    addClass(toAdd, className);
}

function hideElement(element) {
    addClass(element, "hidden");
}

function highlightError(field) {
    addClass(field, "invalid-input");
    field.focus();
}

function showConfirmPopup(message) {
    return confirm(message);
}

// localStorage wrappers
function readLs(key) {
    const localStorageTemp = localStorage.getItem(key);
    if (localStorageTemp !== null) return localStorageTemp;
    else return false;
}

function writeLs(key, value) {
    localStorage.setItem(key, value);
}

function clearLs() {
    localStorage.clear();
}

function saveLibraryToLs() {
    writeLs("library", JSON.stringify(library));
}

let cardButtonsTemplate = "";
async function initFillLibrary() {
    libraryRoot.innerHTML = "";

    if (!library.length) {
        await fetch(BOOKS_FETCH_URL).then((resp) =>
            resp.json().then((json) => (library = json))
        );
        saveLibraryToLs();
    }

    templateCard.removeAttribute("id");
    cardTemplate = templateCard.outerHTML;
    templateCard.remove();

    if (library.length === 0) libraryRoot.textContent = "No Books Saved";
    else library.forEach((book) => addBookToDomLibrary(book));
}

function addBookToDomLibrary(book, scrollToCard = false) {
    // clear "No Books Saved" message
    if (libraryRoot.childElementCount === 0) libraryRoot.innerHTML = "";

    libraryRoot.innerHTML += cardTemplate
        .replace("Book Title", book.title)
        .replace("Book Author", book.author);

    let cards = libraryRoot.querySelectorAll(".card");
    let card = cards[cards.length - 1];

    const pages = card.querySelectorAll(".card-text")[1];
    if (book.pages !== 0 && book.pages !== "0")
        pages.textContent = `${book.pages} pages`;
    else pages.remove();

    let bookImg = card.querySelector("img");
    if (!book.imageLink) bookImg.src = "";
    else if (
        book.imageLink?.startsWith("http") ||
        book.imageLink?.startsWith("/")
    )
        bookImg.src = book.imageLink;
    else bookImg.src = `${IMAGE_ROOT}${book.imageLink}`;
    bookImg.setAttribute(
        "alt",
        `Cover photo of ${book.title} by ${book.author}`
    );

    const notFavBtn = card.querySelector(".not-fav");
    const favBtn = card.querySelector(".fav");
    if (book.fav) {
        hideElement(notFavBtn);
    } else {
        hideElement(favBtn);
    }

    const unreadBtn = card.querySelector(".unread");
    const readBtn = card.querySelector(".read");
    if (book.read) {
        hideElement(unreadBtn);
    } else {
        hideElement(readBtn);
    }

    addListeners();

    if (scrollToCard) {
        card.scrollIntoView();
        addClass(card, "new-card");
    }
}

function addListeners() {
    const libraryRoot = document.querySelector(".content-inner");
    const cards = libraryRoot.querySelectorAll(".card");

    cards.forEach((card, i) => {
        const book = library[i];

        const bookImg = card.querySelector("img");

        if (book.link !== "")
            bookImg.addEventListener("click", () => window.open(book.link));

        const notFavBtn = card.querySelector(".not-fav");
        const favBtn = card.querySelector(".fav");
        const unreadBtn = card.querySelector(".unread");
        const readBtn = card.querySelector(".read");
        const toggleBtnList = [notFavBtn, favBtn, unreadBtn, readBtn];
        const deleteBtn = card.querySelector(".delete");

        toggleBtnList.forEach((btn) =>
            btn.addEventListener("click", toggleCardButtonState)
        );
        deleteBtn.addEventListener("click", deleteBook);
    });
}

function addBookFromUser() {
    const title = formTitle.value.slice(0, MAX_TEXT_INPUT_LENGTH);
    const author = formAuthor.value.slice(0, MAX_TEXT_INPUT_LENGTH);
    const pages = formPages.value;
    if (title.length === 0) {
        highlightError(formTitle);
    } else if (bookAlreadyExists(title)) {
    } else if (author.length === 0) {
        highlightError(formAuthor);
    } else if (
        Number(pages) > MAX_PAGE_COUNT ||
        (pages.length !== 0 && // pages field is not mandatory, only then do non-number
            isNaN(pages)) //  detection https://stackoverflow.com/a/175787
    )
        highlightError(formPages);
    else {
        const book = new newBook(title, author, Number(pages), formReadSwitch);
        library.push(book);
        saveLibraryToLs();
        addBookToDomLibrary(book, true);

        formTitle.value = "";
        formAuthor.value = "";
        formPages.value = "";
    }
}

class newBook {
    constructor(title, author, pages, read) {
        this.title = title;
        this.author = author;
        this.pages = pages;
        this.read = read;
        this.fav = false;
    }
}

function bookAlreadyExists(givenTitle) {
    const titleLc = givenTitle.toLocaleLowerCase();
    if (library.find((book) => book.title.toLocaleLowerCase() === titleLc)) {
        highlightError(formTitle);
        const cards = libraryRoot.querySelectorAll(".card");
        cards.forEach((card) => {
            const cardBookTitle = card.querySelector(".card-title").textContent;
            if (cardBookTitle.toLocaleLowerCase() === titleLc) {
                highlightError(card);
            }
        });
        return true;
    }
    return false;
}

// remove all error highlights on keypress
[formTitle, formAuthor, formPages].forEach((input) =>
    input.addEventListener("keypress", (e) => {
        e.target.classList.remove("invalid-input");
        const cards = libraryRoot.querySelectorAll(".card");
        cards.forEach((card) => {
            card.classList.remove("invalid-input");
        });
    })
);

// toggleHeaderFormReadState
let formReadSwitch = false;
[formUnread, formRead].forEach((btn) =>
    btn.addEventListener("click", () => {
        if (!btn.classList.contains("selected")) {
            if (formUnread.classList.contains("selected")) {
                formReadSwitch = true;
                addRemoveClass("selected", formUnread, formRead);
            } else {
                formReadSwitch = false;
                addRemoveClass("selected", formRead, formUnread);
            }
        }
    })
);

formSubmit.addEventListener("click", (e) => {
    e.stopPropagation();
    addBookFromUser();
});

// book cards stuff below
function toggleCardButtonState() {
    const cardButtons = this.parentElement;
    const bookIndex = getBookTitle(cardButtons, true);

    const options = this.parentElement.dataset.options
        .split("|")
        .map((op) => `.${op}`);
    const offBtn = cardButtons.querySelector(options[0]);
    const onBtn = cardButtons.querySelector(options[1]);
    const key = options[1].slice(1);

    if (offBtn.classList.contains("hidden")) {
        library[bookIndex][key] = false;
        addRemoveClass("hidden", offBtn, onBtn);
    } else {
        library[bookIndex][key] = true;
        addRemoveClass("hidden", onBtn, offBtn);
    }
    saveLibraryToLs();
}

function deleteBook() {
    const bookTitle = getBookTitle(this);

    if (!showConfirmPopup(`Delete the book [${bookTitle}]?`)) return;

    // library = library.filter((book) => book.title !== bookTitle);
    // saveLibraryToLs();

    this.parentElement.parentElement.remove();
    if (libraryRoot.childElementCount === 0)
        libraryRoot.textContent = "No Books Saved";
}

function getBookTitle(cardButtons, getIndexInstead = false) {
    let bookTitle =
        cardButtons.parentElement.parentElement.children[0].querySelector(
            ".card-title"
        ).textContent;
    if (getIndexInstead) {
        return library.findIndex((book) => book.title === bookTitle);
    }
    return bookTitle;
}

function resetLibrary() {
    if (!showConfirmPopup("Delete all books and reset to default?")) return;
    if (
        !showConfirmPopup(
            "Are you absolutely sure? ALL books will be PERMANENTLY DELETED"
        )
    )
        return;

    clearLs();
    document.location.reload();
    window.scrollTo(0, 0);
}

async function search() {
    const query = formSearch.value.toLocaleLowerCase();
    if (!query) {
        initFillLibrary();
        return;
    }

    const results = await fetch(`${BOOKS_SEARCH_URL}${query}`).then((resp) =>
        resp.json().then((json) => {
            return json;
        })
    );

    if (results.length === 0) libraryRoot.textContent = "No books found";
    else {
        libraryRoot.innerHTML = "";
        results.forEach((result) => addBookToDomLibrary(result));
    }
}

const updateStats = () =>
    fetch(STATS_URL)
        .then((r) => r.json())
        .then(
            (r) =>
                (document.querySelector(
                    "#stats"
                ).textContent = `Powered by Lite! Home to ${r.count}+ books`)
        );

document.addEventListener("DOMContentLoaded", () => {
    formSearch.addEventListener("keyup", search);

    resetBtn.addEventListener("click", resetLibrary);

    document.body.addEventListener("click", () => {
        const newCard = document.querySelector(".new-card");
        if (newCard !== null) removeClass(newCard, "new-card");
    });

    if (isAdmin) searchForm.classList.add("hidden");
    else newBookForm.classList.add("hidden");

    document.querySelector("marquee").textContent = atob(
        "QSBib29rIHJldmlldyBhbGxvd3Mgc3R1ZGVudHMgdG8gaWxsdXN0cmF0ZSB0aGUgYXV0aG9ycyBpbnRlbnRpb25zIG9mIHdyaXRpbmcgdGhlIHBpZWNlIGFzIHdlbGwgYXMgY3JlYXRlIGEgY3JpdGljaXNtIG9mIHRoZSBib29rIGFzIGEgd2hvbGUgaW4gb3RoZXIgd29yZHMgZm9ybSBhbiBvcGluaW9uIG9mIHRoZSBhdXRob3JzIHByZXNlbnRlZCBpZGVhcyBib29rIHJldmlld3MgYXJlIGFzc2lnbmVkIHRvIGFsbG93IHN0dWRlbnRzIHRvIHByZXNlbnQgdGhlaXIgb3duIG9waW5pb24gcmVnYXJkaW5nIHRoZSBhdXRob3JzIGlkZWFzIGluY2x1ZGVkIGluIHRoZSBib29rIG9yIHBhc3NhZ2UgdGhleSBhcmUgYSBmb3JtIG9mIGxpdGVyYXJ5IGNyaXRpY2lzbSB0aGF0IGFuYWx5emVzIHRoZSBhdXRob3JzIGlkZWFzIHdyaXRpbmcgdGVjaG5pcXVlcyBhbmQgcXVhbGl0eSBhIGJvb2sgYW5hbHlzaXMgaXMgZW50aXJlbHkgb3BpbmlvbmJhc2VkIGluIHJlbGV2YW5jZSB0byB0aGUgYm9vayB0aGV5IGFyZSBnb29kIHByYWN0aWNlIGZvciB0aG9zZSB3aG8gd2lzaCB0byBiZWNvbWUgZWRpdG9ycyBkdWUgdG8gdGhlIGZhY3QgZWRpdGluZyByZXF1aXJlcyBhIGxvdCBvZiBjcml0aWNpc20gcHJlc3VtYWJseSB5b3UgaGF2ZSBjaG9zZW4geW91ciBib29rIHRvIGJlZ2luIG1lbnRpb24gdGhlIGJvb2sgdGl0bGUgYW5kIGF1dGhvcnMgbmFtZSB0YWxrIGFib3V0IHRoZSBjb3ZlciBvZiB0aGUgYm9vayB3cml0ZSBhIHRoZXNpcyBzdGF0ZW1lbnQgcmVnYXJkaW5nIHRoZSBmaWN0aXRpb3VzIHN0b3J5IG9yIG5vbmZpY3Rpb25hbCBub3ZlbCB3aGljaCBicmllZmx5IGRlc2NyaWJlcyB0aGUgcXVvdGVkIG1hdGVyaWFsIGluIHRoZSBib29rIHJldmlldyB3ZWxjb21lIGJlaW5nIGxpdGUgaXNudCBlYXN5IGJ1dCB3ZSBoZXJlIGF0bGl0ZWxpYnJhcnkgc3RyaXZlIG91dCBiZXN0IHRvIGFkaGVyIHRvIHRoZSBub3Jtcy4gVG8gYmVnaW4gd2l0aCwgd2UgdXNlIG1pbmltYWwgaW50ZXJuZXQgZnJvbSBvdXIgc2VydmVyczogZmV0Y2ggb25jZSBhdCBpbml0aWFsaXNlIGFuZCBicnV0YWxpc2UgbG9jYWxzdG9yYWdlIHRoZXJlYWZ0ZXIuIEFsc28gdGhlIHNjcm9sbGluZyBzcGVlZCBvZiB0aGlzIHRleHQgaXMgdGhlIG1heGltdW0gc3BlZWQgcmVhZGFibGUgYnkgYSBodW1hbiBiZWluZyBhY2NvcmRpbmcgdG8gYSBzdHVkeSBjYXJyaWVkIG91dCBieSB0aGUgdW5pdGVkIG5hdGlvbnMgbmF0aW9uYWwgaW5zdGl0dXRlIG9mIG9jdWxhciBtb2xlY3VsYXIgcmV0aW5hbCBhbmQgcGVudGFnb25hbCB2aXNpb24gZGV2ZWxvcG1lbnQgYW5kIGluZHVzdHJpYWwgY29vcnBvcmF0aW9uIGluc3RpdHV0ZSB1bmRlciB0aGUgc21pdGhzb25pYW4gYWNhZGVteSBvZiBib2RpbHkgYWxjaGVteSBtb3N0IG9mdGhlIGZlYXR1cmVzIG9uIHRoaXMgbGlicmFyeSBhcmUgZm9yIHZpc3VhbCBhcHBlYXNlbWVudGFuZCBzZXJ2ZXIgbm8gYWN0dWFsIGZ1bmN0aW9uIHllcyB3ZSBhZG1pdCB0aGF0IHRoaXNtaWdodCBtYWtlIHNvbWVvbmUgZ28gbWFkIGJ1dCBoZXkgeW91IGNhbiBicm93c2UgYmFyZWx5IHRlbiBib29rcyBhdCBvbmNlLiBUaGF0IGRvZXMgbm90IHNlZW0gbGlrZSBtdWNoIGhlYWRicmVha2luZyB0byB1cy4gRG8gbm90IGV2ZW4gdGhpbmsgb2Ygc3NyZmluZyB1cyBhcyBhbGwgaW1hZ2VzIHNob3duIGNvbWUgZnJvbSBleHRlcm5hbCBzb3VyY2VzLiBXYW5uYSBhZGQgeW91ciB0cmFzaCBib29rIHRvIHRoaXMgcGlsZT8gU29ycnkgd2UgZG8gbm90IGhhdmUgYW4gYWRtaW4gYXZhaWxhYmxlIHJpZ2h0IG5vdy4gT2ggd2FpdC4gV2UgbWlnaHQgaGF2ZSBhbiBSMkQyLiAqYmVlcCogKmJlZXAqIFNvcnJ5IGFnYWluLCBpdCdzIGJyb2t3biBqdXN0IGxpa2UgKnN0YXRpYyogUmVnYXJkcyBNYWRtYXguIGNob29zZSBhIHNwZWNpZmljIGNoYXB0ZXIgb3Igc2NlbmFyaW8gdG8gc3VtbWFyaXNlIGluY2x1ZGUgYWJvdXQgMyBxdW90ZXMgaW4gdGhlIGJvZHkgY3JlYXRlIHN1bW1hcmllcyBvZiBlYWNoIHF1b3RlIGluIHlvdXIgb3duIHdvcmRzIGl0IGlzIGFsc28gZW5jb3VyYWdlZCB0byBpbmNsdWRlIHlvdXIgb3duIHBvaW50b2Z2aWV3IGFuZCB0aGUgd2F5IHlvdSBpbnRlcnByZXQgdGhlIHF1b3RlIGl0IGlzIGhpZ2hseSBpbXBvcnRhbnQgdG8gaGF2ZSBvbmUgcXVvdGUgcGVyIHBhcmFncmFwaCB3cml0ZSBhIHN1bW1hcnkgb2YgdGhlIHN1bW1hcmlzZWQgcXVvdGF0aW9ucyBhbmQgZXhwbGFuYXRpb25zIGluY2x1ZGVkIGluIHRoZSBib2R5IHBhcmFncmFwaHMgYWZ0ZXIgZG9pbmcgc28gZmluaXNoIGJvb2sgYW5hbHlzaXMgd2l0aCBhIGNvbmNsdWRpbmcgc2VudGVuY2UgdG8gc2hvdyB0aGUgYmlnZ2VyIHBpY3R1cmUgb2YgdGhlIGJvb2sgdGhpbmsgdG8geW91cnNlbGYgaXMgaXQgd29ydGggcmVhZGluZyAgYW5kIGFuc3dlciB0aGUgcXVlc3Rpb24gaW4gYmxhY2sgYW5kIHdoaXRlIGhvd2V2ZXIgd3JpdGUgaW5iZXR3ZWVuIHRoZSBsaW5lcyBhdm9pZCBzdGF0aW5nIGkgbGlrZWRpc2xpa2UgdGhpcyBib29rCgoK"
    );

    updateStats();
});

let library = JSON.parse(readLs("library"));

initFillLibrary();
