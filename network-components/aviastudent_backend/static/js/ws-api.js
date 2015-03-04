function AviastudentWS(host)
{
//public methods
  //wifi
  // this.SetWiFi=function (name, password) {  this.socket.send(JSON.stringify({query: 'set_wifi', ssid: name, pass: password})) }
  // this.QueryWiFiList = function() {  this.socket.send(JSON.stringify({query: 'list_wifi'})) }
  //signal source
  // this.SetSignalSource = function(src)
  //                        {
  //                          if(src === 'mic' || src === 'ext' || src === 'airplay')
  //                            this.socket.send(JSON.stringify({query: 'set_source', source: src}))
  //                          else console.log('incorrect src, should be "mic", "ext", "airplay"');
  //                        }
  // //op.mode
  // this.SetMode = function(m)
  //                {
  //                  if(m === 'm1' || m === 'm2' ||m === 'm3' ||m === 'm4' ||m === 'm5' ||m === 'm6' ||m === 'm7'||m === 'm8'||m === 'm9'||m === 'm0'||m === 'test')
  //                    this.socket.send(JSON.stringify({query: 'set_mode', mode: m}));
  //                  else console.log('incorrect mode, should be "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m0", "test"');
  //                }
  // //visual. params
  // this.SetThreshold = function(tr)
  //                     {
  //                       if(tr>=100 && tr <= 1000)
  //                         this.socket.send(JSON.stringify({query: 'set_thres', thres: tr}));
  //                       else
  //                         console.log('incorrect threshold, should be > 100 && < 1000');
  //                     }
  // this.SetMinDelay = function(delay)
  //                    {
  //                      if(delay>=0 && delay <= 1000)
  //                        this.socket.send(JSON.stringify({query: 'set_mindelay', mindelay: delay}));
  //                      else
  //                        console.log('incorrect min delay, should be > 0 && < 1000');
  //                    }
  // this.SetFadeOutDelay = function(delay)
  //                        {
  //                          if(delay>=0 && delay <= 5000)
  //                            this.socket.send(JSON.stringify({query: 'set_fadeoutdelay', fadeoutdelay: delay}));
  //                          else
  //                            console.log('incorrect fadeoutdelay, should be > 0 && < 5000');
  //                        }
  // this.SetAllOffDelay = function(delay)
  //                        {
  //                          if(delay>=0 && delay <= 10000)
  //                            this.socket.send(JSON.stringify({query: 'set_alloffdelay', alloffdelay: delay}));
  //                          else
  //                            console.log('incorrect alloffdelay, should be > 0 && < 10000');
  //                        }
  // this.SetStartBrightness = function(br)
  //                           {
  //                             if(br>=0 && br <= 4095)
  //                               this.socket.send(JSON.stringify({query: 'set_startbrightness', startbrightness: br}));
  //                             else
  //                               console.log('incorrect startbrightness, should be >= 0 && < 4096');
  //                           }
  // this.SetRndAnimationDelay = function(delay)
  //                           {
  //                             if(delay>=0 && delay <= 10000)
  //                               this.socket.send(JSON.stringify({query: 'set_rndanimdelay', rndanimdelay: delay}));
  //                             else
  //                               console.log('incorrect rndanimdelay, should be >= 0 && < 10000');
  //                           }
  // this.SetRndLedsCount = function(count)
  //                           {
  //                             if(count>=1 && count <= 128)
  //                               this.socket.send(JSON.stringify({query: 'set_rndledscount', rndledscount: count}));
  //                             else
  //                               console.log('incorrect rndledscount, should be >= 1 && < 128');
  //                           }
  // //leds control
  // this.SetLed = function(index, val)
  //                     {
  //                       if(index>=0 && index <= 127 && val >= 0 && val <= 4095)
  //                         this.socket.send(JSON.stringify({query: 'set_led', led_index: index, led_val: val}));
  //                       else
  //                         console.log('incorrect led data, index should be > 0 && <= 127, val >=0 && <= 4095');
  //                     }
  // this.SetEqualizer = function(m, vals)
  //                     {
  //                       if(m == 'm0'||m == 'm1'||m == 'm2'||m == 'm3'||m == 'm4'||m == 'm5'||m == 'm6'||m == 'm7'||m == 'm8'||m == 'm9')
  //                       {
  //                         for(var i = 0; i < 10; i ++)
  //                           if( vals[i] < 0 || vals[i] > 15)
  //                           {
  //                             console.log('incorrect eq data, mode should be one of (m1, m2, m3, m4, m5, m6, m7, m8, m9, m0), val >=0 && <= 15');
  //                             return;
  //                           }
  //                         this.socket.send(JSON.stringify({query: 'set_eq', mode: m, eq_vals: vals}));
  //                       }
  //                       else
  //                         console.log('incorrect eq data, mode should be one of (m1, m2, m3, m4, m5, m6, m7, m8, m9, m0), val >=0 && <= 15');
  //                     }
  // this.QueryLeds = function()
  //                  {
  //                     this.socket.send(JSON.stringify({query: 'query_leds'}));
  //                  }
  // this.QueryFPS = function()
  //                  {
  //                     this.socket.send(JSON.stringify({query: 'query_fps'}));
  //                  }
  // this.QueryAll = function()
  //                 {
  //                   showProcess();
  //                   this.socket.send(JSON.stringify({query: 'query_all'}));
  //                 }
  // this.ResetArduino = function()
  //                 {
  //                   this.socket.send(JSON.stringify({query: 'reset_arduino'}));
  //                 }
  // this.PingArduino = function()
  //                 {
  //                   this.socket.send(JSON.stringify({query: 'ping_arduino'}));
  //                 }
  // this.SetFakeBeatMode = function(val)
  //                 {
  //                   if(val == 0 || val == 1)
  //                         this.socket.send(JSON.stringify({query: 'set_fakebeatmode', fakebeatmode: val}));
  //                 }
  this.sendObject = function(val)
          {
           
                  this.socket.send(JSON.stringify(val));
          }
//overridable
  //device connection
  this.OnConnected=function (){console.log('connected default handler'); }
  this.OnDisconnected=function (){console.log('disconnected default handler');  }
  //wifi
  // this.OnWiFiError=function (descr){console.log('WiFi default error handler: ' + descr); }
  // this.OnWiFiProgress=function (){console.log('WiFi default progress handler'); }
  // this.OnWiFiCompleted=function (){console.log('WiFi default completed handler'); }
  // this.OnWiFiListReady=function(wifiList){console.log('wifi list default handler: ' + wifiList); }
  // this.OnWiFiListProgress=function(){console.log('wifi list progress default handler');}
  // //operation modes
  // this.OnSignalSourceChanged=function(src){console.log('default src changed handler: ' + src); }
  // this.OnModeChanged=function(mode){console.log('default mode changed handler: ' + mode); }
  // //visualization parameters
  // this.OnThresholdChanged=function(val){console.log('default Threshold changed handler: ' + val); }
  // this.OnMinDelayChanged=function(val){console.log('default MinDelay changed handler: ' + val); }
  // this.OnFadeOutDelayChanged=function(val){console.log('default FadeOutDelay changed handler: ' + val); }
  // this.OnStartBrightnessChanged=function(val){console.log('default StartBrightness changed handler: ' + val); }
  // this.OnAllOffDelayChanged=function(val){console.log('default AllOffDelay changed handler: ' + val); }
  // this.OnRndAnimationDelayChanged=function(val){console.log('default RndAnimationDelay changed handler: ' + val); }
  // this.OnRndLedsCountChanged=function(val){console.log('default RndLedsCount changed handler: ' + val); }
  //leds info
  // this.OnLedsInfo=function(leds_info){
  //     console.log('default leds info handler: ' + leds_info);
  // }
  // this.OnEqualizerInfo=function(eq_info){
  //   console.log('default equalizer info handler: ' + eq_info);
  // }
  // this.OnArduinoError=function(){
  //   console.log('default arduino connection error handler');
  // }
  // this.OnArduinoFPS=function(val){
  //   console.log('default arduino fps info handler: ' + val);
  // }
  this.onRawMessage=function(val){
    console.log('Raw msg default handler: ' + val);
  }
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////
//internal
  _this_obj = this;
  this.MessageHandler = function (msg)
  {
    obj = JSON.parse(msg.data);
    _this_obj.onRawMessage(msg.data);
    // if(obj.type == 'wifi_changing')
    // {
    //   if(obj.wifi_changing.state == 'error')
    //     _this_obj.OnWiFiError(obj.wifi_changing.descr);
    //   else if(obj.wifi_changing.state == 'completed')
    //     _this_obj.OnWiFiCompleted();
    //   else if(obj.wifi_changing.state == 'progress')
    //     _this_obj.OnWiFiProgress();
    // }
    // else if(obj.type == 'wifi_list')
    // {
    //   if(obj.wifi_list.state == 'querying')
    //     _this_obj.OnWiFiListProgress();
    //   else if(obj.wifi_list.state == 'ready')
    //   {
    //     _this_obj.wifi_list = obj.wifi_list.list;
    //     _this_obj.OnWiFiListReady(obj.wifi_list.list);
    //   }
    // }
    // else if(obj.type == 'arduino')
    // {
    //   console.log('A: ', obj.arduino_output)
    // }
    // else if(obj.type == 'source')
    // {
    //   _this_obj.signalSource = obj.source;
    //   _this_obj.OnSignalSourceChanged(obj.source);
    // }
    // else if(obj.type == 'mode')
    // {
    //   _this_obj.mode = obj.mode;
    //   _this_obj.OnModeChanged(obj.mode);
    // }
    // else if(obj.type == 'thres')
    // {
    //   _this_obj.threshold = obj.thres;
    //   _this_obj.OnThresholdChanged(obj.thres);
    // }
    // else if(obj.type == 'mindelay')
    // {
    //   _this_obj.minDelay = obj.mindelay;
    //   _this_obj.OnMinDelayChanged(obj.mindelay);
    // }
    // else if(obj.type == 'fadeoutdelay')
    // {
    //   _this_obj.fadeoutDelay = obj.fadeoutdelay;
    //   _this_obj.OnFadeOutDelayChanged(obj.fadeoutdelay);
    // }
    // else if(obj.type == 'alloffdelay')
    // {
    //   _this_obj.allOffDelay = obj.alloffdelay;
    //   _this_obj.OnAllOffDelayChanged(obj.alloffdelay);
    // }
    // else if(obj.type == 'startbrightness')
    // {
    //   _this_obj.startBrightness = obj.startbrightness;
    //   _this_obj.OnStartBrightnessChanged(obj.startbrightness);
    // }
    // else if(obj.type == 'rndledscount')
    // {
    //   _this_obj.rndLedsCount = obj.rndledscount;
    //   _this_obj.OnRndLedsCountChanged(obj.rndledscount);
    // }
    // else if(obj.type == 'rndanimdelay')
    // {
    //   _this_obj.rndAnimDelay = obj.rndanimdelay;
    //   _this_obj.OnRndAnimationDelayChanged(obj.rndanimdelay);
    // }
    // else if(obj.type == 'leds_info')
    // {
    //   _this_obj.ledsValues = obj.leds_info;
    //   _this_obj.OnLedsInfo(obj.leds_info);
    // }
    // else if(obj.type == 'eq_info')
    // {
    //   _this_obj.eqLists = obj.eq;
    //   _this_obj.OnEqualizerInfo(obj.eq);
    // }
    // else if(obj.type == 'arduino_error')
    //   _this_obj.OnArduinoError();
    // else if(obj.type == 'arduino_fps')
    // {
    //   _this_obj.arduinoFPS = obj.arduino_fps;
    //   _this_obj.OnArduinoFPS(obj.arduino_fps);
    // }
    // else if(obj.type == 'arduino_dbg')
    // {
    //   _this_obj.OnArduinoDbg(obj.arduino_dbg);
    // }
  }

  this.socket = new WebSocket(host);

  this.hostTimeout = function() {
    if(_this_obj.socket.readyState != _this_obj.socket.OPEN)
    {
      console.log("AviastudentWS reconnecting");
      _this_obj.socket.onclose  = function()  {  }

      _this_obj.socket = new WebSocket(host);
      _this_obj.socket.onopen = function()
                            {
                              _this_obj.OnConnected();
                            }
      _this_obj.socket.onclose= function()
                            {
                              _this_obj.OnDisconnected();
                            }
      _this_obj.socket.onmessage = _this_obj.MessageHandler;
    }
    else
      _this_obj.socket.send('{"ping":""}');
  }
  window.setInterval(this.hostTimeout, 2000);

  this.socket.onopen = function()
                          {
                            _this_obj.OnConnected();
                          }
  this.socket.onclose = function()
  {
    _this_obj.OnDisconnected();
  }
  this.socket.onmessage = this.MessageHandler;
}