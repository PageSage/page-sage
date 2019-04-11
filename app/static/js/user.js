const sidebar = $('#sidebar-bg').get(0);
const smallSidebar = $('#sidebar').get(0)
const main = $('#main').get(0);
const searchItem = $('#search').get(0);
const searchItemSmall = $('#search-small').get(0);
const searchForm = $('#search-form-header').get(0);
const mainSearch = $('#main-search').get(0);
const bookSearcher = $('#book_choice').get(0);

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
               results.innerHTML += "<div class='form-group'>"+
               '{{form2.bookTitle(value+books.items[i].volumeInfo.title' +
               " type='hidden')}} {{form2.isbn(value="+books.items[i].volumeInfo.industryIdentifiers[1].identifier+" type='hidden')}}"+ "<input type='submit' name='book' value="+books.items[i].volumeInfo.title+ "></input></div>"
           }
       }
    });
}
function bookShower(){
  let bookchoice= bookSearcher.value;
  document.getElementById('bookresult').innerHTML = "";
  console.log(bookchoice);
  $.ajax({

    dataType: "json",
    type: 'GET',
    success: function(book){
      bookresult.innerHTML += "<p>"+ book.volumeInfo.title + "</p>";
    }
  })

}
