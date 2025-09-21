class cloud {
  constructor(x,y,cc, vel) {
    this.x = x;
    this.y = y;
    this.circ_coords = cc;
    this.v = vel;
    }
  show(rat) {
    fill(60+(rat * 185));
    noStroke();
    for (let i = 0; i < this.circ_coords.length; i++) {
      circle(this.circ_coords[i][0], this.circ_coords[i][1], 25);
    }
  }
  update() {
    for (let i = 0; i < this.circ_coords.length; i++) {
      this.circ_coords[i][0] += this.v * 0.5;
      if (this.circ_coords[i][0] > width) {
        this.circ_coords[i][0] = 0;
      }
    }
  }
}

function preload(){
  img1 =loadImage("images/moon.avif")
}

let clouds = [];
let stars = [];

function setup() {
  createCanvas(600, 600);
  let n = random(1);
  for (let i = 0; i < 8; i++) {
    let x = random(0, width);
    let y = random(0, height);
    let vel = random(1);
    let num_circles = int(random(10)) + 7;
    let circ_coords = [];
    let offset = 15;
    for (let i = 0; i < num_circles; i++) {
      let dx = random(-offset, offset);
      let dy = random(-offset, offset);
      circ_coords.push([dx + x, dy + y]);
    }
    let c = new cloud(x, y, circ_coords, vel);
    clouds.push(c);
  }
  
  for (let i = 0; i < 50; i++) {
    let x = random(width);
    let y = random(height);
    stars.push([x,y]);
  }
}

function draw() {
  let d = dist(mouseX, mouseY, width / 2, height / 2);
  let w = 50;
  let rat = (d / w) * 100;

  if (rat > 100) {
    rat = 100;
  }

  colorMode(HSB);
  background(200, 23, 95 * (rat / 100));
  
  fill(200, 23 * (rat / 100), 95)
  for (let i = 0; i < stars.length; i++) {
    circle(stars[i][0],stars[i][1],5);
  }

  fill(57, 81, 100);
  circle(width / 2, height / 2, w);

  image(img1,mouseX - 53/2,mouseY - 53/2,53,53);

  fill(255 * (1 - rat / 100));
  textAlign(CENTER);
  text(join([str(round(100 - rat)), "%"], ""), width / 2, height * 0.8);
  
  for (let i = 0; i < clouds.length; i++) {
    clouds[i].show(rat/100);
    clouds[i].update();
  }
}
