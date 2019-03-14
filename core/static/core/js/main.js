//---------------------------------------------Модальное окно выбора иконки
function showModalWin() {
 
    var darkLayer = document.createElement('div'); // слой затемнения
    darkLayer.id = 'shadow'; // id чтобы подхватить стиль
    document.body.appendChild(darkLayer); // включаем затемнение
    
    var modalWin = document.getElementById('openIcons'); // находим наше "окно"
    modalWin.style.display = 'block'; // "включаем" его

    darkLayer.onclick = function () {  // при клике на слой затемнения все исчезнет
        darkLayer.parentNode.removeChild(darkLayer); // удаляем затемнение
        modalWin.style.display = 'none'; // делаем окно невидимым
        return false;
    };
}

function iconSelect(id_obj, path, obj) {
    id_obj.value = path ;
    id_obj.attributes.nodeValue = path ;
    im_icon.src = obj.attributes.src.nodeValue ;
    var modalWin = document.getElementById('openIcons');
    var darkLayer = document.getElementById('shadow');
    darkLayer.parentNode.removeChild(darkLayer);
    modalWin.style.display = 'none';
}

//----------------------------------------------- Просмоторщик фотогалереи
// Определяем все ссылки со св-вом  rel=slide
var galleryAlbum = [] ;
var albomIndex = 0 ;
var albomSubIndex = 0 ;
var currentData = [] ;
let linkNodes = document.querySelectorAll('img[rel=slide]') ; // находим все ссылки с rel=slide
let slideLinks = [].slice.call(linkNodes) ;
slideLinks.forEach(link=>{ 
    link.addEventListener('click', function(evt){ // вешаем на каждую обработчик
    createGalleryBoxViewBody(evt.currentTarget) ;}) // вызываем окно показа изображений
  galleryAlbum.push(link.dataset.prodid)
})

function createGalleryBoxViewBody(link) {
    var container = document.createElement('div') ;
    container.innerHTML = '<div id="galleryBox_view" class="galleryBox"> \
        <div class="galleryBox_content"> \
            <span id="close_galleryBox" onclick="closeGalleryBox()">&times;</span> \
            <div id="layer_image" ><img src="" name="slide" data-prodid=""> \
            <div class="sl-nav"><a class="sl-prev" onclick="prevSlide()"></a><a class="sl-next" onclick="nextSlide()"></a></div> \
            <div class="sl-loader" name="loader"><a class="sl-cancel"></a></div></div> \
            <div id="layer_discr" ><div id="discription" ></div> \
            <form id="getproduct" action=""><button>Запросить</button></from></div> \
            </div> \
        </div>' ;
    document.body.appendChild(container.firstChild) ;
    getproddata(link.dataset.prodid).then(function(data){
        insertDataGalleryBox(data, link.dataset.prodid) ;
        currentData = data ;
    });
}

function closeGalleryBox() {
    let galleryBox = document.getElementById("galleryBox_view");
    if (galleryBox) { galleryBox.remove() ; }
    return true ;
}

function insertDataGalleryBox(data, id) {
    albomSubIndex = 0 ;
    let discription_text = document.getElementById("discription") ;
    let description = data.description ;
    let image = data.images ;
    slideTeg = document.getElementsByTagName('img').slide ;
    loader = document.getElementsByTagName('div').loader ;
    slideTeg.src = image[0] ;
    slideTeg.dataset.prodid = id ;
    loader.style.display = "none" ;
    discription_text.innerHTML = description ;
    getProduct(id)
}

window.onclick = function(event) {
    if (event.target == document.getElementById("galleryBox_view")) {
        closeGalleryBox();
    }
}

function nextSlide() {
    var slideTeg = document.getElementsByTagName('img').slide ;
    var prodid = slideTeg.dataset.prodid ;
    var albomIndex = galleryAlbum.indexOf(prodid) ;
    let image = currentData.images ;
    if (image.length > 1 && albomSubIndex < (image.length-1)) {
        albomSubIndex += 1;
        slideTeg.src = image[albomSubIndex] ;
    }
    else {
        albomIndex += 1 ;
        if (albomIndex === galleryAlbum.length) { return ;}
        albomSubIndex = 0 ;
        prodid = galleryAlbum[albomIndex] ;
        getproddata(prodid).then(function(data){
            insertDataGalleryBox(data, prodid) ;
            currentData = data ;
        });
    }
}

function prevSlide() {
    var slideTeg = document.getElementsByTagName('img').slide ;
    var prodid = slideTeg.dataset.prodid ;
    var albomIndex = galleryAlbum.indexOf(prodid) ;
    let image = currentData.images ;
    if (image.length > 1 && (albomSubIndex <= (image.length-1) && albomSubIndex > 0)) {
        albomSubIndex -= 1;
        slideTeg.src = image[albomSubIndex] ;
    }
    else {
        if (albomIndex === 0) { return ;}
        albomIndex -= 1 ;
        albomSubIndex = 0 ;
        prodid = galleryAlbum[albomIndex] ;
        getproddata(prodid).then(function(data){
            insertDataGalleryBox(data, prodid) ;
            currentData = data ;
        });
    }
}

function getProduct(id) {
    let link = "/main/katalog/product/" +id ;
    form = document.getElementById("getproduct") ;
    form.action = link ;
}

//-----------------------------------------------
// ajax запросы
function status(response) {  
  if (response.status >= 200 && response.status < 300) {  
    return Promise.resolve(response)  
  } else {  
    return Promise.reject(new Error(response.statusText))  
  }  
}

function json(response) {  
  return response.json()  
}

function getproddata(prod_id) {
    return fetch(prod_id)  
      .then(status)  
      .then(json)  
      .then(function(data) {  
        console.log('Request succeeded with JSON response', data);
        return data;
      }).catch(function(error) {  
        console.log('Request failed', error);  
      });
}
//-----------------------------------------------