// set url params
// if params not exists in url, then add params
// if params exists in url, then replace
function setUrlParams (url, params) {
  var parts = url.split("?");
  var path = parts[0]
  var old_params = {};
  if (parts.length == 1);
  else {
    var items = parts[1].split("&");
    for (var i in items) {
      var item = items[i].split('=')
      if (item.length == 2) {
        old_params[item[0]] = item[1]
      }
    }
  }
  for (var key in params) {
    var value = params[key];
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);
    old_params[key] = value
  }
  if (Object.keys(old_params).length) {
    var items = [];
    for (var key in old_params) {
      items.push(key + '=' + old_params[key])
    }
    return path + '?' + items.join('&')
  }
  return path;
}

function getQueryParams (url) {
  var parts = url.split('#')[0].split("?")
  if (parts.length == 1) return {};
  else if (parts.lenght > 2) return undefined;

  var query_string = {};
  var query = parts[1];
  var vars = query.split("&");
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    // If first entry with this name
    if (typeof query_string[pair[0]] === "undefined") {
      query_string[pair[0]] = pair[1];
      // If second entry with this name
    } else if (typeof query_string[pair[0]] === "string") {
      var arr = [query_string[pair[0]], pair[1]];
      query_string[pair[0]] = arr;
      // If third or later entry with this name
    } else {
      query_string[pair[0]].push(pair[1]);
    }
  }
  return query_string;
}