function calculate() {
  var category_list = document.querySelectorAll(".category");

  for (var i = 0; i < category_list.length; i++) {
    var x = category_list[i].querySelector("#current").innerHTML.slice(1);
    var y = category_list[i].querySelector("#spent").innerHTML.slice(1);
    var z = parseFloat(x - y).toFixed(2);
    category_list[i].querySelector("#result").innerHTML = "$" + z;
  }
}
