# JS Files

## `authn.js`
Placeholder JavaScript file for AuthN pages. __Needs to be removed__

## `bookclub.js`
Placeholder JavaScript file for Bookclub pages.

## `landing.js`
Placeholder JavaScript file for Landing pages. 

## `user.js`
JavaScript for User pages. __Needs to be split into user and general.js__
* `const` variables used instead of getElementById because we want persistence with these variables
* `toggleSidebar()` 
  * 250px width because it fit bar items the best
  * Defaults to sidebar not on display
  * Pushes main page to the side: does not overlap
* `toggleSmallSidebar()`
  * toggle for small screens - size is 2/3 of the screen
  * Overlaps content
* `hideStyle()`
  * Hides the Google watermark when the search bar is selected
* `clearSearch()`
  * Clears the contents of the searchbar when the search page is loaded
* `bookSearch()`
  * Uses the Google Books API for book results
