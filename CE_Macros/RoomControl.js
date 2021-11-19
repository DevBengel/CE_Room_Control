import xapi from 'xapi';


global.lightstate='Off';
global.dimmer_Value=0;;


function changeLightStatus(host,value) {
  console.log(value);
  const headers = [
    'Content-Type: application/json',
  ];
  console.log (host)

  switch (value) {

    case 'on':
      console.log('on');
      lightstate='On';
      return xapi.Command.HttpClient.Put({ Header: headers, Url: host }, '{"switch_State":"'+lightstate+'","dimmer_State":"'+dimmer_Value+'"}');
      break;
    case 'off':
      console.log('off');
      lightstate='Off';
      return xapi.Command.HttpClient.Put({ Header: headers, Url: host }, '{"switch_State":"'+lightstate+'","dimmer_State":"'+dimmer_Value+'"}');
      break;
  }
}
function changeDimmerValue(host,value){
  console.log("Changing Dimmer Value")
  dimmer_Value=Math.round((value*100)/256)
  return xapi.Command.HttpClient.Put({ Header:'Content-Type: application/json', Url: host }, '{"switch_State":"'+lightstate+'","dimmer_State":"'+dimmer_Value+'"}');
  
}


function guiEvent(event) {
  if (event.WidgetId === 'light_toggle') {
    console.log(event.Value)
    changeLightStatus("http://192.168.2.119:5001",event.Value)
  }
  if (event.WidgetId === 'slider'){
    console.log(event.Value)
    changeDimmerValue("http://192.168.2.119:5001",event.Value)
  }
}

xapi.Event.UserInterface.Extensions.Widget.Action.on(guiEvent);




