var w_width;

(function() {
  window.onresize = displayWindowSize;
  window.onload = displayWindowSize;

  function displayWindowSize() {
    w_width = window.innerWidth;
    let window_height = window.innerHeight;
  };
});

$(document).ready(function(){

list_a = ['#first-el-header', '#second-el-header', '#third-el-header', '#fourth-el-header', '#fifth-el-header']
icon_list = ['#edit-ico', '#add-image-ico', '#add-attach-ico', '#dok-ico', '#add-contact-ico']
target_a_1 = list_a[0]

function layout(icona, target, list_el){
  break_width = 1055
  $(icona).click(function(){
    $(target).css('display', 'block');
    for (el = 0; el < list_el.length; el++){
      if (target != list_el[el]){
        $(list_el[el]).css("display", "none");
      };
    };
    if (w_width <= break_width){
      $([document.documentElement, document.body]).animate({
          scrollTop: $(target).offset().top
      }, 200);
    };
  });
};

for (i = 0; i <= list_a.length; i++){
  layout(icon_list[i], list_a[i], list_a)
}

$(".hide-el").click(function(){
  for (i = 0; i <= list_a.length; i++){
    $(list_a[i]).css('display', 'none');
  };
  $([document.documentElement, document.body]).animate({
      scrollTop: $(document.body).offset().top
  }, 200);
});

/* DO POPORAWIENIA
classes_arg = ['.is-index-check', '#addpage_form', '.remove_page'];

function toggle_classes_menu(source, state, appen){
 classes_arg = ['.is-index-check', '#addpage_form', '.remove_page'];
  $(classes_arg[0], classes_arg[1]).css('display', 'none');
   $(appen + '3', appen + '2').remove()
  if ( $(source).hasClass(state) ){
    $(classes_arg[2]).css('display', 'none');
      $(source).removeClass(state);
    $(appen).remove();
  }
  else{
    $(source).addClass(state);
     $(classes_arg[2]).css('display', 'block');
     $(source).append('<span id='+ appen +'> &uarr; <span>');
  }
};

f_class_arg = '#removep'
s_class_arg = '#addpage'
t_class_arg = '#adisindex'
state_arg = '#clicked-once'
var append = "#appended"

toggle_classes_menu(f_class_arg, state_arg, append);
*/

$("#removep").click(function() {
    $(".is-index-check, #addpage_form").css('display', 'none');
    $('#appended3, #appended2').remove();
    if ($('#removep').hasClass("clicked-once")) {
			   $('.remove_page').css("display" , "none");
			     $('#removep').removeClass("clicked-once");
      $('#appended').remove();
    }
    else {
			$('#removep').addClass("clicked-once");
			  $('.remove_page').css("display" , "block");
          $("#removep").append("<span id='appended'> &uarr;<span>");
    }
});

$("#addpage").click(function() {
    $(".is-index-check, .remove_page").css('display', 'none');
    $('#appended3, #appended').remove();
    if ($('#addpage').hasClass("clicked-once")) {
			     $('#addpage_form').css("display" , "none");
			        $('#addpage').removeClass("clicked-once");
      $('#appended2').remove();
    }
    else {
			$('#addpage').addClass("clicked-once");
        $("#addpage").append("<span id='appended2'> &uarr;</span>");
			     $('#addpage_form').css("display" , "inline-block");
    }
});


$("#adisindex").click(function() {
    $("#addpage_form, .remove_page").css('display', 'none');
    $('#appended2, #appended').remove();
    if ($('#adisindex').hasClass("clicked-once")) {
      var x = $('.is-index-check');
      var i;
      for (i = 0; i < x.length; i++) {
          x[i].style.display = 'none';
       }
			$('#adisindex').removeClass("clicked-once");
      $('#appended3').remove();
    }
    else {
			$('#adisindex').addClass("clicked-once");
      $("#adisindex").append("<span id='appended3'> &uarr;</span>");
      var x = $('.is-index-check');
      var i;
      for (i = 0; i < x.length; i++) {
          x[i].style.display = 'inline-block';
       }
    }
  });
//sortable for menu
$(function(){
  $('#sortable').sortable({
      tolerance: "pointer",
      distance: 5,
      update: function(event,ui) {
        var postData = $(this).sortable('serialize');

        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(postData),
            dataType: 'json',
            url: '/sort'
        });
      }
  });
}); //end sortable
//sortable-grid for posts vertiacal
$(function(){
  $('#sortable-grid').sortable({
      tolerance: "pointer",
      distance: 5,
      revert: true,
      update: function(event,ui) {
        var postData = $(this).sortable('serialize');

       var pathname = window.location.pathname.match(/\d+/)[0];
       var adres = pathname;
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(postData),
            dataType: 'json',
            url: /sortgrid/ + adres
        });
      }
  });
}); //end sortable-grid

 }); //end document ready

 var class1_1 = 'pure-u-1';
 var class1_2 = 'pure-u-lg-1-2';
 var class1_3 = 'pure-u-lg-1-3';
 var class1_4 = 'pure-u-lg-1-4';
 var class1_5 = 'pure-u-lg-1-5';
 var class2_3 = 'pure-u-lg-2-3';
 var class4_5 = 'pure-u-lg-4-5';
 var class3_4 = 'pure-u-lg-3-4';

