function AviastudentWS()
{

  this.fb_access_token = ""
  this.host = "wss://online.aviastudent.ru:444/ws";
  _this_obj = this;
  this.loginFacebook = function(accessToken) {
    $.post( "/api/v1/auth/facebook/", { "access_token": accessToken, "backend": "facebook" })
              .done(function( data ) {
                localStorage.setItem("token", data.token);
                _this_obj.setToken(data.token);
               _this_obj.onLoggedIn();
               _this_obj.fb_access_token = accessToken;
              });
  }
  this.logOut = function() {

        localStorage.setItem("token", "");
          console.log("Logged out")
        
          _this_obj.setToken("");
          _this_obj.onLoggedOut()
  }
//public methods
  this.sendObject = function(val)
          {
            if(_this_obj.socket != null) {
                 val.token = _this_obj.token;
                  _this_obj.socket.send(JSON.stringify(val));
                }
                else {
                  console.log('AviastudentWS not connected, cannot send data')
                }
          }
  this.isLoggedIn = function() {
    return localStorage.getItem("token") == "";
  }
//overridable
  //device connection
this.onLoggedIn=function (){console.log('onLoggedIn default handler'); }
this.onLoggedOut=function (){console.log('onLoggedOut default handler'); }

  this.onConnected=function (){console.log('connected default handler'); }
  this.onDisconnected=function (){console.log('disconnected default handler');  }
  this.onKicked=function (){console.log('kicked default handler');  }

  this.onRawMessage=function(val){
    console.log('Raw msg default handler: ' + val);
  }
  this.onTelemetryUpdate = function(vehicle_id, timestamp, tel_data) {
      console.log('RonTelemetryUpdate default handler: ', vehicle_id, timestamp, JSON.stringify(tel_data));
  }
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////

  this.setToken = function(token_str) {
    console.log("AviastudentWS:  token set:", token_str)
    if(token_str == "") {
    //     if(_this_obj != undefined && _this_obj.socket != undefined)
    //       _this_obj.socket.close();
    //     _this_obj.socket = null;
    //     // $.ajaxSetup({headers: {"Authorization": ""}})
    }
    else if(_this_obj.token != token_str) {
    //   _this_obj.socket = new WebSocket(_this_obj.host);
    //   _this_obj.socket.onclose  = function()  {  }
      
    //   _this_obj.socket.onopen = function()
    //                         {
    //                           _this_obj.sendObject({'ffuuuu':'f'})
    //                           _this_obj.onConnected();
    //                         }
    //   _this_obj.socket.onclose= function()
    //                         {
    //                           _this_obj.onDisconnected();
    //                         }
    //   _this_obj.socket.onmessage = this.MessageHandler;
      
      
    }
    _this_obj.token = token_str
    // $.ajaxSetup({headers: {"Authorization": "JWT " + token_str}})
  }
  
  this.get = function(url_to_get) {
    return $.ajax( {url: url_to_get, headers: {"Authorization": "JWT " + _this_obj.token}})
  }
//internal
  
  this.MessageHandler = function (msg)
  {
    obj = JSON.parse(msg.data);
    _this_obj.onRawMessage(msg.data);
    if(obj.msg_type == "telem_update") {
        _this_obj.onTelemetryUpdate(obj.vehicle_id, obj.timestamp, obj.data);
    }
    else if('error' in obj && obj.error == 'not authorized'){
        _this_obj.logOut()
        _this_obj.onKicked()

    }
 
  }

  this.hostTimeout = function() {
    if(_this_obj.socket == null || _this_obj.socket.readyState != _this_obj.socket.OPEN)
    {
      
      console.log("AviastudentWS reconnecting");
      if(_this_obj.fb_access_token != "") {
          _this_obj.loginFacebook(_this_obj.fb_access_token)
      }
      if(_this_obj.token == "")
        return;
      if(_this_obj.socket  != null)
          _this_obj.socket.close();

      _this_obj.socket = new WebSocket(_this_obj.host);
      _this_obj.socket.onopen = function()
                            {
                              _this_obj.sendObject({'ffuuuu':'f'})
                              _this_obj.onConnected();
                            }
      _this_obj.socket.onclose= function()
                            {
                              _this_obj.onDisconnected();
                            }
      _this_obj.socket.onmessage = _this_obj.MessageHandler;
    }
    else
      _this_obj.socket.send('{"ping":""}');
  }
  _this_obj.socket == null
  _this_obj.setToken(localStorage.getItem("token"));
  window.setInterval(_this_obj.hostTimeout, 2000);
  // _this_obj.hostTimeout();
}

var aviastudentAPI = new AviastudentWS();