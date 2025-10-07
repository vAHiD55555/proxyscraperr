// proxy.pac - generated sample (obfuscated hex list)
var _0 = "50524f585920312e312e312e313a383038307c534f434b533520352e352e352e353a313038307c50524f585920322e322e322e323a33313238";

function _h2s(h) {
  var s = "";
  for (var i = 0; i < h.length; i += 2) {
    s += String.fromCharCode(parseInt(h.substr(i, 2), 16));
  }
  return s;
}

(function(){
  try {
    var _list = _h2s(_0).split("|");
    var iranSuffixes = [
      ".ir", ".ac.ir", ".co.ir", ".org.ir", ".gov.ir", ".net.ir", ".sch.ir", ".id.ir"
    ];
    var localPatterns = ["localhost", "127.0.0.1", "::1"];
    var localHostPatterns = ["*.local", "*.lan", "*.localdomain"];

    function endsWithAny(h, arr){
      if(!h) return false;
      var L = h.toLowerCase();
      for(var i=0;i<arr.length;i++){
        if(L === arr[i] || L.endsWith(arr[i])) return true;
      }
      return false;
    }

    function FindProxyForURL(url, host) {
      if(!host) return "DIRECT";
      for (var i=0;i<localPatterns.length;i++){
        if(host === localPatterns[i]) return "DIRECT";
      }
      for (var j=0;j<localHostPatterns.length;j++){
        if(shExpMatch(host, localHostPatterns[j])) return "DIRECT";
      }
      if (endsWithAny(host, iranSuffixes)) return "DIRECT";
      if (isInNet(host, "10.0.0.0", "255.0.0.0")) return "DIRECT";
      if (isInNet(host, "172.16.0.0", "255.240.0.0")) return "DIRECT";
      if (isInNet(host, "192.168.0.0", "255.255.0.0")) return "DIRECT";

      if(_list.length === 0) return "DIRECT";
      var idx = Math.floor((+new Date())/3600000) % _list.length;
      var selected = _list[idx] || _list[0];
      return selected;
    }

    this.FindProxyForURL = FindProxyForURL;
  } catch(e) {
    this.FindProxyForURL = function(){ return "DIRECT"; };
  }
})();
