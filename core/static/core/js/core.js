var imgsID = [];
var err_fields = [];

const form = document.getElementById('contact');

if (form) {
  form.addEventListener('submit',  send);
}

var slides = [].slice.call(document.querySelectorAll('a[rel=slide]')) ;

if (slides) {
  slides.forEach(link=>{
    link.addEventListener('click', function(evt){
      evt.preventDefault();
      showGalleryObject(link.href, Number.parseInt(link.dataset.img_id));})
  })
}

get_array_thumbs();



var arrow = document.getElementsByClassName("icon-right");
if (arrow.length > 0) {
  document.onkeydown = NavigateThrough;
  function NavigateThrough (event) {

    switch (event.keyCode ? event.keyCode : event.which ? event.which : null) {

      // previous_page
      case 0x25:
        nextSlide(0);
        break;
      // next_page
      case 0x27:
        nextSlide(1);
        break;
        }
      }
    }











// Получаем список превьюшек галереи и назначаем функцию заполнения ссылок на основное изображение
function get_array_thumbs() {
  imgsID = [];
  var imgIDNodes = document.querySelectorAll('img[rel=thumb]') ;
  var imgIDList = [].slice.call(imgIDNodes) ;
  imgIDList.forEach(link=>{ 
      link.addEventListener('click', function(evt){ // вешаем на каждую обработчик
      get_img(link.dataset.img_id) ;})
    imgsID.push(link.dataset.img_id)
  })
}

// Универсальная функция обработки ajax запроса
function ajaxGET(url, callback) {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      var status = request.status;
      if (status == 200) {
        callback(request.responseText);
      }
    }
  };

  request.open("GET", url);
  request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  request.send();
}


function ajaxPOST(url, data, callback) {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState == 4) {
      var status = request.status;
      callback(status, request.responseText);
    }
  };

  request.open("POST", url, true);
  request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  request.send(data);
}

// Замена url картинки в просмотре
function changeSlide(url, id) {
  var img = document.getElementById("slide");
  img.src = url;
  img.dataset.img_id = id;
  var thumb_active = document.querySelector(`[class="thumb-active"][rel="thumb"]`);
  if (thumb_active) {
    thumb_active.classList.remove("thumb-active");
  }
  var thumb = document.querySelector(`[data-img_id="${id}"][rel="thumb"]`);
  if (thumb) {
    thumb.classList.add("thumb-active");
  }
}

// Создаёт блок для просмотра фотографий галереи
function createGalleryView(data) {

  var container = document.createElement("div");
  var main= document.getElementsByTagName("main")[0];
  container.innerHTML = data;
  main.appendChild(container.firstChild);
  listKeys = true;
  get_array_thumbs();
}

// Получаем url картинки по id из БД
function get_img(id) {

  var id = id;
  var get_img_url = "/pl/get/" + id;
  ajaxGET(get_img_url, function(url) {
    changeSlide(url, id);
  });
}

// Выводит просмотр галереи
function showGalleryObject(link, id) {

  current_photoobj = id;
  ajaxGET(link, createGalleryView);
  return false;
}

// Закрывает галерею
function closeGalleryObject() {

  listKeys = false;
  var back_wrap = document.getElementById("back_wrap");
  if (back_wrap) { back_wrap.remove(); }
}

// Подсталвяет следующий слайд в главное окно просмотра
function nextSlide(step) {
  var img = document.getElementById("slide");
  var imgsIDLen = imgsID.length - 1;
  var index = imgsID.indexOf(img.dataset.img_id);
  if (step == 1) {
    if (index == imgsIDLen) { nextPhotoObj(1); }
    else  { get_img(imgsID[index+1]); }
  }
  if (step == 0) {
    if (index == 0) { nextPhotoObj(0); }
    else  { get_img(imgsID[index-1]); }
  }
}

// Переход к следующему объекту
function nextPhotoObj(step) {
  if (typeof current_photoobj == "undefined") { return };
  var index = context_list.indexOf(current_photoobj);
  var cl_len = context_list.length - 1;
  var nextIndex = (step == 1) ? (index+1) : (index-1);
  
  if (nextIndex>=0 && nextIndex<=cl_len) {
    var link = url_get + context_list[nextIndex];
  } else { return undefined; }
  
  if (url_type == "noajax") {
    document.location.href = link;
  }
  if (url_type == "ajax") {
    ajaxGET(link, function(data) {
      current_photoobj = context_list[nextIndex];
      document.getElementById("back_wrap").outerHTML = data;
      get_array_thumbs();
    });
  }
}

// Отправка сообщения формы обратной связи
function send(event) {

  event.preventDefault();

  var form = event.target;
  var url = form.action;
  var data = new FormData(form);

  ajaxPOST(url, data, function(status, data) {
    data = JSON.parse(data);
    if (status == 200) {
      form.reset();
      if (err_fields.length > 0) {
        err_fields.forEach(key=>{
          form.elements.namedItem(key).classList.remove("error");
          err_fields = [];
        })
      }
      alert(data.message);
    }
    if (status == 400) {
      Object.keys(data).forEach(key=>{
        form.elements.namedItem(key).classList.add("error");
        err_fields.push(key);
        alert("Не правильно заполнены поля");
      })
    }
  });
}

