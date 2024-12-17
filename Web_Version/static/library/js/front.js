const API_URL = '/api/books/';
let currentPage = 1;
let totalPages = 1;



function fetchBooks() {
    const search = document.getElementById('search').value;
    const yearMin = document.getElementById('year-min').value;
    const yearMax = document.getElementById('year-max').value;
    const status = document.getElementById('status').value;

    const url = new URL(API_URL, window.location.origin);
    const params = new URLSearchParams();

    if (search) params.append('search', search);
    if (yearMin) params.append('year_min', yearMin);
    if (yearMax) params.append('year_max', yearMax);
    if (status) params.append('status', status);
    params.append('page', currentPage);

    url.search = params.toString();

    fetch(url)
        .then(response => response.json())
        .then(data => {
            totalPages = Math.ceil(data.count / 4);
            displayBooks(data.results);
            updatePagination(data);
        })
        .catch(err => console.error('Error fetching books:', err));
}

function displayBooks(books) {
    const bookList = document.getElementById('book-list');
    bookList.innerHTML = ''; // Clear previous results

    books.forEach(book => {
        const li = document.createElement('li');
        li.classList.add('book-item');

        // Fallback to default image if cover_image is not available
        const coverImage = book.cover_image ? book.cover_image : '/media/book_covers/default_cover.jpg';

        li.innerHTML = `
            <a href="/book/${book.id}">
                <img src="${coverImage}" alt="${book.title}">
            </a>
            <h3>${book.title}</h3>
            <p><strong>Автор:</strong> ${book.author}</p>
            <p><strong>Год Издания:</strong> ${book.year}</p>
            <p><strong>Статус:</strong> ${book.status}</p>
        `;
        bookList.appendChild(li);
    });
}

function updatePagination(data) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const prevButton = document.createElement('button');
    prevButton.innerText = 'Назад';
    prevButton.disabled = currentPage <= 1;
    prevButton.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            fetchBooks();
        }
    });

    const nextButton = document.createElement('button');
    nextButton.innerText = 'Вперед';
    nextButton.disabled = currentPage >= totalPages;
    nextButton.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            fetchBooks();
        }
    });

    pagination.appendChild(prevButton);
    pagination.appendChild(nextButton);
}

document.getElementById('year-min').addEventListener('input', function () {
    document.getElementById('year-min-value').textContent = this.value;
});
document.getElementById('year-max').addEventListener('input', function () {
    document.getElementById('year-max-value').textContent = this.value;
});
document.getElementById('status').addEventListener('change', function () {
    currentPage = 1;
});

window.onload = fetchBooks;