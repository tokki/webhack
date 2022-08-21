(function () {
  const canvas = document.getElementById("radar");
  const ctx = canvas.getContext("2d");
  const map = document.getElementById("map");
  const btn = document.getElementById("btn");
  btn.addEventListener("click", function () {
    var url = document.getElementById("server").value;
    if (url == "") {
      url = "ws://127.0.0.1:9999";
    }
    const ws = new WebSocket(url);
    run(ws);
  });

  var ratio = 2;

  function query_map_info(name) {
    var url = "./img/" + name + ".txt";
    var mapinfo = {};
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send(null);
    if (xhr.status === 200) {
      let txt = xhr.responseText.split("\n");
      txt.forEach(function (line) {
        if (line.match("pos_x")) {
          let num = line.replace(/[^0-9.-]/g, "");
          mapinfo.pos_x = parseFloat(num);
        }
        if (line.match("pos_y")) {
          let num = line.replace(/[^0-9.-]/g, "");
          mapinfo.pos_y = parseFloat(num);
        }
        if (line.match("scale")) {
          let num = line.replace(/[^0-9.-]/g, "");
          mapinfo.scale = parseFloat(num);
        }
      });
      return mapinfo;
    } else {
      console.error(xhr.statusText);
    }
  }

  function draw_entity(x, y, health, mapinfo) {
    if (health > 0) {
      var map_x = (mapinfo.pos_x - x) / (-mapinfo.scale * ratio);
      var map_y = (mapinfo.pos_y - y) / (mapinfo.scale * ratio);
      //console.log(map_x);
      //console.log(map_y);
      ctx.beginPath();
      ctx.arc(map_x, map_y, 3, 0 * Math.PI, 2 * Math.PI);
      ctx.fillStyle = "red";
      ctx.fill();

      ctx.beginPath();
      ctx.fillStyle = "green";
      ctx.font = "12px bold";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(health, map_x, map_y + 12);
    }
  }

  function clear_canvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function run(ws) {
    ws.addEventListener("message", (e) => {
      const obj = JSON.parse(e.data);
      //console.log(obj);
      var mapname = "";
      var mapinfo = {};
      const newname = obj["map"];

      if (mapname != newname) {
        mapname = newname;
        map.src = "./img/" + mapname + "_radar.jpg";
        mapinfo = query_map_info(mapname);
      }

      var players = obj.player_list;

      if (players.length > 0) {
        clear_canvas();
        players.forEach(function (p) {
          draw_entity(p.pos_x, p.pos_y, p.health, mapinfo);
        });
      }
    });
  }
})();
