"use strict";
const $ = id => document.getElementById(id);
const KEY = "cetys.graph.editor.v1";
const categories = ["cruce","entrada","salon","laboratorio","bano","comida","escalera","elevador","rampa","otro"];
const types = ["pasillo","sendero","escalera","elevador","rampa"];
const seed = [
["iOS lab",32.505466272730324,-116.9246645749568,"laboratorio"],
["Cafetería",32.50578344907374,-116.9245173616592,"comida"],
["CECE 2",32.505974471951035,-116.92374581691023,"otro"],
["Baño CECE",32.50605804433695,-116.92384314480552,"bano"],
["Baño administrativo",32.505540457116126,-116.92477443434825,"bano"],
["Baño E4",32.5053044959788,-116.92364268473547,"bano"],
["Juice N Joy",32.5051333068815,-116.92359715209908,"comida"],
["Salón heterogéneas",32.50575049717793,-116.92488192328878,"salon"]
];
function initialGraph(){return {version:1,cost_unit:"metros",nodes:seed.map((n,i)=>({id:"n"+(i+1),name:n[0],lat:n[1],lng:n[2],category:n[3],building:"Por verificar",floor:0,notes:"Ubicación original. Verificar edificio y piso."})),edges:[]};}
function validateGraph(g){
 const fail = message => {throw new Error(message);};
 if(!g || g.version!==1 || g.cost_unit!=="metros" || !Array.isArray(g.nodes) || !Array.isArray(g.edges)) fail("Formato inválido: se requiere versión 1, cost_unit metros, nodes y edges.");
 const ids = new Set(), edgeIds = new Set();
 const string = v => typeof v==="string" && v.trim().length>0;
 for(const n of g.nodes){
  if(!n || !string(n.id) || ids.has(n.id) || !string(n.name) || !string(n.building) || !Number.isInteger(n.floor) || !Number.isFinite(n.lat) || Math.abs(n.lat)>90 || !Number.isFinite(n.lng) || Math.abs(n.lng)>180 || !categories.includes(n.category) || typeof n.notes!=="string") fail("Hay un nodo inválido o un identificador repetido.");
  ids.add(n.id);
 }
 for(const e of g.edges){
  if(!e || !string(e.id) || edgeIds.has(e.id) || !ids.has(e.source) || !ids.has(e.target) || e.source===e.target || !Number.isFinite(e.cost) || e.cost<0 || !types.includes(e.type) || ![true,false,null].includes(e.accessible) || typeof e.bidirectional!=="boolean") fail("Hay una conexión inválida; revisa extremos, costo y atributos.");
  if(e.type==="escalera" && e.accessible!==false) fail("Las escaleras deben marcarse como no accesibles.");
  const a=g.nodes.find(n=>n.id===e.source), b=g.nodes.find(n=>n.id===e.target);
  if(a.floor!==b.floor && !["escalera","elevador","rampa"].includes(e.type)) fail("Una conexión entre pisos debe ser escalera, elevador o rampa.");
  edgeIds.add(e.id);
 }
 return g;
}
let graph=initialGraph(), selected=null, selectedEdge=null, placing=false, map, layers;
let startup="Selecciona un lugar o activa Colocar nodos. Datos iniciales pendientes de verificar.";
try{const saved=localStorage.getItem(KEY);if(saved){graph=validateGraph(JSON.parse(saved));startup="Borrador recuperado del navegador.";}}catch(error){startup="No se pudo recuperar el borrador. "+error.message;}
function status(message){$("status").textContent=message;}
function persist(message){
 try{localStorage.setItem(KEY,JSON.stringify(graph));status(message+" · Borrador guardado.");}
 catch{status(message+" · No se pudo guardar en el navegador. Exporta JSON para conservarlo.");}
}
function id(prefix,items){let i=1;while(items.some(x=>x.id===prefix+i))i++;return prefix+i;}
function option(select,value,label){select.add(new Option(label,value));}
function fillNodes(select,empty){
 const previous=select.value;select.replaceChildren();if(empty)option(select,"",empty);
 graph.nodes.forEach(n=>option(select,n.id,n.name+" · "+n.building+" · P"+n.floor+" ["+n.id+"]"));
 if([...select.options].some(o=>o.value===previous))select.value=previous;
}
function nodeName(id){return graph.nodes.find(n=>n.id===id)?.name || id;}
function refresh(){
 const previous=$("floor").value;$("floor").replaceChildren();option($("floor"),"","Todos los pisos");
 [...new Set(graph.nodes.map(n=>n.floor))].sort((a,b)=>a-b).forEach(f=>option($("floor"),String(f),"Piso "+f));
 if([...$("floor").options].some(o=>o.value===previous))$("floor").value=previous;
 fillNodes($("node-select"),"Selecciona un nodo");$("node-select").value=selected||"";
 fillNodes($("source"),"Elige origen");fillNodes($("target"),"Elige destino");
 $("edge-select").replaceChildren();option($("edge-select"),"","Nueva conexión");
 graph.edges.forEach(e=>option($("edge-select"),e.id,nodeName(e.source)+(e.bidirectional?" ↔ ":" → ")+nodeName(e.target)+" · "+e.type));
 $("edge-select").value=selectedEdge||"";
 $("counts").textContent=graph.nodes.length+" nodos · "+graph.edges.length+" conexiones";
 render();
}
function render(){
 if(!map)return;layers.clearLayers();
 const floor=$("floor").value,visible=n=>floor===""||n.floor===Number(floor);
 graph.edges.forEach(e=>{
  const a=graph.nodes.find(n=>n.id===e.source),b=graph.nodes.find(n=>n.id===e.target);
  if(!visible(a)&&!visible(b))return;
  const color=e.id===selectedEdge?"#e49a14":(["escalera","elevador","rampa"].includes(e.type)?"#8854ba":"#526f83");
  const opts={color,weight:e.id===selectedEdge?7:4,dashArray:e.accessible===true?null:"7 6",bubblingMouseEvents:false};
  const line=(a.lat===b.lat&&a.lng===b.lng)?L.circleMarker([a.lat,a.lng],{...opts,radius:17,fill:false}):L.polyline([[a.lat,a.lng],[b.lat,b.lng]],opts);
  const tip=document.createElement("span");tip.textContent=nodeName(e.source)+(e.bidirectional?" ↔ ":" → ")+nodeName(e.target)+" · "+e.type+" · "+e.cost+" m";
  line.bindTooltip(tip).on("click",()=>selectEdge(e.id)).addTo(layers);
 });
 graph.nodes.filter(visible).forEach(n=>{
  const marker=L.marker([n.lat,n.lng],{draggable:!placing,bubblingMouseEvents:false,icon:L.divIcon({className:"",html:'<div class="node-dot'+(selected===n.id?' selected':'')+'"></div>',iconSize:[22,22],iconAnchor:[11,11]})});
  const tip=document.createElement("span");tip.textContent=n.name+" · Piso "+n.floor;
  marker.bindTooltip(tip).on("click",()=>selectNode(n.id)).on("dragend",event=>{
   const p=event.target.getLatLng();n.lat=p.lat;n.lng=p.lng;selectNode(n.id);refresh();persist("Ubicación actualizada; revisa los costos de sus conexiones.");
  }).addTo(layers);
 });
}
function selectNode(nodeId,pan=false){
 selected=nodeId||null;const n=graph.nodes.find(n=>n.id===selected);
 $("node-select").value=selected||"";
 if(!n){$("node-form").reset();$("node-id").textContent="Sin selección";render();return;}
 $("node-id").textContent="Identificador: "+n.id;
 for(const [field,key] of [["name","name"],["building","building"],["level","floor"],["category","category"],["lat","lat"],["lng","lng"],["notes","notes"]])$(field).value=n[key];
 if(pan&&map){$("floor").value=String(n.floor);map.panTo([n.lat,n.lng]);}
 render();
}
function selectEdge(edgeId){
 selectedEdge=edgeId||null;$("edge-select").value=selectedEdge||"";
 const e=graph.edges.find(e=>e.id===selectedEdge);
 if(e){$("source").value=e.source;$("target").value=e.target;$("type").value=e.type;$("cost").value=e.cost;$("accessible").value=e.accessible===null?"unknown":e.accessible?"yes":"no";$("bidirectional").checked=e.bidirectional;}
 else{$("edge-form").reset();}
 $("accessible").disabled=$("type").value==="escalera";render();
}
$("browse").onclick=()=>setMode(false);$("place").onclick=()=>setMode(true);
function setMode(value){placing=value;$("place").classList.toggle("active",value);$("browse").classList.toggle("active",!value);if(map)map.getContainer().style.cursor=value?"crosshair":"";render();status(value?"Haz clic en el mapa para crear un nodo.":"Selecciona un nodo o una conexión para editarlo.");}
$("floor").onchange=render;
$("node-select").onchange=()=>selectNode($("node-select").value,true);
$("edge-select").onchange=()=>selectEdge($("edge-select").value);
$("node-form").onsubmit=event=>{
 event.preventDefault();if(!selected){status("Primero coloca o selecciona un nodo.");return;}
 const previous=graph.nodes.find(n=>n.id===selected);
 const updated={...previous,name:$("name").value.trim(),building:$("building").value.trim(),floor:Number($("level").value),category:$("category").value,lat:Number($("lat").value),lng:Number($("lng").value),notes:$("notes").value};
 const candidate={...graph,nodes:graph.nodes.map(n=>n.id===selected?updated:n)};
 try{validateGraph(candidate);}catch(error){status(error.message);return;}
 graph=candidate;refresh();selectNode(selected,true);persist("Nodo actualizado.");
};
$("delete-node").onclick=()=>{
 if(!selected)return;
 const count=graph.edges.filter(e=>e.source===selected||e.target===selected).length;
 if(!confirm("¿Eliminar "+nodeName(selected)+" y sus "+count+" conexiones?"))return;
 graph.edges=graph.edges.filter(e=>e.source!==selected&&e.target!==selected);graph.nodes=graph.nodes.filter(n=>n.id!==selected);
 selectNode(null);selectEdge(null);refresh();persist("Nodo eliminado.");
};
$("type").onchange=()=>{const stairs=$("type").value==="escalera";$("accessible").disabled=stairs;if(stairs)$("accessible").value="no";};
$("estimate").onclick=()=>{
 const a=graph.nodes.find(n=>n.id===$("source").value),b=graph.nodes.find(n=>n.id===$("target").value);
 if(!a||!b||a.id===b.id){status("Selecciona dos nodos distintos.");return;}
 const rad=x=>x*Math.PI/180,dlat=rad(b.lat-a.lat),dlng=rad(b.lng-a.lng);
 const h=Math.sin(dlat/2)**2+Math.cos(rad(a.lat))*Math.cos(rad(b.lat))*Math.sin(dlng/2)**2;
 $("cost").value=(6371000*2*Math.asin(Math.sqrt(Math.min(1,h)))).toFixed(2);
 status("Distancia horizontal estimada. Ajusta al recorrido real; no incluye desnivel.");
};
$("edge-form").onsubmit=event=>{
 event.preventDefault();
 const edge={id:selectedEdge||id("e",graph.edges),source:$("source").value,target:$("target").value,type:$("type").value,cost:Number($("cost").value),accessible:$("accessible").value==="unknown"?null:$("accessible").value==="yes",bidirectional:$("bidirectional").checked};
 const candidate={...graph,edges:selectedEdge?graph.edges.map(e=>e.id===selectedEdge?edge:e):[...graph.edges,edge]};
 try{validateGraph(candidate);}catch(error){status(error.message);return;}
 graph=candidate;selectedEdge=edge.id;refresh();persist("Conexión guardada.");
};
$("delete-edge").onclick=()=>{
 if(!selectedEdge)return;if(!confirm("¿Eliminar esta conexión?"))return;
 graph.edges=graph.edges.filter(e=>e.id!==selectedEdge);selectEdge(null);refresh();persist("Conexión eliminada.");
};
$("export").onclick=()=>{
 const url=URL.createObjectURL(new Blob([JSON.stringify(graph,null,2)],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download="grafoCETYS.json";document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 status("JSON exportado con los últimos cambios guardados en los formularios.");
};
$("import").onchange=async event=>{
 const file=event.target.files[0];if(!file)return;
 try{
  const candidate=validateGraph(JSON.parse(await file.text()));
  if(!confirm("¿Reemplazar el grafo actual por el archivo importado? Exporta primero si necesitas un respaldo."))return;
  graph=candidate;selected=null;selectedEdge=null;$("floor").value="";refresh();selectNode(null);selectEdge(null);
  if(map&&graph.nodes.length)map.fitBounds(graph.nodes.map(n=>[n.lat,n.lng]),{maxZoom:18,padding:[30,30]});
  persist("Grafo importado.");
 }catch(error){status("No se importó el archivo: "+error.message);}
 finally{event.target.value="";}
};
if(typeof L!=="undefined"){
 map=L.map("map",{maxZoom:22}).setView([32.5055,-116.9242],18);
 L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{maxNativeZoom:19,maxZoom:22,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map).on("tileerror",()=>status("No se pudo cargar el mapa base. Revisa tu conexión; puedes seguir editando los datos."));
 layers=L.layerGroup().addTo(map);
 map.on("click",event=>{
  if(!placing)return;
  const node={id:id("n",graph.nodes),name:"Nuevo nodo",building:"Por verificar",floor:$("floor").value===""?0:Number($("floor").value),category:"cruce",lat:event.latlng.lat,lng:event.latlng.lng,notes:""};
  graph.nodes.push(node);selected=node.id;refresh();selectNode(node.id);persist("Nodo creado. Completa sus características y pulsa Guardar nodo.");
 });
 refresh();status(startup);
}else{refresh();status("No se pudo cargar Leaflet. Conéctate a internet y recarga para usar el mapa. La importación y exportación siguen disponibles.");}

