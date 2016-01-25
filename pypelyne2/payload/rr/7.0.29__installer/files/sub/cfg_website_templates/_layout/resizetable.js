
var objTh = null;
var objDiv = null;
var overColumn = false;
var overTable = false;
 
var iEdgeThreshold = 10;
 
function findPos(obj) {
  var curleft = curtop = 0;
  if (obj.offsetParent) {
      curleft = obj.offsetLeft;
      curtop = obj.offsetTop;
      while (obj = obj.offsetParent) {
         curleft += obj.offsetLeft;
         curtop += obj.offsetTop;
      }
   }
   return [curleft,curtop];
}
 
/* Function that tells me if on the right border or not */
function isOnBorderRight(elem,event){
  var width = elem.offsetWidth;
  var pos = findPos(elem);
  var absRight = pos[0] + width;
 
  if( event.clientX > (absRight - iEdgeThreshold) ){
      return true;
  }
 
  return false;
}
 
/* Function that tells me if on the bottom border or not */
function isOnBorderBottom(elem,event){
  var height = elem.offsetHeight;
 
  var pos = findPos(elem);
  var absTop = pos[1];
 
  if( event.clientY > (absTop + elem.offsetHeight - iEdgeThreshold) ){
      return true;
  }
  return false;
}
 
function getParentNode(objReference,nodeName,className){
   var oElement = objReference;
   while (oElement != null && oElement.tagName != null && oElement.tagName != "BODY") {
      if (oElement.tagName.toUpperCase() == nodeName && (className == null || oElement.className.search("\b"+className+"\b") != 1) ) {
         return oElement;
      }
      oElement = oElement.parentNode;
   }
   return null;
}
 
function doColumnResize(th,event){
    if(!event) event = window.event;
    if( isOnBorderRight(th,event)){ 
       overColumn=true;
       th.style.cursor="e-resize";
    }
    else{
       overColumn=false;
       th.style.cursor="";
    }
    return overColumn;
}
 
function doTableResize(div,event){
    if(!event) event = window.event;
 
    if( isOnBorderBottom(div,event)){ 
       div.style.cursor="move";
       overTable=true;
    }
    else{
       div.style.cursor="";
       overTable=false;
    }
    return overTable;
}
 
function doneTableResizing(){
   overTable=false;
}
 
function doneColumnResizing(){
   overColumn=false;
}
 
function MD(event) {
   if(!event) event = window.event;
 
   MOUSTSTART_X=event.clientX;
   MOUSTSTART_Y=event.clientY;
 
 
   if (overColumn){
 
       if(event.srcElement)objTh = event.srcElement;
       else if(event.target)objTh = event.target;
       else return;
 
       objTh = getParentNode(objTh,"TH");
       if(objTh == null) return;
       objTable = getParentNode(objTh,"TABLE");
       objThWidth=parseInt(objTh.style.width);
       objTableWidth=parseInt(objTable.offsetWidth);
   }
   else if(overTable){
       if(event.srcElement)objDiv = event.srcElement;
       else if(event.target)objDiv = event.target;
       else return;
 
       objDiv = getParentNode(objDiv,"DIV","scrollable");
 
       if(objDiv == null)return;
       objDivHeight=objDiv.offsetHeight;
       objTbodyHeight=objDiv.getElementsByTagName('TBODY')[0].offsetHeight;
   }
}
 
function MM(event) {
    if(!event) event = window.event;
 
    if (objTh) {
        var thSt=event.clientX-MOUSTSTART_X+objThWidth;
        var tableSt=event.clientX-MOUSTSTART_X+objTableWidth;
 
        /* check for minimum width */
        if(thSt>=10){
            objTh.style.width=thSt;
            objTable.style.width=tableSt;
        }
        if(document.selection) document.selection.empty();
        else if(window.getSelection)window.getSelection().removeAllRanges();
    }
    else if( objDiv ){
 
        var divSt=event.clientY-MOUSTSTART_Y+objDivHeight;
        var tbodySt = event.clientY-MOUSTSTART_Y+objTbodyHeight;
 
 
        /* check for minimum height */
        if(divSt >=70 ){
 
            var tbody = objDiv.getElementsByTagName('TBODY')[0];
            var table = objDiv.getElementsByTagName('TABLE')[0];
 
            /* adjust the height for mozilla, this is not needed for IE */
            if(tbodySt >= tbody.scrollHeight)tbodySt=tbody.scrollHeight;
            tbody.style.height=tbodySt;
 
            /* adjust the height for IE, this is not needed more Mozilla */
            if(divSt >= table.scrollHeight)divSt=table.scrollHeight;
            objDiv.style.height=divSt;
        }
        if(document.selection) document.selection.empty();
        else if(window.getSelection)window.getSelection().removeAllRanges();
    }
}
 
function MU(event) {
    if(!event) event = window.event;
    if(objTh){
        if(document.selection) document.selection.empty();
        else if(window.getSelection)window.getSelection().removeAllRanges();
        objTh = null;
    }
    else if( objDiv ){
        if(document.selection) document.selection.empty();
        else if(window.getSelection)window.getSelection().removeAllRanges();
        objDiv = null;
    }
}
 
document.onmousedown = MD;
document.onmousemove = MM;
document.onmouseup = MU;
