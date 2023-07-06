function loadSearchData() {
    // Data to be used in the searchbar
    let countries = [
      'Australia',
      'Austria',
      'Brazil',
      'Canada',
      'Denmark',
      'Egypt',
      'France',
      'Germany',
      'USA',
      'Vietnam'
    ];
    // Get the HTML element of the list
    let list = document.getElementById('list');
    // Add each data item as an <a> tag
    countries.forEach((country)=>{
        let a = document.createElement("a");
        a.innerText = country;
        a.classList.add("listItem");
        list.appendChild(a);
    })
  }

function search() {
    let listContainer = document.getElementById('list');
    let listItems = document.getElementsByClassName('listItem');
    let input = document.getElementById('searchbar').value
    input = input.toLowerCase(); 

    let noResults = true;
    for (i = 0; i < listItems.length; i++) { 
        if (!listItems[i].innerHTML.toLowerCase().includes(input) || input === "") {
            listItems[i].style.display="none";
            continue;
        }
        else {
            listItems[i].style.display="flex";
            listItems[i].onclick = function(){
                document.getElementById("searchbar").value = this.innerHTML;
                listContainer.style.display="none";
            }
            noResults = false; 
        }
    }
    listContainer.style.display = noResults ? "none" : "block";
}