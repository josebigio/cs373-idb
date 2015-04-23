/*
 * I/O(1/0) Matrix on Canvas
 * leeethe@gmail.com
 */
// Bind polyfill from MDN
// --------------------------------------------
if (!Function.prototype.bind) {
  Function.prototype.bind = function(oThis) {
    if (typeof this !== "function") {
      // closest thing possible to the ECMAScript 5 internal IsCallable function
      throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
    }

    var aArgs = Array.prototype.slice.call(arguments, 1),
      fToBind = this,
      fNOP = function() {},
      fBound = function() {
        return fToBind.apply(this instanceof fNOP && oThis ? this : oThis || window,
          aArgs.concat(Array.prototype.slice.call(arguments)));
      };

    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();

    return fBound;
  };
}
// --------------------------------------------

var Io = function() {};
Io.prototype = {
  // Params
  constructor: Io,
  canvas: document.getElementById('canvas'),
  units: [],
  unit: {
    width: 22,
    height: 32,
  },
  // Function
  // ------------------
  // init
  init: function() {
    canvas.addEventListener("mousemove", this.move, false);
    window.addEventListener("resize", this.resize.bind(this), false);
    this.resize();
    setInterval(this.repaint.bind(this), 100);
  },

  move: function(e) {
    mouse.x = e.layerX;
    mouse.y = e.layerY;
  },

  resize: function() {
    this.canvas.width = window.innerWidth * 0.97;
    this.canvas.height = window.innerHeight * 0.97;
    this.deposite();
  },
  // repaint (main#2)
  repaint: function() {
    context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    var units = this.units;
    for (var i = 0; i < this.units.length; i++) {
      var unit = units[i];
      var distance = this.distance(mouse, unit);
      if (distance < 150) {
        unit.text = (Math.random() > 0.5) ? 1 : 0;
        // unit.text = (unit.index % 2) ? 1 : 0;
        // unit.color = randomColor();
        context.font = "12px Arial";
      } else {
        unit.text = (unit.index % 2) ? 1 : 0;
        unit.color = "#1A850E"
        context.font = "14px Arial";
      }
      context.textAlign = "center";
      context.fillStyle = unit.color;
      context.fillText(unit.text, unit.x, unit.y);
    }
  },

  distance: function(e, t) {
    var n = t.x - e.x;
    var r = t.y - e.y;
    return Math.sqrt(n * n + r * r)
  },

  // deposite (main#1)
  deposite: function() {
    this.units = [];
    // each unit should span the width of $this.unit.width
    var col = Math.floor(this.canvas.width / this.unit.width),
      // and the height of $this.unit.height
      row = Math.floor(this.canvas.height / this.unit.height);
    for (var c = 0; c < col; c++) {
      for (var r = 0; r < row; r++) {
        this.units.push({
          // position units
          x: Math.floor(this.unit.width * (c + 1)),
          y: Math.floor(this.unit.height * (r + 1)),
          index: (function() {
            return (r % 2) ? c : c + 1;
          })(),
          color: "#1A850E"
        });
      }
    }
  }
}

// instance run
if (canvas && canvas.getContext) {
  var context = canvas.getContext("2d"),
    mouse = {
      x: 300,
      y: 300
    }
  new Io().init()
}