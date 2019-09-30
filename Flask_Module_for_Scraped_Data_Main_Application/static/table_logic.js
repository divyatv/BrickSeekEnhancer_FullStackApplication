// from data.js get the data.
var tableData = dict_values;
console.log(tableData);

// Getting tbody tag
var tbody_tag = document.getElementsByTagName("tbody")[0];

// Get the columns of the data table
var columns=[]
columns=Object.keys(tableData[0]);

//Define the tr tag
var tr_tag;

//Set button for later user to click
var button = d3.select("#filter-btn");

//Code to just render all the table content. Outside of click.
//------------------------------------------------------------------
tableData.forEach(function(name){
  tr_tag=document.createElement('tr');
  
  columns.forEach(function(column){ 
    //console.log(column)
    var td_tag=document.createElement('td');
    var td_text=document.createTextNode(name[column]);
   //console.log(td_text);
    td_tag.appendChild(td_text);
    //console.log(td_tag);
   tr_tag.appendChild(td_tag);  
  });
 
  //console.log(tr_tag);
  tbody_tag.appendChild(tr_tag); 
});
//-------------------------------------------------------------------------    

//Code for button click and to filter the data based on user preference.
//-----------------------------------------------------------------------------
button.on("click", function() {
  //Clear previous search results.
tbody_tag.innerHTML=" ";
  //Get input element
var inputElement_sku = d3.select("#sku");
  // Get the value property of the input element
var inputValue_sku = inputElement_sku.property("value");

var inputElement_discount = d3.select("#discount");
  // Get the value property of the input element
var inputValue_discount = inputElement_discount.property("value");

var inputElement_stock = d3.select("#quantity");
  // Get the value property of the input element
var inputValue_stock = inputElement_stock.property("value");

var inputElement_zip = d3.select("#zip");
  // Get the value property of the input element
var inputValue_zip = inputElement_zip.property("value");

tableData.forEach(function(name){
  tr_tag=document.createElement('tr');
  
  columns.forEach(function(column){    
    
    //var denter= new Date(inputValue_sku);
    var dtable= new Date(name['datetime']);

    //Convert city and shape to all lower case so that it will match the dataset
    //var city_lowercase= inputValue_city.toLowerCase();
    //var shape_tolowercase=inputValue_shape.toLowerCase();

        
    //if statement to compare the dates and city and shape
    if((inputValue_sku == "" || inputValue_sku===name['sku']) && 
        (inputValue_discount == "" || inputValue_discount === name['priceoff']) && 
        (inputValue_stock == "" || inputValue_stock === name['quantity']) &&
        (inputValue_zip== "") || inputValue_zip ===name['zipcode'])
{
    //console.log(column)
     var td_tag=document.createElement('td');
     var td_text=document.createTextNode(name[column]);
    //console.log(td_text);
     td_tag.appendChild(td_text);
     //console.log(td_tag);
    tr_tag.appendChild(td_tag);
    
}
    
  });
 
  //console.log(tr_tag);
  tbody_tag.appendChild(tr_tag);

});
});