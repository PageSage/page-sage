const sidebar = $('#sidebar-bg').get(0);
const smallSidebar = $('#sidebar').get(0)
const main = $('#main').get(0);
const searchItem = $('#search').get(0);
const searchItemSmall = $('#search-small').get(0);
const searchForm = $('#search-form-header').get(0);
const mainSearch = $('#main-search').get(0);

function toggleSidebar() {
    if (sidebar.style.display === "none") {
        main.style.marginLeft="250px";
        sidebar.style.width="250px";
        sidebar.style.display = "block";
    } else {
        main.style.marginLeft="0%";
        sidebar.style.display = "none";
    }
}

function toggleSmallSidebar() {
    if (smallSidebar.style.display === "none") {
        smallSidebar.style.width="66%"
        main.style.marginLeft="0%"
        smallSidebar.style.display = "block";
    } else {
        smallSidebar.style.display = "none";
    }
}

function hideStyle() {
    searchItem.style.backgroundImage="none";
}

function clearSearch() {
    searchItem.value="";
}

function bookSearch() {
    let search = searchItem.value;
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
               results.innerHTML += "<p>" + books.items[i].volumeInfo.title + "</p>"
           }
       }
    });
}
