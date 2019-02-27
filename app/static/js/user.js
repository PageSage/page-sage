const sidebar = $('#sidebar-bg').get(0);
const main = $('#main').get(0);

function toggleSidebar() {
    if (sidebar.style.display === "none") {
        main.style.marginLeft="12%";
        sidebar.style.width="12%";
        sidebar.style.display = "block";
    } else {
        main.style.marginLeft="0%";
        sidebar.style.display = "none";
    }
}

function bookSearch() {
    let search = document.getElementById('search').value;
    document.getElementById('results').innerHTML = "";
    console.log(search);
    let maxResults = "40";
    let orderBy = "relevance";
    let printType = "books";
    let projection = "full";
    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=" + search + "&maxResults=" + maxResults + 
             "&orderBy=" + orderBy + "&printType=" + printType + "&projection=" + projection + 
             "&key=" + search_api,
       dataType: "json",
       type: 'GET',
       success: function(books) {
           for (i = 0; i < books.items.length; i++) {
               results.innerHTML += "<h3>" + books.items[i].volumeInfo.title + "</h3>"
           }
       }
    });
}
