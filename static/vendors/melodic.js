"use strict";
/*!
 * Melodic JavaScript Library v1.0a
 * http://github.com/shiroyuki/melodic-js
 *
 * Copyright 2014 Juti Noppornpitak
 * Released under the MIT license
 * See https://github.com/shiroyuki/melodic-js/blob/master/LICENSE
 */
;var EventEmitter=function(){};$.extend(EventEmitter.prototype,{_useTimestamp:false,_lastKnownIdentifier:0,EventEmitter:function(a){this.uniqueIdentifier=a||null},getEventUniqueIdentifier:function(){if(typeof this.uniqueIdentifier===undefined){this.uniqueIdentifier=this._useTimestamp?(new Date()).getTime():++this._lastKnownIdentifier}},getActualEventType:function(a){return[this.getEventUniqueIdentifier(),a].join(".")},addEventListener:function(b,c){var a=this.getActualEventType(b);document.addEventListener(a,c)},on:function(a,b){this.addEventListener(a,b)},dispatchEvent:function(b,c){var a=this.getActualEventType(b);c=c||{};var d=new CustomEvent(a,{origin:this,userData:c});document.dispatchEvent(d)},emit:function(a,b){this.dispatchEvent(a,b)},raise:function(a){throw a}});"use strict";
/*!
 * Melodic JavaScript Library v1.0a
 * http://github.com/shiroyuki/melodic-js
 *
 * Copyright 2014 Juti Noppornpitak
 * Released under the MIT license
 * See https://github.com/shiroyuki/melodic-js/blob/master/LICENSE
 */
;var EditableWidget=function(a){a=a||{};this.subSelectorForActivator="[data-widget*=editable]";this.subSelectorForInput=this.subSelectorForActivator+" + .form-control"};$.extend(EditableWidget.prototype,EventEmitter.prototype);EditableWidget.prototype.onActivatorClick=function(c){var a=$(c.currentTarget),d=a.next(),b={"font-size":a.css("font-size"),"margin-top":a.css("margin-top"),"margin-left":a.css("margin-left"),"margin-right":a.css("margin-right"),"margin-bottom":a.css("margin-bottom")};c.preventDefault();a.addClass("active");d.css(b).val(a.text()).focus()};EditableWidget.prototype.onPressUpdateOrResetData=function(d){var f=$(d.currentTarget),a=f.prev(),b=a.text(),c=$.trim(f.val());switch(d.keyCode){case 13:a.html(c);a.removeClass("active");this.emit("editable.updated",{element:a,oldValue:b,newValue:c});break;case 27:f.val(b);a.removeClass("active");this.emit("editable.cancelled",{element:a,oldValue:b,newValue:c});break}};EditableWidget.prototype.initialize=function(a){a=a||{};$(document).on("click",this.subSelectorForActivator,$.proxy(this.onActivatorClick,this));$(document).on("keyup",this.subSelectorForInput,$.proxy(this.onPressUpdateOrResetData,this))};EditableWidget.prototype.apply=function(a){a=a||{};if(!a.hasOwnProperty("selector")){a.selector=document}$(a.selector).find(this.subSelectorForActivator).each(function(d){var b=$(this),c=this.nodeName.toLowerCase(),e=b.data("placeholder");if(c.match(/^(h\d|span)$/)){b.after('<input type="text" class="form-control" data-element="'+c+'" placeholder="'+e+'"/>');return}else{if(c.match(/^(p|div|addr)$/)){b.after('<textarea class="form-control" data-element="'+c+'" placeholder="'+e+'"></textarea>')}}})};"use strict";
/*!
 * Melodic JavaScript Library v1.0a
 * http://github.com/shiroyuki/melodic-js
 *
 * Copyright 2014 Juti Noppornpitak
 * Released under the MIT license
 * See https://github.com/shiroyuki/melodic-js/blob/master/LICENSE
 */
;var WidgetManager=function(){this.widgetMap={editable:null}};$.extend(WidgetManager.prototype,EventEmitter.prototype,{use:function(b,a){this.enable(b,a)},enable:function(b,a){var c=b.replace(/^./,function(d){return d.toUpperCase()})+"Widget";if(!window.hasOwnProperty(c)){this.raise("melodicjs.widget_manager.enable.error")}if(!this.widgetMap[b]){this.widgetMap[b]=new window[c](a);this.widgetMap[b].initialize(a)}},get:function(a){if(!this.widgetMap[a]){this.raise("melodicjs.widget_manager.get.error")}return this.widgetMap[a]}});