function lay(sourceElem, index) {
  var klasa = '';
  $("#item_" + sourceElem).removeClass();
  if (index == 1) {
    var klasa = class1_1;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 2) {
    var klasa = class1_2;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 3) {
    klasa = class1_3;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 4) {
    klasa = class1_4;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 5) {
    klasa = class1_5;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 6) {
    klasa = class2_3;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 7) {
    klasa = class4_5;
    $("#item_" + sourceElem).addClass(klasa);
  } else if (index == 8) {
    klasa = class3_4;
    $("#item_" + sourceElem).addClass(klasa);
  }
    $.ajax({
    type: "POST",
    contentType: 'application/json',
    data: JSON.stringify(klasa),
    dataType: 'json',
    url: '/lay/' + sourceElem
});

}

function check(source, index) {
  var pathname = window.location.pathname.match(/\d+/)[0];
  var adres = pathname;
  var iD = source.toString();

  //console.log(pathname);


jQuery.each(index, function( i, val ){
  if (val == source){
     if ($("#item_"+ source +" ").hasClass('checked')){
            $("#item_"+ source +" ").removeClass('checked');
            $("#item_"+ source +" ").addClass('before-check');
     } else {
        $("#item_"+ source +" ").addClass('checked');
        $("#item_"+ source +" ").removeClass('before-check');
     }
  } else {
     if ($("#item_"+ val +" ").hasClass('checked')){
         $("#item_"+ val +" ").removeClass('checked');
         $("#item_"+ val +" ").removeClass('before-check');
     }else{
        $("#item_"+ val +" ").addClass('before-check');
   };
  };
});

  $.ajax({
    success: function(msg = iD){
      $("#baseLay").attr("href", "javascript: lay("+ iD + ',' + 1 +")");
      $("#firstLay").attr("href", "javascript: lay("+ iD + ',' + 2 +")");
      $("#secondLay").attr("href", "javascript: lay("+ iD + ',' + 3 +")");
      $("#thirdLay").attr("href", "javascript: lay("+ iD + ',' + 4 +")");
      $("#fourthLay").attr("href", "javascript: lay("+ iD + ',' + 5 +")");
      $("#fifthLay").attr("href", "javascript: lay("+ iD + ',' + 6 +")");
      $("#sixthLay").attr("href", "javascript: lay("+ iD + ',' + 7 +")");
      $("#seventhLay").attr("href", "javascript: lay("+ iD + ',' + 8 +")");
    },
    url: '/editpage/' + adres
  });
};

var classes = '.' + class1_1 + ', .' + class1_2 + ', .'
                  + class1_3 + ', .' + class1_4 + ', .'
                  + class1_5 + ', .' + class2_3 + ', .'
                  + class4_5 + ', .' + class3_4;

$('.content_container').click(function(){
  $(classes).removeClass('before-check');
  $(classes).removeClass('checked');
});


function oznacz(source){
  var klasa = 'marked-order';
  $("#order_" + source).addClass(klasa);

    $.ajax({
    type: "POST",
    contentType: 'application/json',
    data: JSON.stringify(klasa),
    dataType: 'json',
    url: '/oznacz/' + source
});
};

function odznacz(source){
  var klasa = 'unmarked-order';
  $("#order_" + source).removeClass();
    $.ajax({
    type: "POST",
    contentType: 'application/json',
    data: JSON.stringify(klasa),
    dataType: 'json',
    url: '/oznacz/' + source
});
};

var getnumer = '';
var getmiejsce = '';
var getopis = '';
var list = {};

function edit_order(source){
  var numer = $('#numer_' + source);
  var miejsce = $('#miejsce_' + source);
  var opis = $('#opis_' + source);

  numer.attr("contenteditable", "True").addClass('blink');
  miejsce.attr("contenteditable", "True").addClass('blink');
  opis.attr("contenteditable", "True").addClass('blink');


  $(document).on('keypress',function(e) {
    if(e.which == 13) {
      numer.attr("contenteditable", "False").removeClass('blink');
      miejsce.attr("contenteditable", "False").removeClass('blink');
      opis.attr("contenteditable", "False").removeClass('blink');
      getnumer = numer.html();
      getmiejsce = miejsce.html();
      getopis = opis.html();
      list = {numer:getnumer, miejsce:getmiejsce, opis:getopis}

      $.ajax({
      type: "POST",
      contentType: 'application/json',
      data: JSON.stringify(list),
      dataType: 'json',
      url: '/get_order/' + source
   });
  }
});
 }; //end of edit_order function


function save_order(source){

var numer = $('#numer_' + source);
var miejsce = $('#miejsce_' + source);
var opis = $('#opis_' + source);

   numer.attr("contenteditable", "False").removeClass('blink');
   miejsce.attr("contenteditable", "False").removeClass('blink');
   opis.attr("contenteditable", "False").removeClass('blink');
   getnumer = numer.html();
   getmiejsce = miejsce.html();
   getopis = opis.html();
   list = {numer:getnumer, miejsce:getmiejsce, opis:getopis}

   $.ajax({
   type: "POST",
   contentType: 'application/json',
   data: JSON.stringify(list),
   dataType: 'json',
   url: '/get_order/' + source
 });
    };

var lightbox = new SimpleLightbox('.light-img', { overlay:true, captions:false, spinner:false, });
$(function() {
  $( ".dtpick" ).datepicker({changeMonth:true, changeYear:true});
});

$.datepicker.regional.pl = {
closeText: "Zamknij",
prevText: "&#x3C;Poprzedni",
nextText: "Następny&#x3E;",
currentText: "Dziś",
monthNames: [ "Styczeń","Luty","Marzec","Kwiecień","Maj","Czerwiec",
"Lipiec","Sierpień","Wrzesień","Październik","Listopad","Grudzień" ],
monthNamesShort: [ "Sty","Lu","Mar","Kw","Maj","Cze",
"Lip","Sie","Wrz","Pa","Lis","Gru" ],
dayNames: [ "Niedziela","Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota" ],
dayNamesShort: [ "Nie","Pn","Wt","Śr","Czw","Pt","So" ],
dayNamesMin: [ "N","Pn","Wt","Śr","Cz","Pt","So" ],
weekHeader: "Tydz",
dateFormat: "dd.mm.yy",
firstDay: 1,
isRTL: false,
showMonthAfterYear: false,
yearSuffix: "" };

$.datepicker.setDefaults($.datepicker.regional.pl);
